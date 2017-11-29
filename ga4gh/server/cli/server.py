"""
Server cli
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests

import ga4gh.server.cli as cli
import ga4gh.server.frontend.core as core

import ga4gh.common.cli as common_cli


def addServerOptions(parser):
    parser.add_argument(
        "--port", "-P", default=8000, type=int,
        help="The port to listen on")
    parser.add_argument(
        "--host", "-H", default="127.0.0.1",
        help="The server host string; use 0.0.0.0 to allow all connections.")
    parser.add_argument(
        "--config", "-c", default='DevelopmentConfig', type=str,
        help="The configuration to use")
    parser.add_argument(
        "--config-file", "-f", type=str, default=None,
        help="The configuration file to use")
    parser.add_argument(
        "--tls", "-t", action="store_true", default=False,
        help="Start in TLS (https) mode.")
    parser.add_argument(
        "--dont-use-reloader", default=False, action="store_true",
        help="Don't use the flask reloader")
    cli.addVersionArgument(parser)
    cli.addDisableUrllibWarningsArgument(parser)


def getServerParser():
    parser = common_cli.createArgumentParser("GA4GH reference server")
    addServerOptions(parser)
    return parser


def server_main(args=None):
    parser = getServerParser()
    parsedArgs = parser.parse_args(args)
    if parsedArgs.disable_urllib_warnings:
        requests.packages.urllib3.disable_warnings()
    core.coreInstance.setup(parsedArgs.config_file, parsedArgs.config, parsedArgs.port)
    #configurer.configure(
    #    parsedArgs.config_file, parsedArgs.config, parsedArgs.port)
    sslContext = None
    app = core.coreInstance.getApp()
    if parsedArgs.tls or ("OIDC_PROVIDER" in app.config):
        sslContext = "adhoc"
    app.run(
        host=parsedArgs.host, port=parsedArgs.port,
        use_reloader=not parsedArgs.dont_use_reloader,
        ssl_context=sslContext)
