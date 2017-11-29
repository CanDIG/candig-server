"""
The endpoint routers for the Flask server frontend of the GA4GH API.
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import flask
from flask import current_app
# from flask import request

import ga4gh.server.backend as backend
import ga4gh.server.exceptions as exceptions
import ga4gh.server.auth as auth
import ga4gh.schemas.protocol as protocol


def getFlaskResponse(responseString, httpStatus=200):
    """
    Returns a Flask response object for the specified data and HTTP status.
    """
    MIMETYPE= "application/json"
    return flask.Response(responseString, status=httpStatus, mimetype=MIMETYPE)


def handleHttpPost(request, endpoint):
    """
    Handles the specified HTTP POST request, which maps to the specified
    protocol handler endpoint and protocol request class.
    """
    MIMETYPE= "application/json"
    if request.mimetype and request.mimetype != MIMETYPE:
        raise exceptions.UnsupportedMediaTypeException()
    request = request.get_data()
    if request == '' or request is None:
        request = '{}'
    responseStr = endpoint(request)
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
    responseStr = endpoint(id_)
    return getFlaskResponse(responseStr)


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




def handleFlaskGetRequest(id_, flaskRequest, endpoint):
    """
    Handles the specified flask request for one of the GET URLs
    Invokes the specified endpoint to generate a response.
    """
    if flaskRequest.method == "GET":
        return handleHttpGet(id_, endpoint)
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
    if flaskRequest.method == "POST":
        return handleHttpPost(flaskRequest, endpoint)
    elif flaskRequest.method == "OPTIONS":
        return handleHttpOptions()
    else:
        raise exceptions.MethodNotAllowedException()



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


#@DisplayedRoute('/references/<id>', app)
#@requires_auth
#@oidc.require_login
#@requires_token
def getReference(id, app):
    action = app.backend.runGetReference
    return handleFlaskGetRequest(id, flask.request, action)


#@DisplayedRoute('/referencesets/<id>', app)
#@requires_auth
#@oidc.require_login
#@requires_token
def getReferenceSet(id, app):
    action = app.backend.runGetReferenceSet
    return handleFlaskGetRequest(id, flask.request, action)


#@DisplayedRoute('/listreferencebases', app, postMethod=True)
def listReferenceBases(app):
    action = app.backend.runListReferenceBases
    return handleFlaskListRequest(id, flask.request, action)


#@DisplayedRoute('/callsets/search', app, postMethod=True)
def searchCallSets(app):
    action = app.backend.runSearchCallSets
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/readgroupsets/search', app, postMethod=True)
def searchReadGroupSets(app):
    action = app.backend.runSearchReadGroupSets
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/reads/search', app, postMethod=True)
def searchReads(app):
    return handleFlaskPostRequest(
        flask.request, app.backend.runSearchReads)


#@DisplayedRoute('/referencesets/search', app, postMethod=True)
def searchReferenceSets(app):
    action = app.backend.runSearchReferenceSets
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/references/search', app, postMethod=True)
def searchReferences(app):
    action = app.backend.runSearchReferences
    return handleFlaskPostRequest(
        flask.request, action)


#@DisplayedRoute('/variantsets/search', app, postMethod=True)
def searchVariantSets(app):
    action = app.backend.runSearchVariantSets
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/variants/search', app, postMethod=True)
def searchVariants(app):
    action = app.backend.runSearchVariant
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/variantannotationsets/search', app, postMethod=True)
def searchVariantAnnotationSets(app):
    action = app.backend.runSearchVariantAnnotationSets
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/variantannotations/search', app, postMethod=True)
def searchVariantAnnotations(app):
    action = app.backend.runSearchVariantAnnotations
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/datasets/search', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def searchDatasets(app):
    action = app.backend.runSearchDatasets
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/featuresets/search', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def searchFeatureSets(app):
    action = app.backend.runSearchFeatureSets
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/features/search', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def searchFeatures(app):
    action = app.backend.runSearchFeatures
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/continuoussets/search', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def searchContinuousSets(app):
    action = app.backend.runSearchContinuousSets
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/continuous/search', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def searchContinuous(app):
    action = app.backend.runSearchContinuous
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/biosamples/search', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def searchBiosamples(app):
    action = app.backend.runSearchBiosamples
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/individuals/search', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def searchIndividuals(app):
    action = app.backend.runSearchIndividuals
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/peers/list', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def listPeers(app):
    action = app.backend.runListPeers
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/announce', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def announce(app):
    # We can't use the post handler here because we want detailed request
    # data.
    return app.backend.runAddAnnouncement(flask.request)


#@DisplayedRoute(
#    '/biosamples/<no(search):id>', app,
#    pathDisplay='/biosamples/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getBiosample(id, app):
    action = app.backend.runGetBiosample
    return handleFlaskGetRequest(id, flask.request, action)


#@DisplayedRoute(
#    '/individuals/<no(search):id>', app,
#    pathDisplay='/individuals/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getIndividual(id, app):
    action = app.backend.runGetIndividual
    return handleFlaskGetRequest(id, flask.request, action)


#@DisplayedRoute('/rnaquantificationsets/search', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def searchRnaQuantificationSets(app):
    action = app.backend.runSearchRnaQuantificationSets
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/rnaquantifications/search', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def searchRnaQuantifications(app):
    action = app.backend.runSearchRnaQuantifications
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute('/expressionlevels/search', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def searchExpressionLevels(app):
    action = app.backend.runSearchExpressionLevels
    return handleFlaskPostRequest(flask.request, action)


#@DisplayedRoute(
#    '/variantsets/<no(search):id>', app,
#    pathDisplay='/variantsets/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getVariantSet(id, app):
    action = app.backend.runGetVariantSet
    return handleFlaskGetRequest(id, flask.request, action)


#@DisplayedRoute(
#    '/variants/<no(search):id>', app,
#    pathDisplay='/variants/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getVariant(id, app):
    action = app.backend.runGetVariant
    return handleFlaskGetRequest(id, flask.request, action)


#@DisplayedRoute(
#    '/readgroupsets/<no(search):id>', app,
#    pathDisplay='/readgroupsets/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getReadGroupSet(id, app):
    action = app.backend.runGetReadGroupSet
    return handleFlaskGetRequest(id, flask.request, action)


#@DisplayedRoute('/readgroups/<id>', app)
#@requires_auth
#@oidc.require_login
#@requires_token
def getReadGroup(id, app):
    action = app.backend.runGetReadGroup
    return handleFlaskGetRequest(id, flask.request, action)


#@DisplayedRoute(
#    '/callsets/<no(search):id>', app,
#    pathDisplay='/callsets/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getCallSet(id, app):
    action = app.backend.runGetCallSet
    return handleFlaskGetRequest(id, flask.request, action)


#@DisplayedRoute(
#    '/featuresets/<no(search):id>', app,
#    pathDisplay='/featuresets/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getFeatureSet(id, app):
    return handleFlaskGetRequest(
        id, flask.request, app.backend.runGetFeatureSet)


#@DisplayedRoute(
#    '/features/<no(search):id>', app,
#    pathDisplay='/features/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getFeature(id, app):
    return handleFlaskGetRequest(
        id, flask.request, app.backend.runGetFeature)


#@DisplayedRoute(
#    '/continuoussets/<no(search):id>', app,
#    pathDisplay='/continuoussets/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getContinuousSet(id, app):
    return handleFlaskGetRequest(
        id, flask.request, app.backend.runGetContinuousSet)


#@DisplayedRoute(
#    '/rnaquantificationsets/<no(search):id>', app,
#    pathDisplay='/rnaquantificationsets/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getRnaQuantificationSet(id, app):
    return handleFlaskGetRequest(
        id, flask.request, app.backend.runGetRnaQuantificationSet)


#@DisplayedRoute(
#    '/rnaquantifications/<no(search):id>', app,
#    pathDisplay='/rnaquantifications/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getRnaQuantification(id, app):
    return handleFlaskGetRequest(
        id, flask.request, app.backend.runGetRnaQuantification)


#@DisplayedRoute(
#    '/expressionlevels/<no(search):id>', app,
#    pathDisplay='/expressionlevels/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getExpressionLevel(id, app):
    return handleFlaskGetRequest(
        id, flask.request, app.backend.runGetExpressionLevel)


#@DisplayedRoute(
#    '/datasets/<no(search):id>', app,
#    pathDisplay='/datasets/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getDataset(id, app):
    return handleFlaskGetRequest(
        id, flask.request, app.backend.runGetDataset)


#@DisplayedRoute(
#    '/variantannotationsets/<no(search):id>', app,
#    pathDisplay='/variantannotationsets/<id>')
#@requires_auth
#@oidc.require_login
#@requires_token
def getVariantAnnotationSet(id, app):
    return handleFlaskGetRequest(
        id, flask.request, app.backend.runGetVariantAnnotationSet)


#@DisplayedRoute('/phenotypes/search', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def searchPhenotypes(app):
    return handleFlaskPostRequest(
        flask.request, app.backend.runSearchPhenotypes)


#@DisplayedRoute('/featurephenotypeassociations/search', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def searchGenotypePhenotypes(app):
    return handleFlaskPostRequest(
        flask.request,
        app.backend.runSearchGenotypePhenotypes)


#@DisplayedRoute('/phenotypeassociationsets/search', app, postMethod=True)
#@requires_auth
#@oidc.require_login
#@requires_token
def searchPhenotypeAssociationSets(app):
    return handleFlaskPostRequest(
        flask.request, app.backend.runSearchPhenotypeAssociationSets)


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


