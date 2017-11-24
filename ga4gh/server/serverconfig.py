"""
Sets of configuration values for a GA4GH server.
Any of these values may be overridden by a file on the path
given by the environment variable GA4GH_CONFIGURATION.
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import yaml 
import pkg_resources

def importYamlConfig(config):
    """
    A function that returns the frontend and server configuration
    as a dictionary.
    """
    stream = file(config, 'r')
    config = yaml.load(stream)
    return config


class BaseConfig(object):
    """
    Simplest default server configuration.
    """
    pathLocation = '/'.join(('.', 'config', 'oidc_auth_config.yml'))
    configPath = pkg_resources.resource_filename(__name__, pathLocation)
    config = importYamlConfig(config=configPath)

    serverConfig = config["server"]

    MAX_CONTENT_LENGTH = serverConfig["MAX_CONTENT_LENGTH"]
    MAX_RESPONSE_LENGTH = serverConfig["MAX_RESPONSE_LENGTH"]
    REQUEST_VALIDATION = serverConfig["REQUEST_VALIDATION"]
    DEFAULT_PAGE_SIZE = serverConfig["DEFAULT_PAGE_SIZE"]
    DATA_SOURCE = serverConfig["DATA_SOURCE"]
    DEBUG = serverConfig["DEBUG"]
    INITIAL_PEERS = serverConfig["INITIAL_PEERS"]
    LANDING_MESSAGE_HTML = serverConfig["LANDING_MESSAGE_HTML"]
    FILE_HANDLE_CACHE_MAX_SIZE = serverConfig["FILE_HANDLE_CACHE_MAX_SIZE"]

    # Options for the simulated backend.
    SIMULATED_BACKEND_RANDOM_SEED = serverConfig["SIMULATED_BACKEND_RANDOM_SEED"]
    SIMULATED_BACKEND_NUM_CALLS = serverConfig["SIMULATED_BACKEND_NUM_CALLS"]
    SIMULATED_BACKEND_VARIANT_DENSITY = serverConfig["SIMULATED_BACKEND_VARIANT_DENSITY"]
    SIMULATED_BACKEND_NUM_VARIANT_SETS = serverConfig["SIMULATED_BACKEND_NUM_VARIANT_SETS"]
    SIMULATED_BACKEND_NUM_REFERENCE_SETS = serverConfig["SIMULATED_BACKEND_NUM_REFERENCE_SETS"]
    SIMULATED_BACKEND_NUM_REFERENCES_PER_REFERENCE_SET = serverConfig["SIMULATED_BACKEND_NUM_REFERENCES_PER_REFERENCE_SET"]
    SIMULATED_BACKEND_NUM_ALIGNMENTS_PER_READ_GROUP = serverConfig["SIMULATED_BACKEND_NUM_ALIGNMENTS_PER_READ_GROUP"]
    SIMULATED_BACKEND_NUM_READ_GROUPS_PER_READ_GROUP_SET = serverConfig["SIMULATED_BACKEND_NUM_READ_GROUPS_PER_READ_GROUP_SET"]
    SIMULATED_BACKEND_NUM_PHENOTYPE_ASSOCIATIONS = serverConfig["SIMULATED_BACKEND_NUM_PHENOTYPE_ASSOCIATIONS"]
    SIMULATED_BACKEND_NUM_PHENOTYPE_ASSOCIATION_SETS = serverConfig["SIMULATED_BACKEND_NUM_PHENOTYPE_ASSOCIATION_SETS"]
    SIMULATED_BACKEND_NUM_RNA_QUANTIFICATION_SETS = serverConfig["SIMULATED_BACKEND_NUM_RNA_QUANTIFICATION_SETS"]
    SIMULATED_BACKEND_NUM_EXPRESSION_LEVELS_PER_RNA_QUANT_SET = serverConfig["SIMULATED_BACKEND_NUM_EXPRESSION_LEVELS_PER_RNA_QUANT_SET"]


class ComplianceConfig(BaseConfig):
    """
    Configuration used for compliance testing.
    """
    pass


class DevelopmentConfig(BaseConfig):
    """
    Configuration used for development.
    """
    # DATA_SOURCE = "ga4gh-example-data/registry.db"
    DATA_SOURCE = "/srv/ga4gh-compliance-data/registry.db"
    DEBUG = True


class LocalOidConfig(DevelopmentConfig):
    """
    Configuration used for developing against a local OIDC server
    """
    SECRET_KEY = "super_secret"
    OIDC_PROVIDER = "https://opennet-33-237.uhnres.utoronto.ca:8443"


class KeycloakOidConfig(DevelopmentConfig):
    """
    Configuration used for OIDC with Keycloak server
    """
    SECRET_KEY = "super_secret"  # Unsure what this does, but it is needed.
    KEYCLOAK = True


class SimulatedConfig(BaseConfig):
    """
    A configuration that uses simulated backing for testing.
    """
    DATA_SOURCE = "simulated://"
    DEBUG = True
    REQUEST_VALIDATION = True


class ProductionConfig(BaseConfig):
    """
    Configuration that is a good basis for production deployments.
    """
    REQUEST_VALIDATION = True
    # We should complain loudly if data source is not set, rather than
    # mysteriously serve no data.
    DATA_SOURCE = None


class GoogleOidcConfig(ProductionConfig):
    """
    Configuration that is a good basis for production deployments using
    Google as the authentication provider.
    """
    SECRET_KEY = "super_secret"
    OIDC_PROVIDER = "https://accounts.google.com"
    OIDC_REDIRECT_URI = "https://localhost/oauth2callback"
    OIDC_CLIENT_ID = "XXX"
    OIDC_CLIENT_SECRET = "XXX"


class TestAuth0Config(DevelopmentConfig):
    """
    Auth0 configuration
    """
    AUTH0_ENABLED = True
    SECRET_KEY = "super_secret"
    AUTH0_SCOPES = "openid email"
    AUTH0_CALLBACK_URL = "http://localhost:8000/callback"
    AUTH0_HOST = "david4096.auth0.com"
    AUTH0_CLIENT_ID = "r99hdj5hhkazgePB5oMYK9Sv4NaUwwYp"
    AUTH0_CLIENT_SECRET = "KeV2tMyGaSgLeOhpoGs_XLH65Tfw43yBjT8" \
    "DIpaTxXAKmd_bguJwXA6T7D0iYfgB"
    AUTH0_AUTHORIZED_EMAILS = "davidcs@ucsc.edu,your@email.com"


class TestConfig(BaseConfig):
    """
    Configuration used in frontend unit tests.
    """
    TESTING = True
    REQUEST_VALIDATION = True


class TestOidcConfig(TestConfig):
    SECRET_KEY = "super_secret"
    OIDC_PROVIDER = "http://localhost:8080/auth/realms/demo"
    OIDC_CLIENT_ID = "demo"
    OIDC_CLIENT_SECRET = "xxx"
    OIDC_AUTHZ_ENDPOINT = "http://localhost:8080/auth/realms/" \
    "demo/protocol/openid-connect/auth"
    OIDC_TOKEN_ENDPOINT = "http://localhost:8080/auth/realms/" \
    "demo/protocol/openid-connect/token"
    OIDC_TOKEN_REV_ENDPOINT = "http://localhost:8080/auth/realms/" \
    "demo/protocol/openid-connect/token/introspect"


class FlaskDefaultConfig(object):
    """
    The default values for the Flask config.
    Only used in testing.
    """
    APPLICATION_ROOT = None
    DEBUG = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    JSON_AS_ASCII = True
    JSON_SORT_KEYS = True
    LOGGER_NAME = 'ga4gh.frontend'
    MAX_CONTENT_LENGTH = None
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(31)
    PREFERRED_URL_SCHEME = 'http'
    PRESERVE_CONTEXT_ON_EXCEPTION = None
    PROPAGATE_EXCEPTIONS = None
    SECRET_KEY = None
    SEND_FILE_MAX_AGE_DEFAULT = 43200
    SERVER_NAME = None
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_PATH = None
    SESSION_COOKIE_SECURE = False
    TESTING = False
    TRAP_BAD_REQUEST_ERRORS = False
    TRAP_HTTP_EXCEPTIONS = False
    USE_X_SENDFILE = False
