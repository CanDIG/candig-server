"""
The configuration class for the Flask frontend

Configures the following:
- Flask application 
- Backend
- Network
- Authentication
- Cache
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import socket
import urlparse
import json
import requests
import logging
from logging import StreamHandler
from yaml import load
import pkg_resources

from werkzeug.contrib.cache import FileSystemCache

import flask
import flask.ext.cors as cors

import oic
import oic.oic.message as message
from oauth2client.client import OAuth2Credentials

import ga4gh.server.backend as backend
import ga4gh.server.datamodel as datamodel
import ga4gh.server.exceptions as exceptions
import ga4gh.server.datarepo as datarepo
import ga4gh.server.auth as auth
import ga4gh.server.network as network
import ga4gh.schemas.protocol as protocol

# import ga4gh.server.frontend.flaskRouter as flaskRouter
# import ga4gh.server.frontend.auth as authRoute


class configurer():


    def import_yaml_config(self, config):
        """
        A function that returns the frontend and server configuration
        as a dictionary.
        """
        stream = file(config, 'r')
        config = load(stream)
        return config


    def loadConfig(self, app):
        """
        Loads the configuration file into the app
        """
        pathLocation = '/'.join(('config', 'oidc_auth_config.yml'))
        configPath = pkg_resources.resource_filename(__name__, pathLocation)
        configStream = self.import_yaml_config(config=configPath)
        app.config.update(configStream)


    def reset(self):
        """
        Resets the flask app; used in testing
        """
        app.config.clear()
        configStr = 'ga4gh.server.serverconfig:FlaskDefaultConfig'
        app.config.from_object(configStr)


    def _configure_backend(self, app):
        """
        Allocates and configures the server backend

        The backend serves stored data and performs searches requested by the frontend   

        We use URLs to specify the backend. Currently we have file:// URLs (or
        URLs with no scheme) for the SqlDataRepository, and special empty:// and
        simulated:// URLs for empty or simulated data sources.
        """
        dataSource = urlparse.urlparse(app.config["DATA_SOURCE"], "file")

        if dataSource.scheme == "simulated":
            # Ignore the query string
            randomSeed = app.config["SIMULATED_BACKEND_RANDOM_SEED"]
            numCalls = app.config["SIMULATED_BACKEND_NUM_CALLS"]
            variantDensity = app.config["SIMULATED_BACKEND_VARIANT_DENSITY"]
            numVariantSets = app.config["SIMULATED_BACKEND_NUM_VARIANT_SETS"]
            numReferenceSets = app.config[
                "SIMULATED_BACKEND_NUM_REFERENCE_SETS"]
            numReferencesPerReferenceSet = app.config[
                "SIMULATED_BACKEND_NUM_REFERENCES_PER_REFERENCE_SET"]
            numAlignmentsPerReadGroup = app.config[
                "SIMULATED_BACKEND_NUM_ALIGNMENTS_PER_READ_GROUP"]
            numReadGroupsPerReadGroupSet = app.config[
                "SIMULATED_BACKEND_NUM_READ_GROUPS_PER_READ_GROUP_SET"]
            numPhenotypeAssociations = app.config[
                "SIMULATED_BACKEND_NUM_PHENOTYPE_ASSOCIATIONS"]
            numPhenotypeAssociationSets = app.config[
                "SIMULATED_BACKEND_NUM_PHENOTYPE_ASSOCIATION_SETS"]
            numRnaQuantSets = app.config[
                "SIMULATED_BACKEND_NUM_RNA_QUANTIFICATION_SETS"]
            numExpressionLevels = app.config[
                "SIMULATED_BACKEND_NUM_EXPRESSION_LEVELS_PER_RNA_QUANT_SET"]

            dataRepository = datarepo.SimulatedDataRepository(
                randomSeed=randomSeed, numCalls=numCalls,
                variantDensity=variantDensity, numVariantSets=numVariantSets,
                numReferenceSets=numReferenceSets,
                numReferencesPerReferenceSet=numReferencesPerReferenceSet,
                numReadGroupsPerReadGroupSet=numReadGroupsPerReadGroupSet,
                numAlignments=numAlignmentsPerReadGroup,
                numPhenotypeAssociations=numPhenotypeAssociations,
                numPhenotypeAssociationSets=numPhenotypeAssociationSets,
                numRnaQuantSets=numRnaQuantSets,
                numExpressionLevels=numExpressionLevels)
        elif dataSource.scheme == "empty":
            dataRepository = datarepo.EmptyDataRepository()
        elif dataSource.scheme == "file":
            path = os.path.join(dataSource.netloc, dataSource.path)
            dataRepository = datarepo.SqlDataRepository(path)
            dataRepository.open(datarepo.MODE_READ)
        else:
            raise exceptions.ConfigurationException(
                "Unsupported data source scheme: " + dataSource.scheme)
        theBackend = backend.Backend(dataRepository)
        theBackend.setRequestValidation(app.config["REQUEST_VALIDATION"])
        theBackend.setDefaultPageSize(app.config["DEFAULT_PAGE_SIZE"])
        theBackend.setMaxResponseLength(app.config["MAX_RESPONSE_LENGTH"])
        return theBackend


    def networkConfig(self, app, port):
        """
        Initialize the network and authentication protocols
        """

        # Peer service initialization
        network.initialize(
            app.config.get('INITIAL_PEERS'),
            app.backend.getDataRepository(),
            app.logger)
        app.oidcClient = None
        app.myPort = port

        if app.config.get('AUTH0_ENABLED'):
            emails = app.config.get('AUTH0_AUTHORIZED_EMAILS', '').split(',')
            [auth.authorize_email(e, app.cache) for e in emails]

        if "OIDC_PROVIDER" in app.config:
            self.oidcConfig(app)

        if "KEYCLOAK" in app.config:
            self.keycloakConfig(app)


    def cacheConfig(self, app):
        """
        Configures the server filesystem cache and its location
        Default: /tmp/ga4gh
        """
        if app.config.get('CACHE_DIRECTORY'):
            app.cache_dir = app.config['CACHE_DIRECTORY']
        else:
            app.cache_dir = '/tmp/ga4gh'
        app.cache = FileSystemCache(
            app.cache_dir, threshold=5000, default_timeout=600, mode=384)


    def oidcConfig(self, app):
        # The oic client. If we're testing, we don't want to verify
        # SSL certificates
        app.oidcClient = oic.oic.Client(
            verify_ssl=('TESTING' not in app.config))
        try:
            app.oidcClient.provider_config(app.config['OIDC_PROVIDER'])
        except requests.exceptions.ConnectionError:
            configResponse = message.ProviderConfigurationResponse(
                issuer=app.config['OIDC_PROVIDER'],
                authorization_endpoint=app.config['OIDC_AUTHZ_ENDPOINT'],
                token_endpoint=app.config['OIDC_TOKEN_ENDPOINT'],
                revocation_endpoint=app.config['OIDC_TOKEN_REV_ENDPOINT'])
            app.oidcClient.handle_provider_config(configResponse,
                                                  app.config['OIDC_PROVIDER'])

        # The redirect URI comes from the configuration.
        # If we are testing, then we allow the automatic creation of a
        # redirect uri if none is configured
        redirectUri = app.config.get('OIDC_REDIRECT_URI')
        if redirectUri is None:
            redirectUri = 'https://{0}:{1}/oauth2callback'.format(
                socket.gethostname(), app.myPort)
        app.oidcClient.redirect_uris = [redirectUri]
        if redirectUri is []:
            raise exceptions.ConfigurationException(
                'OIDC configuration requires a redirect uri')
        print(redirectUri)
        # We only support dynamic registration while testing.
        if ('registration_endpoint' in app.oidcClient.provider_info):
            app.oidcClient.register(
                app.oidcClient.provider_info["registration_endpoint"],
                redirect_uris=[redirectUri])
        else:
            response = message.RegistrationResponse(
                client_id=app.config['OIDC_CLIENT_ID'],
                client_secret=app.config['OIDC_CLIENT_SECRET'],
                redirect_uris=[redirectUri],
                verify_ssl=False)
            app.oidcClient.store_registration_info(response)


    def keycloakConfig(self, app):
        # This is for the configuration of the Keycloak Server
        # added by Kevin Chan on June 12, 2017
        # Configuration using the requests library.
        # I left this here for your reference to
        # familiarize yourself with the Authorization code flow
        # Makes a request to get the configuration,
        # and stores all the endpoints/id/secrets needed

        #app.oidcClient = Client(client_authn_method=CLIENT_AUTHN_METHOD)
        #endpoints = requests.get(app.config["WELL_KNOWN_CONFIG"]).json()
        #opInfo = message.ProviderConfigurationResponse(
        #    issuer=endpoints["issuer"],
        #    authorization_endpoint=endpoints["authorization_endpoint"],
        #    token_endpoint=endpoints["token_endpoint"],
        #    introspect_endpoint=endpoints["token_introspection_endpoint"],
        #    user_endpoint= endpoints["userinfo_endpoint"],
        #    session_endpoint=endpoints["end_session_endpoint"],
        #    jwks_uri= endpoints["jwks_uri"])
        #app.oidcClient.provider_info = opInfo
        #app.oidcClient.client_id = app.config['CLIENT_ID']
        #app.oidcClient.client_secret = app.config["CLIENT_SECRET"]

        #For configuration of your server, change the host.
        #redirectUri = 'http://{0}:{1}/keycallback'.format(
        #        socket.gethostbyname(socket.gethostname()), app.myPort)
        #app.oidcClient.redirect_uris = [redirectUri]
        pass

    def configure(self, app, configFile=None, baseConfig="ProductionConfig",
                  port=8000, extraConfig={}):
        """
        TODO Document this critical function! What does it do?
        What does it assume?

        Based on the configuration the server is being hosted with,
        it initalizes all the variables needed, and generates the
        redirect-url for the Auth and OIDC providers (if present).

        This function sets the configuration of the server

        By configuration, we mean explicitly:

        - Flask frontend application configuration 
          - This is held by the flask.app singleton
        - Backend configuration
          - The backend is responsible for fetching 
            data from the databases held by the ga4gh repository
            so that they may be served by the frontend web API
        - Network configuration
        - Protocols configuration
        - Cache configuration

        Parameters:

        configFile  - A configuration file to read and set the configuration
                      This is set by a command-line argument to ga4gh_server
                      By default, this is None, and the default configuration
                      file is used
                      This should really be updated to the default 

        baseConfig  - This could be the name of the class used to 
                      instantiate the configuration of the server
                      The possible classes that can be instantiated
                      are in serverconfig.py
                      This has been set to ProdictionConfig by default

        port        - The port on which the API web server listens
                      The default is 8000

        extraConfig - This may be a dictionary of additional
                      parameters to explictly set outside of the default
                      configuration or with the configuration file

        Returns: None
        """
        self.loadConfig(app)

        # use the configuration file if it has 
        # been given over the command-line
        if configFile is not None:
            app.config.from_pyfile(configFile)

        # update the configuration with the 
        # configuration dictionary parameter
        app.config.update(extraConfig.items())

        # Setup file handle cache max size
        datamodel.fileHandleCache.setMaxCacheSize(
            app.config["FILE_HANDLE_CACHE_MAX_SIZE"])

        # Setup CORS
        try:
            cors.CORS(app, allow_headers='Content-Type')
        except AssertionError:
            pass

        # configure the backend
        app.backend = self._configure_backend(app)

        # Set the secret key if OIDC_PROVIDER is used
        if app.config.get('SECRET_KEY'):
            app.secret_key = app.config['SECRET_KEY']
        elif app.config.get('OIDC_PROVIDER'):
            raise exceptions.ConfigurationException(
                'OIDC configuration requires a secret key')

        # Set the server cache
        # By default, the cache is /tmp/ga4gh
        self.cacheConfig(app)

        # Initialize the network
        self.networkConfig(app, port)

        # app.register_blueprint(flaskRouter)
        # app.register_blueprint(authRoute)
