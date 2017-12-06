"""
The Core class for the frontend

Contains the flask application singleton
Contains the authentication singleton

Composes and calls all other frontend modules
Entrypoint for the frontend
"""

import werkzeug

import flask
from flask.ext.oidc import OpenIDConnect

import ga4gh.server.frontend.configurer as configurer
import ga4gh.server.frontend.status as status

import ga4gh.server.frontend.routeFactory as routeFactory


class NoConverter(werkzeug.routing.BaseConverter):
    """
    A converter that allows the routing matching algorithm to not
    match on certain literal terms

    This is needed because if there are e.g. two routes:

    /callsets/search
    /callsets/<id>

    A request for /callsets/search will get routed to
    the second, which is not what we want.
    """
    def __init__(self, map, *items):
        werkzeug.routing.BaseConverter.__init__(self, map)
        self.items = items

    def to_python(self, value):
        if value in self.items:
            raise werkzeug.routing.ValidationError()
        return value


class core():
    """
    The core singleton which coordinates the frontend

    Behaves as the entrypoint for the frontend
    Initializes and coordinates all other frontend modules
    Stores the Flask application and the authentication modules
    """
    def setup(self, configFile=None, baseConfig="ProductionConfig",
              port=8000, extraConfig={}):

        # intialize the flask application
        self.app = flask.Flask(__name__)

        # create the URL list
        assert not hasattr(self.app, 'urls')
        self.app.urls = []

        # set the converters on the application
        self.app.url_map.converters['no'] = NoConverter

        # create the configurer
        self.configurer = configurer.configurer(self.app)

        # configure the flask server
        self.configurer.configure(configFile, baseConfig, port, extraConfig)

        # create the oidc authentication object
        self.oidc = OpenIDConnect(self.app)

        # Create the server status singleton
        self.status = self.app.serverStatus = status.ServerStatus(self.app)

        # create the API endpoints
        self.routeFactory = routeFactory.routeFactory(self.app, self.oidc)

    def getApp(self):
        return self.app

    def getOidc(self):
        return self.oidc

    def getConfigurer(self):
        return self.configurer

    def getStatus(self):
        return self.status


coreInstance = core()
