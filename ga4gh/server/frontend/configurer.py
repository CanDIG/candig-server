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
import requests
from yaml import load
import pkg_resources

from werkzeug.contrib.cache import FileSystemCache

import flask.ext.cors as cors

import oic
import oic.oic.message as message

import ga4gh.server.backend as backend
import ga4gh.server.datamodel as datamodel
import ga4gh.server.exceptions as exceptions
import ga4gh.server.datarepo as datarepo
import ga4gh.server.auth as auth
import ga4gh.server.network as network


class configurer():

    def __init__(self, app):
        self.app = app

    def import_yaml_config(self, config):
        """
        A function that returns the frontend and server configuration
        as a dictionary.
        """
        stream = file(config, 'r')
        config = load(stream)
        return config

    def loadConfig(self, configPath):
        """
        Loads the configuration file into the app
        """
        configStream = self.import_yaml_config(config=configPath)
        self.app.config.update(configStream)

    def reset(self):
        """
        Resets the flask app; used in testing
        """
        self.app.config.clear()
        configStr = 'ga4gh.server.serverconfig:FlaskDefaultConfig'
        self.app.config.from_object(configStr)

    def configBackendSimulated(self):
        """
        Configures a simulated backend
        """
        # Ignore the query string
        config = self.app.config

        argDict = {
            "randomSeed": config[
                "SIMULATED_BACKEND_RANDOM_SEED"],
            "numCalls": config[
                "SIMULATED_BACKEND_NUM_CALLS"],
            "variantDensity": config[
                "SIMULATED_BACKEND_VARIANT_DENSITY"],
            "numVariantSets": config[
                "SIMULATED_BACKEND_NUM_VARIANT_SETS"],
            "numReferenceSets": config[
                "SIMULATED_BACKEND_NUM_REFERENCE_SETS"],
            "numReferencesPerReferenceSet": config[
                "SIMULATED_BACKEND_NUM_REFERENCES_PER_REFERENCE_SET"],
            "numAlignments": config[
                "SIMULATED_BACKEND_NUM_ALIGNMENTS_PER_READ_GROUP"],
            "numReadGroupsPerReadGroupSet": config[
                "SIMULATED_BACKEND_NUM_READ_GROUPS_PER_READ_GROUP_SET"],
            "numPhenotypeAssociations": config[
                "SIMULATED_BACKEND_NUM_PHENOTYPE_ASSOCIATIONS"],
            "numPhenotypeAssociationSets": config[
                "SIMULATED_BACKEND_NUM_PHENOTYPE_ASSOCIATION_SETS"],
            "numRnaQuantSets": config[
                "SIMULATED_BACKEND_NUM_RNA_QUANTIFICATION_SETS"],
            "numExpressionLevels": config[
                "SIMULATED_BACKEND_NUM_EXPRESSION_LEVELS_PER_RNA_QUANT_SET"]
        }
        dataRepository = datarepo.SimulatedDataRepository(**argDict)

        # dataRepository = datarepo.SimulatedDataRepository(
        #    randomSeed=randomSeed, numCalls=numCalls,
        #    variantDensity=variantDensity, numVariantSets=numVariantSets,
        #    numReferenceSets=numReferenceSets,
        #    numReferencesPerReferenceSet=numReferencesPerReferenceSet,
        #    numReadGroupsPerReadGroupSet=numReadGroupsPerReadGroupSet,
        #    numAlignments=numAlignmentsPerReadGroup,
        #    numPhenotypeAssociations=numPhenotypeAssociations,
        #    numPhenotypeAssociationSets=numPhenotypeAssociationSets,
        #    numRnaQuantSets=numRnaQuantSets,
        #    numExpressionLevels=numExpressionLevels)

        return dataRepository

    def configBackendFile(self, dataSource):
        """
        Configures the backend based on a file
        """
        path = os.path.join(dataSource.netloc, dataSource.path)

        dataRepository = datarepo.SqlDataRepository(path)
        dataRepository.open(datarepo.MODE_READ)

        return dataRepository

    def _configure_backend(self):
        """
        Allocates and configures the server backend
        based on the data source scheme

        The backend serves stored data and
        performs searches requested by the frontend

        We use URLs to specify the backend.
        Currently we have file:// URLs
        (or URLs with no scheme)
        for the SqlDataRepository,
        and special empty:// and simulated://
        URLs for empty or simulated data sources.

        A backend can be configured in one of three ways:

        1. From File
        2. Simulated
        3. Empty

        A scheme that does not match these will be
        raised as an error in the scheme

        Returns:

        backend theBackend - the backend instance for the GA4GH server
        """

        # get the data source
        dataSource = urlparse.urlparse(self.app.config["DATA_SOURCE"], "file")

        # get the data scheme
        scheme = dataSource.scheme

        # prepare the data repository based on the scheme
        if scheme == "simulated":
            dataRepository = self.configBackendSimulated()
        elif scheme == "empty":
            dataRepository = datarepo.EmptyDataRepository()
        elif scheme == "file":
            dataRepository = self.configBackendFile(dataSource)
        else:
            # throw an error if an
            # unrecognized scheme is used
            raise exceptions.ConfigurationException(
                "Unsupported data source scheme: " + dataSource.scheme)

        # create the backend based on the repository
        theBackend = backend.Backend(dataRepository)

        # configure the backend
        theBackend.setRequestValidation(self.app.config["REQUEST_VALIDATION"])
        theBackend.setDefaultPageSize(self.app.config["DEFAULT_PAGE_SIZE"])
        theBackend.setMaxResponseLength(self.app.config["MAX_RESPONSE_LENGTH"])

        return theBackend

    def networkConfig(self, port):
        """
        Initialize the network and authentication protocols
        """
        config = self.app.config

        # Peer service initialization
        network.initialize(
            config.get('INITIAL_PEERS'),
            self.app.backend.getDataRepository(),
            self.app.logger)
        self.app.oidcClient = None
        self.app.myPort = port

        if config.get('AUTH0_ENABLED'):
            emails = config.get('AUTH0_AUTHORIZED_EMAILS', '').split(',')
            [auth.authorize_email(e, self.app.cache) for e in emails]

        if "OIDC_PROVIDER" in config:
            self.oidcConfig()

        if "KEYCLOAK" in config:
            self.keycloakConfig()

    def cacheConfig(self):
        """
        Configures the server filesystem cache and its location
        Default: /tmp/ga4gh
        """
        if self.app.config.get('CACHE_DIRECTORY'):
            self.app.cache_dir = self.app.config['CACHE_DIRECTORY']
        else:
            self.app.cache_dir = '/tmp/ga4gh'
        self.app.cache = FileSystemCache(
            self.app.cache_dir, threshold=5000, default_timeout=600, mode=384)

    def oidcConfig(self):
        # The oic client. If we're testing, we don't want to verify
        # SSL certificates
        config = self.app.config
        oidcCli = self.app.oidcClient
        self.app.oidcClient = oic.oic.Client(
            verify_ssl=('TESTING' not in config))
        try:
            oidcCli.provider_config(config['OIDC_PROVIDER'])
        except requests.exceptions.ConnectionError:
            configResponse = message.ProviderConfigurationResponse(
                issuer=config['OIDC_PROVIDER'],
                authorization_endpoint=config['OIDC_AUTHZ_ENDPOINT'],
                token_endpoint=config['OIDC_TOKEN_ENDPOINT'],
                revocation_endpoint=config['OIDC_TOKEN_REV_ENDPOINT'])
            oidcCli.handle_provider_config(configResponse,
                                           config['OIDC_PROVIDER'])

        # The redirect URI comes from the configuration.
        # If we are testing, then we allow the automatic creation of a
        # redirect uri if none is configured
        redirectUri = config.get('OIDC_REDIRECT_URI')
        if redirectUri is None:
            redirectUri = 'https://{0}:{1}/oauth2callback'.format(
                socket.gethostname(), self.app.myPort)
        self.app.oidcClient.redirect_uris = [redirectUri]
        if redirectUri is []:
            raise exceptions.ConfigurationException(
                'OIDC configuration requires a redirect uri')
        print(redirectUri)
        # We only support dynamic registration while testing.
        if ('registration_endpoint' in self.app.oidcClient.provider_info):
            self.app.oidcClient.register(
                self.app.oidcClient.provider_info["registration_endpoint"],
                redirect_uris=[redirectUri])
        else:
            response = message.RegistrationResponse(
                client_id=config['OIDC_CLIENT_ID'],
                client_secret=config['OIDC_CLIENT_SECRET'],
                redirect_uris=[redirectUri],
                verify_ssl=False)
            self.app.oidcClient.store_registration_info(response)

    def keycloakConfig(self):
        """
        This is for the configuration of the Keycloak Server
        added by Kevin Chan on June 12, 2017
        Configuration using the requests library.
        I left this here for your reference to
        familiarize yourself with the Authorization code flow
        Makes a request to get the configuration,
        and stores all the endpoints/id/secrets needed
        """
        # app.oidcClient = Client(client_authn_method=CLIENT_AUTHN_METHOD)
        # endpoints = requests.get(app.config["WELL_KNOWN_CONFIG"]).json()
        # opInfo = message.ProviderConfigurationResponse(
        #    issuer=endpoints["issuer"],
        #    authorization_endpoint=endpoints["authorization_endpoint"],
        #    token_endpoint=endpoints["token_endpoint"],
        #    introspect_endpoint=endpoints["token_introspection_endpoint"],
        #    user_endpoint= endpoints["userinfo_endpoint"],
        #    session_endpoint=endpoints["end_session_endpoint"],
        #    jwks_uri= endpoints["jwks_uri"])
        # app.oidcClient.provider_info = opInfo
        # app.oidcClient.client_id = app.config['CLIENT_ID']
        # app.oidcClient.client_secret = app.config["CLIENT_SECRET"]

        # For configuration of your server, change the host.
        # redirectUri = 'http://{0}:{1}/keycallback'.format(
        #        socket.gethostbyname(socket.gethostname()), app.myPort)
        # app.oidcClient.redirect_uris = [redirectUri]
        pass

    def configure(self, configFile=None, baseConfig="ProductionConfig",
                  port=8000, extraConfig={}):
        """
        Entrypoint for frontend configuration

        Called by the frontend core class to configure the frontend:

        - Flask frontend application configuration
          - This is held by the flask.app singleton
        - Backend configuration
          - The backend is responsible for fetching
            data from the databases held by the ga4gh repository
            so that they may be served by the frontend web API
        - Network configuration
        - Protocols configuration
        - Cache configuration

        Based on the configuration the server is being hosted with,
        it initalizes all the variables needed, and generates the
        redirect-url for the Auth and OIDC providers (if present).

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

        if configFile is None:
            # load the default configuration
            # if no configuration file has been given
            configPath = '/'.join(('config', 'oidc_config.yml'))
            configName = pkg_resources.resource_filename(__name__, configPath)
            self.loadConfig(configName)
        else:
            # load the specificied configuration file
            # the configFile is given as a command-line
            # argument
            self.loadConfig(configFile)

        # update the configuration with the
        # configuration dictionary parameter
        self.app.config.update(extraConfig.items())

        # Setup file handle cache max size
        datamodel.fileHandleCache.setMaxCacheSize(
            self.app.config["FILE_HANDLE_CACHE_MAX_SIZE"])

        # Setup CORS
        try:
            cors.CORS(self.app, allow_headers='Content-Type')
        except AssertionError:
            pass

        # configure the backend
        self.app.backend = self._configure_backend()

        # Set the secret key if OIDC_PROVIDER is used
        if self.app.config.get('SECRET_KEY'):
            self.app.secret_key = self.app.config['SECRET_KEY']
        elif self.app.config.get('OIDC_PROVIDER'):
            exceptMsg = 'OIDC configuration requires a secret key'
            raise exceptions.ConfigurationException(exceptMsg)

        # Set the server cache
        # By default, the cache is /tmp/ga4gh
        self.cacheConfig()

        # Initialize the network
        self.networkConfig(port)
