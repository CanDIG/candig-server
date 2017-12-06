from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import functools

import ga4gh.server.frontend.router as router
import ga4gh.server.auth as auth
import ga4gh.server.frontend.auth as frontAuth

# from flask import request
import flask


class routeFactory:
    """
    Constructs and registers routes for the GA4GH server with Flask

    This class serves as the intermediary between the backend and frontend

    The routeFactory is intended to be contained in the Core class of
    the frontend

    Fields:

    app - The flask application singleton
    oidc - The flask-oidc extension singleton
           This implements the authentication
    back - The backend for the GA4GH server
    requires_auth - OAuth2 Decorator for authentication
    """

    def __init__(self, app, oidc):
        """
        Constructor for the routeFactory

        This sets the fields for the routeFactory class

        Parameters:

        flask.app app - The flask application server singleton
                        for the GA4GH server

        oidc - The flask oidc extension singleton
        """
        self.oidc = oidc
        self.app = app
        self.back = self.app.backend
        self.requires_auth = auth.auth_decorator(self.app)
        self.register()

    def dispRoute(self, path, func, name, postMethod=False, pathDisplay=None):
        """
        Method for registering POST and GET endpoints
        """
        methods = None
        methodDisplay = None

        if postMethod:
            methodDisplay = 'POST'
            methods = ['POST', 'OPTIONS']
        else:
            methodDisplay = 'GET'
            # methods = ['GET', 'OPTIONS']

        if pathDisplay is None:
            pathDisplay = path

        self.app.urls.append((methodDisplay, pathDisplay))

        if methods is None:
            self.app.add_url_rule(path, name, func)
        else:
            self.app.add_url_rule(path, name, func, methods=methods)

    def bindApp(self, f):
        """
        Bind the application to the endpoint function
        Transforms f into a partial function

        Parameters:

        f - The function to pass the Flask application to

        Returns:

        transFunc - A partial function that holds f but with app already given
        """
        transFunc = functools.partial(f, app=self.app)
        return transFunc

    def registerException(self):
        """
        Method that registers exceptions for the Flask application

        There are five types of exceptions registered:

        Exception - Generic exception base class
        401 - Unauthorized
        403 - Not Authenticated
        404 - Path Not Found
        405 - Method Not Allowed

        Returns: None
        """

        # ExceptList is a list of pairs (E, F) such that:
        # - E is an Exception object
        # - F is the function to be called when E is raised

        exceptList = [(Exception, router.handleException),
                      (401, router.unauthorizedHandler),
                      (403, router.notAuthenticatedHandler),
                      (404, router.pathNotFoundHandler),
                      (405, router.methodNotAllowedHandler)]

        # register the exceptions in the exceptList by iteration:
        for item in exceptList:
            boundFunc = self.bindApp(item[1])
            self.app.register_error_handler(item[0], boundFunc)

    def subRegisterAlpha(self):
        callbackHandle = self.bindApp(router.callback_handling)
        robots = self.bindApp(router.robots)

        funcList = [
            ('/login', 'login', frontAuth.login),
            ('/logout', 'logout', self.requires_auth(frontAuth.logout)),
            ('/keycallback', 'keycloakCallback', frontAuth.keycloakCallback),
            ('/callback', 'callback', callbackHandle),
            ('/favicon.ico', 'favicon', robots),
            ('/robots.txt', 'robots.txt', robots)]

        for item in funcList:
            self.app.add_url_rule(item[0], item[1], item[2])

    def subRegisterBeta(self):
        secureList = [('/', 'index', router.index)]

        for item in secureList:
            authFunc = frontAuth.requires_token(item[2], self.app, self.oidc)
            secureFunc = self.oidc.require_login(authFunc)
            boundFunc = self.bindApp(secureFunc)
            self.app.add_url_rule(item[0], item[1], boundFunc)

        secureRouteList = [('/info', router.getInfo, 'info')]

        for item in secureRouteList:
            secureFunc = self.requires_auth(self.oidc.require_login(item[1]))
            boundFunc = self.bindApp(secureFunc)
            self.dispRoute(item[0], boundFunc, item[2])

        self.app.add_url_rule('/oauth2callback', 'oidcCallback',
                              frontAuth.oidcCallback, methods=['GET'])

        announceList = [
            ('/announce', router.announce, 'announce'),
            ('/listreferencebases', router.listReferenceBases,
             'listReferenceBases')]

        for item in announceList:
            authFunc = frontAuth.requires_token(item[1], self.app, self.oidc)
            secureFunc = self.requires_auth(self.oidc.require_login(authFunc))
            boundFunc = self.bindApp(secureFunc)
            self.dispRoute(item[0], boundFunc, item[2], postMethod=True)

    def register(self):
        """
        Entrypoint method for registering all
        endpoints to the Flask application

        Returns: None
        """
        self.subRegisterAlpha()
        self.subRegisterBeta()
        self.registerException()

        back = self.back

        tokenList = [
            ('/callsets/search',
             back.runSearchCallSets,
             'searchCallSets'),
            ('/readgroupsets/search',
             back.runSearchReadGroupSets,
             'searchReadGroupSets'),
            ('/reads/search',
             back.runSearchReads,
             'searchReads'),
            ('/referencesets/search',
             back.runSearchReferenceSets,
             'searchReferenceSets'),
            ('/references/search',
             back.runSearchReferences,
             'searchReferences'),
            ('/variantsets/search',
             back.runSearchVariantSets,
             'searchVariantSets'),
            ('/variants/search',
             back.runSearchVariants,
             'searchVariants'),
            ('/variantannotations/search',
             back.runSearchVariantAnnotations,
             'searchVariantAnnotations'),
            ('/variantannotationsets/search',
             back.runSearchVariantAnnotationSets,
             'searchAnnotationSets'),
            ('/datasets/search',
             back.runSearchDatasets,
             'searchDatasets'),
            ('/featuresets/search',
             back.runSearchFeatureSets,
             'searchFeatureSets'),
            ('/features/search',
             back.runSearchFeatures,
             'searchFeatures'),
            ('/continuoussets/search',
             back.runSearchContinuousSets,
             'searchContinuousSets'),
            ('/continuous/search',
             back.runSearchContinuous,
             'searchContinuous'),
            ('/biosamples/search',
             back.runSearchBiosamples,
             'searchBiosamples'),
            ('/individuals/search',
             back.runSearchIndividuals,
             'searchIndividuals'),
            ('/peers/list',
             back.runListPeers,
             'listPeers'),
            ('/rnaquantificationsets/search',
             back.runSearchRnaQuantificationSets,
             'searchRnaQuantificationSets'),
            ('/rnaquantifications/search',
             back.runSearchRnaQuantifications,
             'searchRnaQuantifiactions'),
            ('/expressionlevels/search',
             back.runSearchExpressionLevels,
             'searchExpressionLevels'),
            ('/phenotypes/search',
             back.runSearchPhenotypes,
             'searchPhenotypes'),
            ('/featurephenotypeassociations/search',
             back.runSearchGenotypePhenotypes,
             'searchPhenotypeAssociations'),
            ('/phenotypeassociationsets/search',
             back.runSearchPhenotypeAssociationSets,
             'searchPhenotypeAssociationSets')]

        idList = [
            ('/references/<no(search):id>',
             back.runGetReference,
             'getReference',
             '/references/<id>'),
            ('/referencesets/<no(search):id>',
             back.runGetReferenceSet,
             'getReferenceSet',
             '/referencesets/<id>'),
            ('/biosamples/<no(search):id>',
             back.runGetBiosample,
             'getBiosample',
             '/biosamples/<id>'),
            ('/individuals/<no(search):id>',
             back.runGetIndividual,
             'getIndvidual',
             '/individuals/<id>'),
            ('/variantsets/<no(search):id>',
             back.runGetVariantSet,
             'getVariantSet',
             '/variantsets/<id>'),
            ('/variants/<no(search):id>',
             back.runGetVariant,
             'getVariant',
             '/variants/<id>'),
            ('/readgroupsets/<no(search):id>',
             back.runGetReadGroupSet,
             'getReadGroupSet',
             '/readgroupsets/<id>'),
            ('/readgroups/<id>',
             back.runGetReadGroup,
             'getReadGroup',
             "/readgroups/<id>"),
            ('/callsets/<no(search):id>',
             back.runGetCallSet,
             'getCallSet',
             '/callsets/<id>'),
            ('/featuresets/<no(search):id>',
             back.runGetFeatureSet,
             'getFeatureSet',
             '/featuresets/<id>'),
            ('/features/<no(search):id>',
             back.runGetFeature,
             'getFeature',
             '/features/<id>'),
            ('/continuoussets/<no(search):id>',
             back.runGetContinuousSet,
             'getContinuousSet',
             '/continuoussets/<id>'),
            ('/rnaquantificationsets/<no(search):id>',
             back.runGetRnaQuantificationSet,
             'getRnaQuantificationSet',
             '/rnaquantificationsets/<id>'),
            ('/rnaquantifications/<no(search):id>',
             back.runGetRnaQuantification,
             'getRnaQuantification',
             '/rnaquantifications/<id>'),
            ('/expressionlevels/<no(search):id>',
             back.runGetExpressionLevel,
             'getExpressionLevel',
             '/expressionlevels/<id>'),
            ('/datasets/<no(search):id>',
             back.runGetDataset,
             'getDataset',
             '/datasets/<id>'),
            ('/variantannotationsets/<no(search):id>',
             back.runGetVariantAnnotationSet,
             'getVariantAnnotationSet',
             '/variantAnnotationSet/<id>')]

        tokenMethod = ("POST", tokenList)
        idMethod = ("GET", idList)

        methodList = [idMethod, tokenMethod]
        for item in methodList:
            if item[0] == "GET":
                self.getListProcess(item[1])
            elif item[0] == "POST":
                self.postListProcess(item[1])
            else:
                raise ValueError("Unknown method {}".format(item[0]))

    def bindEndpoint(self, endpointFunc, methodHandler):
        transFunc = functools.partial(methodHandler,
                                      flaskRequest=flask.request,
                                      endpoint=endpointFunc)
        return transFunc

    def postListProcess(self, iList):
        for item in iList:
            authFunc = frontAuth.requires_token(item[1], self.app, self.oidc)
            secureFunc = self.requires_auth(self.oidc.require_login(authFunc))
            boundFunc = self.bindEndpoint(secureFunc,
                                          router.handleFlaskPostRequest)
            self.dispRoute(item[0], boundFunc, item[2], postMethod=True)

    def getListProcess(self, iList):
        for item in iList:
            authFunc = frontAuth.requires_token(item[1], self.app, self.oidc)
            secureFunc = self.requires_auth(self.oidc.require_login(authFunc))
            boundFunc = self.bindEndpoint(secureFunc,
                                          router.handleFlaskGetRequest)
            self.dispRoute(item[0], boundFunc, item[2], pathDisplay=item[3])
