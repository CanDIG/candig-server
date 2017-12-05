"""
The endpoint routers for the Flask server frontend of the GA4GH API.
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import flask
#from flask import current_app
#from flask import request

import ga4gh.server.backend as backend
import ga4gh.server.exceptions as exceptions
import ga4gh.server.auth as auth
import ga4gh.schemas.protocol as protocol


def getFlaskResponse(responseString, httpStatus=200):
    """
    Returns a Flask response object for the specified data and HTTP status.
    """
    MIMETYPE= "application/json"
    print('getFlaskResponse')
    print(responseString)
    print(httpStatus)
    response = flask.Response(responseString, status=httpStatus, mimetype=MIMETYPE)
    print(response)
    return response

def handleHttpPost(request, endpoint):
    """
    Handles the specified HTTP POST request, which maps to the specified
    protocol handler endpoint and protocol request class.
    """
    print('handleHttpPost')
    print(request)
    print(endpoint)
    MIMETYPE= "application/json"
    if request.mimetype and request.mimetype != MIMETYPE:
        raise exceptions.UnsupportedMediaTypeException()
    request = request.get_data()
    print('Request')
    print(request)
    if request == '' or request is None:
        request = '{}'
    responseStr = endpoint(request)
    print('Response String')
    print(responseStr)
    return getFlaskResponse(responseStr)


def handleList(endpoint, request):
    """
    Handles the specified HTTP GET request, mapping to a list request
    """
    responseStr = endpoint(request.get_data())
    return getFlaskResponse(responseStr)


def handleHttpGet(id_, endpoint):
    """
    Handles the specified HTTP GET request, which maps to the specified
    protocol handler endpoint and protocol request class
    """
    print('handleHttpGet')
    print(id_)
    print(endpoint)
    responseStr = endpoint(id_)
    print(responseStr)
    #return responseStr
    response = flask.Response(responseStr, status=200, mimetype="application/json")
    print(response)
    return response
    #return getFlaskResponse(responseStr)


def handleHttpOptions(self):
    """
    Handles the specified HTTP OPTIONS request.
    """
    response = getFlaskResponse("")
    response.headers.add("Access-Control-Request-Methods", "GET,POST,OPTIONS")
    return response


# @app.errorHandler(Exception)
def handleException(exception, app):
    """
    Handles an exception that occurs somewhere in the process of handling
    a request.
    """
    serverException = exception
    if not isinstance(exception, exceptions.BaseServerException):
        with app.test_request_context():
            app.log_exception(exception)
        serverException = exceptions.getServerError(exception)
    error = serverException.toProtocolElement()
    # If the exception is being viewed by a web browser, we can render a nicer
    # view.
    if flask.request and 'Accept' in flask.request.headers and \
            flask.request.headers['Accept'].find('text/html') != -1:
        message = "<h1>Error {}</h1><pre>{}</pre>".format(
                    serverException.httpStatus,
                    protocol.toJson(error))
        if serverException.httpStatus == 401 \
                or serverException.httpStatus == 403:
            message += "Please try <a href=\"/login\">logging in</a>."
        return message
    else:
        responseStr = protocol.toJson(error)
        return getFlaskResponse(responseStr, serverException.httpStatus)




def handleFlaskGetRequest(id, flaskRequest, endpoint):
    """
    Handles the specified flask request for one of the GET URLs
    Invokes the specified endpoint to generate a response.
    """
    if flaskRequest.method == "GET":
        return handleHttpGet(id, endpoint)
    else:
        raise exceptions.MethodNotAllowedException()


def handleFlaskListRequest(id_, flaskRequest, endpoint):
    """
    Handles the specified flask list request for one of the GET URLs.
    Invokes the specified endpoint to generate a response.
    """

    return handleList(endpoint, flaskRequest)


def handleFlaskPostRequest(flaskRequest, endpoint):
    """
    Handles the specified flask request for one of the POST URLS
    Invokes the specified endpoint to generate a response.
    """
    print('handleFlaskPostRequest')
    if flaskRequest.method == "POST":
        return handleHttpPost(flaskRequest, endpoint)
    elif flaskRequest.method == "OPTIONS":
        return handleHttpOptions()
    else:
        raise exceptions.MethodNotAllowedException()


def handleFlaskPostRequestSimple(endpoint):
    flaskRequest = flask.request
    return handleHttpPost(flaskRequest, endpoint)



#@app.route('/')
#@oidc.require_login
#@requires_token
def index(app):
    response = flask.render_template('index.html',
                                     info=app.serverStatus)
    if app.config.get('AUTH0_ENABLED'):
        key = (flask.request.args.get('key'))
        try:
            print(key)
            profile = app.cache.get(key)
        except:
            raise exceptions.NotAuthorizedException()
        if (profile):
            return response
        else:
            exceptions.NotAuthenticatedException()
    else:
        return response




#@app.route('/callback')
def callback_handling(app):
    if app.config.get('AUTH0_ENABLED'):
        return auth.callback_maker(
            cache=app.cache,
            domain=app.config.get('AUTH0_HOST'),
            client_id=app.config.get('AUTH0_CLIENT_ID'),
            client_secret=app.config.get('AUTH0_CLIENT_SECRET'),
            redirect_uri=app.config.get('AUTH0_CALLBACK_URL'))()
    else:
        raise exceptions.NotFoundException()


#@app.route('/favicon.ico')
#@app.route('/robots.txt')
def robots(app):
    return flask.send_from_directory(
        app.static_folder, flask.request.path[1:])


#@DisplayedRoute('/info', app)
#@requires_auth
#@oidc.require_login
def getInfo(app):
    action = app.backend.runGetInfo
    return handleFlaskGetRequest(None, flask.request, action)



#@DisplayedRoute('/listreferencebases', app, postMethod=True)
def listReferenceBases(app):
    action = app.backend.runListReferenceBases
    return handleFlaskListRequest(id, flask.request, action)


def searchEndpoint(app, endpoint):
    return handleFlaskPostRequest(flask.request, endpoint)



#@DisplayedRoute('/announce', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def announce(app):
    # We can't use the post handler here because we want detailed request
    # data.
    return app.backend.runAddAnnouncement(flask.request)


# The below methods ensure that JSON is returned for various errors
# instead of the default, html

#@app.errorhandler(401)
def unauthorizedHandler(errorString, app):
    return handleException(exceptions.UnauthorizedException(errorString), app)


#@app.errorhandler(404)
def pathNotFoundHandler(errorString, app):
    return handleException(exceptions.PathNotFoundException(), app)


#@app.errorhandler(405)
def methodNotAllowedHandler(errorString, app):
    return handleException(exceptions.MethodNotAllowedException(), app)


#@app.errorhandler(403)
def notAuthenticatedHandler(errorString, app):
    return handleException(exceptions.NotAuthenticatedException(errorString), app)


