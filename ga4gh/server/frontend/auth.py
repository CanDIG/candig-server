"""
Contains the authentication decorators and functions

This separates out the authentication imports
so that the imports occur only in this module
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import functools
import socket
import urlparse
import json
import requests

import oic.oauth2
import oic.oic.message as message
from oauth2client.client import OAuth2Credentials

import flask
import flask.ext.cors as cors
from flask import request

import ga4gh.server.exceptions as exceptions

import ga4gh.server.auth as auth


# Added by Kevin Chan
def requires_token(f, app, oidc):
    """
    Decorator function that ensures that the token is valid,
    if the token is invalid or expired, the user will be
    redirected to the login page. Much of the authorization
    code flow is done solely by the function decorator
    @oidc.require_login
    """
    @functools.wraps(f)
    def decorated(*args, **kargs):
        if app.config.get("KEYCLOAK"):
            hostname = socket.gethostbyname(socket.gethostname())
            redirectUri = 'http://{0}:{1}{2}'.format(
                    hostname, app.myPort, request.path)
            try:
                info = oidc.user_getinfo(['sub'])
                subStore = oidc.credentials_store[info.get('sub')]
                credentials = OAuth2Credentials.from_json(subStore)
                tokenResponse = credentials.token_response
                introspectArgs = {
                    "token": tokenResponse["access_token"],
                    "client_id": oidc.client_secrets["client_id"],
                    "client_secret": oidc.client_secrets["client_secret"],
                    "refresh_token": tokenResponse["refresh_token"],
                }
            except:
                return flask.redirect(redirectUri)
            introspect = oidc.client_secrets["token_introspection_uri"]
            userInfo = requests.post(url=introspect, data=introspectArgs)

            if userInfo.status_code != 200:
                raise exceptions.NotAuthenticatedException()
        return f(*args, **kargs)
    return decorated


def startLogin(app):
    """
    If user is not logged in, this generates the redirect URL
    to the OIDC or Auth provider (depending on the configuration)
    Returns: the redirect response
    """
    SECRET_KEY_LENGTH = 24
    flask.session["state"] = oic.oauth2.rndstr(SECRET_KEY_LENGTH)
    flask.session["nonce"] = oic.oauth2.rndstr(SECRET_KEY_LENGTH)
    provInfo = app.oidcClient.provider_info
    args = {
        "client_id": app.oidcClient.client_id,
        "response_type": "code",
        "scope": ["openid", "profile"],
        "nonce": flask.session["nonce"],
        "redirect_uri": app.oidcClient.redirect_uris[0],
        "authorization_endpoint": provInfo["authorization_endpoint"],
        "state": flask.session["state"],
    }

    # First condition is the configuration for the Keycloak Server.
    # Redirects the user to the Keycloak sign in page.
    # I left this here for your reference.
    # Added by Kevin Chan

    if "WELL_KNOWN_CONFIG" in app.config:
        # result = app.oidcClient.do_authorization_request(
        #     request_args=args, state=flask.session["state"])
        result = app.oidcClient.construct_AuthorizationRequest(
            request_args=args)
        addOn = result.request(app.oidcClient.authorization_endpoint)
        authInfo = app.oidcClient.provider_info["authorization_endpoint"]
        loginUrl = authInfo + addOn

        if request.path == "/login":
            flask.session["path"] = "/"
        else:
            flask.session["path"] = request.path
        return flask.redirect(loginUrl)

    result = app.oidcClient.do_authorization_request(
        request_args=args, state=flask.session["state"])
    return flask.redirect(result.url)


# New configuration added by Kevin Chan
# @app.route("/login")
def login(app):

    if app.config.get('AUTH0_ENABLED'):
        if (flask.request.args.get('code')):
            return auth.render_key(app, key=flask.request.args.get('code'))
        else:
            return auth.render_login(
                app=app,
                scopes=app.config.get('AUTH0_SCOPES'),
                redirect_uri=app.config.get('AUTH0_CALLBACK_URL'),
                domain=app.config.get('AUTH0_HOST'),
                client_id=app.config.get('AUTH0_CLIENT_ID'))

    # Configuration for KeyCloak Server
    elif app.config.get('KEYCLOAK'):
        app.oidClient = None
        flask.session.clear()
        return startLogin()

    else:
        raise exceptions.NotFoundException()


# @app.route("/logout")
# @authenticator.requires_auth
@cors.cross_origin(headers=['Content-Type', 'Authorization'])
def logout(app):
    if app.config.get('AUTH0_ENABLED'):
        key = flask.session['auth0_key']
        auth.logout(app.cache)
        url = 'https://{}/v2/logout?access_token={}&?client_id={}'.format(
            app.config.get('AUTH0_HOST'),
            key,
            app.config.get('AUTH0_CLIENT_ID'),
            app.config.get('AUTH0_CALLBACK_URL'))
        return flask.redirect(url)
    else:

        # args = {
        #    "token": app.oidcClient.token["access_token"],
        #    "client_id": app.oidcClient.client_id,
        #    "client_secret": app.oidcClient.client_secret,
        #    "refresh_token": app.oidcClient.token["refresh_token"]
        #    }

        # endpoint = app.oidcClient.provider_info["session_endpoint"]
        # logout = requests.post(url=endpoint, data=args)
        flask.session.clear()
        hostname = socket.gethostbyname(socket.gethostname())
        return flask.redirect("http://{0}:{1}".format(hostname, app.myPort))


# @app.route('/oauth2callback', methods=['GET'])
def oidcCallback(app):
    """
    Once the authorization provider has cleared the user, the browser
    is returned here with a code. This function takes that code and
    checks it with the authorization provider to prove that it is valid,
    and get a bit more information about the user (which we don't use).

    A token is generated and given to the user, and the authorization info
    retrieved above is stored against this token. Later, when a client
    connects with this token, it is assumed to be a valid user.

    :return: A display of the authentication token to use in the client. If
    OIDC is not configured, raises a NotImplementedException.
    """
    SECRET_KEY_LENGTH = 24
    if app.oidcClient is None:
        raise exceptions.NotImplementedException()

    response = dict(flask.request.args.iteritems(multi=True))
    aresp = app.oidcClient.parse_response(
        message.AuthorizationResponse,
        info=response,
        sformat='dict')
    sessState = flask.session.get('state')
    respState = aresp['state']
    if (not isinstance(aresp, message.AuthorizationResponse) or
            respState != sessState):
        raise exceptions.NotAuthenticatedException()

    args = {
        "code": aresp['code'],
        "redirect_uri": app.oidcClient.redirect_uris[0],
        "client_id": app.oidcClient.client_id,
        "client_secret": app.oidcClient.client_secret
    }

    atr = app.oidcClient.do_access_token_request(
        scope="openid",
        state=respState,
        request_args=args)
    if not isinstance(atr, message.AccessTokenResponse):
        raise exceptions.NotAuthenticatedException()

    atrDict = atr.to_dict()
    if flask.session.get('nonce') != atrDict['id_token']['nonce']:
        raise exceptions.NotAuthenticatedException()
    key = oic.oauth2.rndstr(SECRET_KEY_LENGTH)
    flask.session['key'] = key
    token_data = aresp["code"], respState, atrDict
    app.cache.set(key, token_data)
    # flask.url_for is broken. It relies on SERVER_NAME for both name
    # and port, and defaults to 'localhost' if not found. Therefore
    # we need to fix the returned url
    indexUrl = flask.url_for('index', _external=True)
    indexParts = list(urlparse.urlparse(indexUrl))
    if ':' not in indexParts[1]:
        indexParts[1] = '{}:{}'.format(socket.gethostname(), app.myPort)
        indexUrl = urlparse.urlunparse(indexParts)
    response = flask.redirect(indexUrl)
    return response


# Leaving this function here for reference for the Authorization Code flow
# Added by Kevin Chan
# @app.route('/keycallback')
def keycloakCallback(app):
    """
    Similar to the oidcCallback function, once the authorization provider
    has cleared the user, browser is returned here with a code. The code
    is then checked with the authorization provider and if valid a token
    is returned.

    The token is stored in the session, and the user is assumed to be valid.

    Returns: a token and the redirect url to the new page.
    """
    if app.oidcClient is None:
        raise exceptions.NotImplementedException()

    response = dict(flask.request.args.iteritems(multi=True))
    authMsg = message.AuthorizationResponse
    aresp = app.oidcClient.parse_response(
        authMsg, info=response, sformat="dict")
    respState = aresp["state"]
    sessState = flask.session.get('state')

    if sessState != respState:
        raise exceptions.NotAuthorizedException()

    args = {
        "code": aresp["code"],
        "redirect_uri": app.oidcClient.redirect_uris[0],
        "client_id": app.oidcClient.client_id,
        "client_secret": app.oidcClient.client_secret,
        "token_endpoint": app.oidcClient.provider_info["token_endpoint"],
        "grant_type": "authorization_code",
    }

    endpoint = app.oidcClient.provider_info["token_endpoint"]
    tokResp = requests.post(url=endpoint, data=args)
    tokContent = json.loads(tokResp.content)
    # token = tokContent["access_token"]

    if tokResp.status_code != 200:
        raise exceptions.NotAuthorizedException()
    app.oidcClient.token = tokContent

    # flask.session["key"] = idGenerator(size=SECRET_KEY_LENGTH)
    # This next line will display the access token on the server front end.
    # If you do not want this uncomment the line above
    flask.session["key"] = app.oidcClient.token["access_token"]
    # change the url depending on where the GA4GH server is hosted
    hostname = socket.gethostname()
    path = flask.session["path"]
    host = socket.gethostbyname(hostname, app.myPort, path)
    redirectUri = 'http://{0}:{1}{2}'.format(host)
    return flask.redirect(redirectUri)


# Commented out by Kevin Chan.
# If Using the Keycloak Config or no authentication
# this function is no longer needed
"""
@app.before_request
def checkAuthentication():

    The request will have a parameter 'key' if it came from the command line
    client, or have a session key of 'key' if it's the browser.
    If the token is not found, start the login process.

    If there is no oidcClient, we are runnning naked and we don't check.
    If we're being redirected to the oidcCallback we don't check.

    :returns None if all is ok (and the request handler continues as usual).
    Otherwise if the key was in the session (therefore we're in a browser)
    then startLogin() will redirect to the OIDC provider. If the key was in
    the request arguments, we're using the command line and just raise an
    exception.

    if app.oidcClient is None:
        return

    oidcCall = flask.request.endpoint == 'oidcCallback'
    keyCall = flask.request.endpoint == "keycloakCallback"
    if oidcCall or keyCall:
        return
    key = flask.session.get('key') or flask.request.args.get('key')

    if key is None: # or not app.cache.get(key):
        if 'key' in flask.request.args:
            raise exceptions.NotAuthorizedException()
        else:
            return startLogin()
"""
