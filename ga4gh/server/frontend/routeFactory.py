
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import functools

import ga4gh.server.frontend.router as router
import ga4gh.server.auth as auth
import ga4gh.server.frontend.auth as frontAuth


class routeFactory:


    def __init__(self, app, oidc):
        self.oidc = oidc
        self.app = app
        self.requires_auth = auth.auth_decorator(self.app)
        self.register()


    def dispRoute(self, path, func, name, postMethod=False, pathDisplay=None):
        methods = None
        methodDisplay = None

        if postMethod:
            methodDisplay = 'POST'
            methods = ['POST', 'OPTIONS']
            #methods = 'POST'
        else:
            methodDisplay = 'GET'
            #methods = ['GET', 'OPTIONS']

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
        """
        transFunc = functools.partial(f, app=self.app)            
        return transFunc


    def register(self):

        #indexFunc = self.bindApp(router.index)
        callbackHandle = self.bindApp(router.callback_handling)
        robots = self.bindApp(router.robots)

        funcList = [('/login', 'login', frontAuth.login), 
                    ('/logout', 'logout', self.requires_auth(frontAuth.logout)), 
                    ('/keycallback', 'keycloakCallback', frontAuth.keycloakCallback),
                    ('/callback', 'callback', callbackHandle),
                    ('/favicon.ico', 'favicon', robots),
                    ('/robots.txt', 'robots.txt', robots)]

        for item in funcList:
            self.app.add_url_rule(item[0], item[1], item[2])

    
        secureList = [('/', 'index', router.index)]

        for item in secureList:
            secureFunc = self.oidc.require_login(frontAuth.requires_token(item[2], self.app))
            boundFunc = self.bindApp(secureFunc)
            self.app.add_url_rule(item[0], item[1], boundFunc)            


        self.app.add_url_rule('/oauth2callback', 'oidcCallback', frontAuth.oidcCallback, methods=['GET'])


        exceptList = [(Exception, router.handleException), (401, router.unauthorizedHandler), 
                      (404, router.pathNotFoundHandler), (405, router.methodNotAllowedHandler), 
                      (403, router.notAuthenticatedHandler)]

        for item in exceptList:
            boundFunc = self.bindApp(item[1])
            self.app.register_error_handler(item[0], boundFunc)


        bindList = [('/listreferencebases', router.listReferenceBases, 'listReferenceBases'),
                    ('/callsets/search', router.searchCallSets, 'searchCallSets'),
                    ('/readgroupsets/search', router.searchReadGroupSets, 'searchReadGroupSets'),
                    ('/reads/search', router.searchReads, 'searchReads'),
                    ('/referencesets/search', router.searchReferenceSets, 'searchReferenceSets'),          
                    ('/references/search', router.searchReferences, 'searchReferences'),
                    ('/variantsets/search', router.searchVariantSets, 'searchVariantSets'),
                    ('/variants/search', router.searchVariants, 'searchVariants'),
                    ('/variantannotations/search', router.searchVariantAnnotations, 'searchVariantAnnotations'),
                    ('/variantannotationsets/search', router.searchVariantAnnotationSets, 'searchAnnotationSets')]

        for item in bindList:
            boundFunc = self.bindApp(item[1])
            self.dispRoute(item[0], boundFunc, item[2], postMethod=True)


        secureRouteList = [('/info', router.getInfo, 'info')]

        for item in secureRouteList:
            secureFunc = self.requires_auth(self.oidc.require_login(item[1]))
            boundFunc = self.bindApp(secureFunc)
            self.dispRoute(item[0], boundFunc, item[2])

           
        tokenList = [
                     ('/datasets/search', router.searchDatasets, 'searchDatasets'),
                     ('/featuresets/search', router.searchFeatureSets, 'searchFeatureSets'),
                     ('/features/search', router.searchFeatures, 'searchFeatures'),
                     ('/continuoussets/search', router.searchContinuousSets, 'searchContinuousSets'),
                     ('/continuous/search', router.searchContinuous, 'searchContinuous'),
                     ('/biosamples/search', router.searchBiosamples, 'searchBiosamples'),
                     ('/individuals/search', router.searchIndividuals, 'searchIndividuals'),
                     ('/peers/list', router.listPeers, 'listPeers'),
                     ('/announce', router.announce, 'announce'),
                     ('/rnaquantificationsets/search', router.searchRnaQuantificationSets, 'searchRnaQuantificationSets'),
                     ('/rnaquantifications/search', router.searchRnaQuantifications, 'searchRnaQuantifiactions'),
                     ('/expressionlevels/search', router.searchExpressionLevels, 'searchExpressionLevels'),
                     ('/phenotypes/search', router.searchPhenotypes, 'searchPhenotypes'),
                     ('/featurephenotypeassociations/search', router.searchGenotypePhenotypes, 'searchPhenotypeAssociations'),
                     ('/phenotypeassociationsets/search', router.searchPhenotypeAssociationSets, 'searchPhenotypeAssociationSets')]

        for item in tokenList:
            secureFunc = self.requires_auth(self.oidc.require_login(frontAuth.requires_token(item[1], self.app)))
            boundFunc = self.bindApp(secureFunc)         
            self.dispRoute(item[0], boundFunc, item[2], postMethod=True)
    

        secureDispList = [('/references/<no(search):id>', router.getReference, 'getReference', '/references/<id>'),
                          ('/referencesets/<no(search):id>', router.getReferenceSet, 'getReferenceSet', '/referencesets/<id>'),
                          ('/biosamples/<no(search):id>', router.getBiosample, 'getBiosample','/biosamples/<id>'),
                          ('/individuals/<no(search):id>', router.getIndividual, 'getIndvidual', '/individuals/<id>'),
                          ('/variantsets/<no(search):id>', router.getVariantSet, 'getVariantSet', '/variantsets/<id>'),
                          ('/variants/<no(search):id>', router.getVariant, 'getVariant', '/variants/<id>'),
                          ('/readgroupsets/<no(search):id>', router.getReadGroupSet, 'getReadGroupSet', '/readgroupsets/<id>'),
                          ('/readgroups/<id>', router.getReadGroup, 'getReadGroup', "/readgroups/<id>"),
                          ('/callsets/<no(search):id>', router.getCallSet, 'getCallSet', '/callsets/<id>'),                         
                          ('/featuresets/<no(search):id>', router.getFeatureSet, 'getFeatureSet', '/featuresets/<id>'),
                          ('/features/<no(search):id>', router.getFeature, 'getFeature', '/features/<id>'),
                          ('/continuoussets/<no(search):id>', router.getContinuousSet, 'getContinuousSet', '/continuoussets/<id>'),
                          ('/rnaquantificationsets/<no(search):id>', router.getRnaQuantificationSet, 'getRnaQuantificationSet', '/rnaquantificationsets/<id>'),
                          ('/rnaquantifications/<no(search):id>', router.getRnaQuantification, 'getRnaQuantification', '/rnaquantifications/<id>'),
                          ('/expressionlevels/<no(search):id>', router.getExpressionLevel, 'getExpressionLevel', '/expressionlevels/<id>'),
                          ('/datasets/<no(search):id>', router.getDataset, 'getDataset', '/datasets/<id>'),
                          ('/variantannotationsets/<no(search):id>', router.getVariantAnnotationSet, 'getVariantAnnotationSet', '/variantAnnotationSet/<id>')]

        for item in secureDispList:
            secureFunc = self.requires_auth(self.oidc.require_login(frontAuth.requires_token(item[1], self.app)))
            boundFunc = self.bindApp(secureFunc)
            self.dispRoute(item[0], boundFunc, item[2], pathDisplay=item[3])
        


        #exceptFunc = self.bindApp(router.handleException)
        #unauthFunc = self.bindApp(router.unauthorizedHandler)
        #unfoundPath = self.bindApp(router.pathNotFoundHandler)
        #notAllowed = self.bindApp(router.methodNotAllowedHandler)
        #notAuth = self.bindApp(router.notAuthenticatedHandler)


        #searchVarSet = self.bindApp(router.getVariantSet)
        #searchPheno = self.bindApp(router.searchPhenotypes)
        #searchPhenoAssoc = self.bindApp(router.searchGenotypePhenotypes)
        #searchPhenoAssocSet = self.bindApp(router.searchPhenotypeAssociationSets)

        #getVarSet = self.bindApp(router.getVariantSet)
        #getVar = self.bindApp(router.getVariant)
        #getReadGrpSet = self.bindApp(router.getReadGroupSet)
        #getReadGrp = self.bindApp(router.getReadGroup)
        #getCallSet = self.bindApp(router.getCallSet)
        #getFeatSet = self.bindApp(router.getFeatureSet)
        #getFeat = self.bindApp(router.getFeature)
        #getContSet = self.bindApp(router.getContinuousSet)
        #getRnaQuantSet = self.bindApp(router.getRnaQuantificationSet)
        #getRnaQuant = self.bindApp(router.getRnaQuantificationSet)
        #getExprLvl = self.bindApp(router.getExpressionLevel)
        #getDataSet = self.bindApp(router.getDataset)
        #getVarAnnoSet = self.bindApp(router.getVariantAnnotationSet) 


        #self.app.add_url_rule('/login', 'login', frontAuth.login)
        #self.app.add_url_rule('/logout', 'logout', self.requires_auth(frontAuth.logout))
        #self.app.add_url_rule('/keycallback', 'keycloakCallback', frontAuth.keycloakCallback)

        #self.dispRoute('/info', info, 'info', postMethod=True)
        #self.dispRoute('/references/<id>', getRef, 'getReference', postMethod=True,)
        #self.dispRoute('/referencesets/<id>', getRefSet, 'getReferenceSet', postMethod=True)
        #self.dispRoute('/listreferencebases', listRefBase, 'listReferenceBases', postMethod=True)
        #self.dispRoute('/callsets/search', searchCallSet, 'searchCallSets', postMethod=True)
        #self.dispRoute('/readgroupsets/search', searchReadGrpSet, 'searchReadGroupSets', postMethod=True)
        #self.dispRoute('/reads/search', searchRead, 'searchReads', postMethod=True)

        #self.dispRoute('/referencesets/search', searchRefSet, 'searchReferenceSets', postMethod=True)
        #self.dispRoute('/references/search', searchRef, 'searchReferences', postMethod=True)
        #self.dispRoute('/variantsets/search', searchVarSet, 'searchVariantSets', postMethod=True)
        #self.dispRoute('/variants/search', searchVar, 'searchVariants', postMethod=True)
        #self.dispRoute('/variantannotationsets/search', searchVarAnnoSet, 'searchAnnotationSets', postMethod=True)
        #self.dispRoute('/variantannotations/search', searchVarAnno, 'searchVariantAnnotations', postMethod=True)
        #self.dispRoute('/datasets/search', searchDataSet, 'searchDatasets', postMethod=True)

        #self.app.register_error_handler(Exception, exceptFunc)
        #self.app.register_error_handler(401, unauthFunc)
        #self.app.register_error_handler(404, unfoundPath)
        #self.app.register_error_handler(405, notAllowed)
        #self.app.register_error_handler(403, notAuth)
        #self.app.add_url_rule('/', 'index', indexFunc)
        #self.app.add_url_rule('/callback', 'callback', callbackHandle)
        #self.app.add_url_rule('/favicon.ico', 'favicon', robots)
        #self.app.add_url_rule('/robots.txt', 'robots.txt', robots)

        #info = self.bindApp(router.getInfo)
        #getRef = self.bindApp(router.getReference)
        #getRefSet = self.bindApp(router.getReferenceSet)
        #listRefBase = self.bindApp(router.listReferenceBases)
        #searchCallSet = self.bindApp(router.searchCallSets)
        #searchReadGrpSet = self.bindApp(router.searchReadGroupSets)
        #searchRead = self.bindApp(router.searchReads)
        #searchRefSet = self.bindApp(router.searchReferenceSets)
        #searchRef = self.bindApp(router.searchReferences)
        #searchVarSet = self.bindApp(router.searchVariantSets)
        #searchVar = self.bindApp(router.searchVariants)
        #searchVarAnnoSet = self.bindApp(router.searchVariantAnnotationSets)
        #searchVarAnno = self.bindApp(router.searchVariantAnnotations)

        #searchFeatSet = self.bindApp(router.searchFeatureSets)
        #searchFeat = self.bindApp(router.searchFeatures)
        #searchContSet = self.bindApp(router.searchContinuousSets)
        #searchCont = self.bindApp(router.searchContinuous)
        #searchBio = self.bindApp(router.searchBiosamples)
        #searchInd = self.bindApp(router.searchIndividuals)
        #listPeer = self.bindApp(router.listPeers)
        #announce = self.bindApp(router.announce)
        #getBio = self.bindApp(router.getBiosample)
        #getInd = self.bindApp(router.getIndividual)
        #searchRnaQuantSet = self.bindApp(router.searchRnaQuantificationSets)
        #searchRnaQuant = self.bindApp(router.searchRnaQuantifications)
        #searchExprLvl = self.bindApp(router.searchExpressionLevels)

# class DisplayedRoute(object):
#    """
#    Registers that a route should be displayed on the html page
#    """
#    def __init__(self, path, app, func, postMethod=False, pathDisplay=None):
#        self.path = path
#        self.methods = None
#        if postMethod:
#            methodDisplay = 'POST'
#            self.methods = ['POST', 'OPTIONS']
#        else:
#            methodDisplay = 'GET'
#        if pathDisplay is None:
#            pathDisplay = path
#        app.urls.append((methodDisplay, pathDisplay))
#        self.__call__(func, app)
# 
#    def __call__(self, func, app):
#        if self.methods is None:
#            app.add_url_rule(self.path, func.func_name, func)
#        else:
#            app.add_url_rule(
#                self.path, func.func_name, func, methods=self.methods)
#
#        @functools.wraps(func)
#        def wrapper(*args, **kwargs):
#            result = func(*args, **kwargs)
#            return result
#        return wrapper
