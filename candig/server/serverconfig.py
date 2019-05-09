"""
Sets of configuration values for a GA4GH server.
Any of these values may be overridden by a file on the path
given by the environment variable GA4GH_CONFIGURATION.
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
# import socket


class BaseConfig(object):
    """
    Simplest default server configuration.
    """
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB
    MAX_RESPONSE_LENGTH = 1024 * 1024  # 1MB
    REQUEST_VALIDATION = True
    DEFAULT_PAGE_SIZE = 1800
    DATA_SOURCE = "empty://"

    # Options for the simulated backend.
    SIMULATED_BACKEND_RANDOM_SEED = 0
    SIMULATED_BACKEND_NUM_CALLS = 1
    SIMULATED_BACKEND_VARIANT_DENSITY = 0.5
    SIMULATED_BACKEND_NUM_VARIANT_SETS = 1
    SIMULATED_BACKEND_NUM_REFERENCE_SETS = 1
    SIMULATED_BACKEND_NUM_REFERENCES_PER_REFERENCE_SET = 1
    SIMULATED_BACKEND_NUM_ALIGNMENTS_PER_READ_GROUP = 2
    SIMULATED_BACKEND_NUM_READ_GROUPS_PER_READ_GROUP_SET = 2
    SIMULATED_BACKEND_NUM_PHENOTYPE_ASSOCIATIONS = 2
    SIMULATED_BACKEND_NUM_PHENOTYPE_ASSOCIATION_SETS = 2
    SIMULATED_BACKEND_NUM_RNA_QUANTIFICATION_SETS = 2
    SIMULATED_BACKEND_NUM_EXPRESSION_LEVELS_PER_RNA_QUANT_SET = 2

    FILE_HANDLE_CACHE_MAX_SIZE = 50

    LANDING_MESSAGE_HTML = "landing_message.html"


class ComplianceConfig(BaseConfig):
    """
    Configuration used for compliance testing.
    """
    DATA_SOURCE = "ga4gh-compliance-data/registry.db"
    DEBUG = True
    DP_EPSILON = None


class DevelopmentConfig(BaseConfig):
    """
    Configuration used for development.
    """
    DATA_SOURCE = "ga4gh-example-data/registry.db"
    # DATA_SOURCE = "1000genomes_partition/registry.db"
    DEBUG = True
    # INITIAL_PEERS =
    #   "/srv/candig/server/candig/server/templates/initial_peers.txt"
    INITIAL_PEERS = "candig/server/templates/initial_peers.txt"
    DP_EPSILON = None


class LocalOidConfig(DevelopmentConfig):
    """
    Configuration used for developing against a local OIDC server
    """
    SECRET_KEY = "key"
    OIDC_PROVIDER = "http://localhost:8080"


class KeycloakOidConfig(DevelopmentConfig):
    """
    Configuration used for OIDC with Keycloak server
    """
    # Unsure what this does, but it is needed.
    SECRET_KEY = "key"
    KEYCLOAK = True


class SimulatedConfig(BaseConfig):
    """
    A configuration that uses simulated backing for testing.
    """
    DATA_SOURCE = "simulated://"
    DEBUG = True
    REQUEST_VALIDATION = True
    DP_EPSILON = None


class ProductionConfig(BaseConfig):
    """
    Configuration that is a good basis for production deployments.
    """
    REQUEST_VALIDATION = True
    # We should complain loudly if data source is not set, rather than
    # mysteriously serve no data.
    DATA_SOURCE = None
    DP_EPSILON = None


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
    AUTH0_CLIENT_SECRET = (
        "KeV2tMyGaSgLeOhpoGs_XLH65Tfw43yBjT8DIpaTxXAKmd_bg",
        "uJwXA6T7D0iYfgB")
    AUTH0_AUTHORIZED_EMAILS = "davidcs@ucsc.edu,your@email.com"


class TestConfig(BaseConfig):
    """
    Configuration used in frontend unit tests.
    """
    TESTING = True
    REQUEST_VALIDATION = True
    TYK_ENABLED = False
    TYK_SERVER = TYK_LISTEN_PATH = KC_SERVER = KC_LOGIN_REDIRECT = ''
    DP_EPSILON = None


class TestOidcConfig(TestConfig):
    SECRET_KEY = "super_secret"
    OIDC_PROVIDER = "http://localhost:8080/auth/realms/demo"
    OIDC_CLIENT_ID = "demo"
    OIDC_CLIENT_SECRET = "xxx"
    OIDC_AUTHZ_ENDPOINT = (
        "http://localhost:8080/auth/realms/demo/protocol/",
        "openid-connect/auth")
    OIDC_TOKEN_ENDPOINT = (
        "http://localhost:8080/auth/realms/demo/protocol/",
        "openid-connect/token")
    OIDC_TOKEN_REV_ENDPOINT = (
        "http://localhost:8080/auth/realms/demo/",
        "protocol/openid-connect/token/introspect")


class FlaskDefaultConfig(object):
    """
    The default values for the Flask config.
    Only used in testing.
    """
    APPLICATION_ROOT = '/'
    DEBUG = False
    EXPLAIN_TEMPLATE_LOADING = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    JSON_AS_ASCII = True
    JSON_SORT_KEYS = True
    LOGGER_NAME = 'candig.frontend'
    LOGGER_HANDLER_POLICY = None
    MAX_CONTENT_LENGTH = None
    MAX_COOKIE_SIZE = 4093
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
    SESSION_COOKIE_SAMESITE = None
    SESSION_REFRESH_EACH_REQUEST = None
    TESTING = False
    TEMPLATES_AUTO_RELOAD = None
    TRAP_BAD_REQUEST_ERRORS = False
    TRAP_HTTP_EXCEPTIONS = False
    USE_X_SENDFILE = False


class TykConfig(KeycloakOidConfig):
    """
    Configuration to use when forwarding requests through the API gateway.
    This also requires that keycloak config is being used and is set up properly.

    To start a dev flask server using this config add in launch option, -c TykConfig
    """
    ACCESS_LIST = "access_list.txt"

    TYK_ENABLED = True
    TYK_SERVER = 'http://ga4ghdev01.bcgsc.ca:8008'
    TYK_LISTEN_PATH = '/candig-dev'

    # Keycloak settings with redirection through tyk
    KC_REALM = 'CanDIG'
    KC_SERVER = 'http://ga4ghdev01.bcgsc.ca:8080'
    KC_SCOPE = 'openid+email'
    KC_RTYPE = 'code'
    KC_CLIENT_ID = 'ga4gh'
    KC_RMODE = 'form_post'
    KC_REDIRECT = TYK_SERVER + TYK_LISTEN_PATH + '/login_oidc'
    KC_LOGIN_REDIRECT = '/auth/realms/{0}/protocol/openid-connect/auth?scope={1}&response_type={2}&client_id={3}&response_mode={4}&redirect_uri={5}'.format(
        KC_REALM, KC_SCOPE, KC_RTYPE, KC_CLIENT_ID, KC_RMODE, KC_REDIRECT
    )


class NoAuth(DevelopmentConfig):
    """
    Configuration to use when not using API gateway to forward requests.
    This means requests do not need to be authenticated. For dev only.

    To start a dev flask server using this config add in launch option, -c NoAuth
    """

    TYK_ENABLED = False
    TYK_SERVER = TYK_LISTEN_PATH = KC_SERVER = KC_LOGIN_REDIRECT = ''
