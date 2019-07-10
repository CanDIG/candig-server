"""
Functionality common to cli modules
"""

import candig.server

import candig.schemas.protocol as protocol


def addVersionArgument(parser):
    # TODO argparse strips newlines from version output
    versionString = (
        "CanDIG Server Version {}\n"
        "(Protocol Version {})".format(
            candig.server.__version__, protocol.version))
    parser.add_argument(
        "--version", version=versionString, action="version")


def addDisableUrllibWarningsArgument(parser):
    parser.add_argument(
        "--disable-urllib-warnings", default=False, action="store_true",
        help="Disable urllib3 warnings")
