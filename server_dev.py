"""
Simple shim for running the server program during development.
"""

import dev_glue  # NOQA
import candig.server.cli.server as cli_server

if __name__ == "__main__":
    cli_server.server_main()
