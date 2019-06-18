"""
Glue for running server code during development

Import this module before using any other module that imports candig.server.
Otherwise, python will look for server in the installed candig package.

See __path__ documentation at:
    https://docs.python.org/2/tutorial/modules.html
"""

import candig
candig.__path__.append('candig')
