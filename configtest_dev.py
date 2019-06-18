"""
Simple shim for running the configuration testing program during development.
"""

import dev_glue  # NOQA
import candig.server.cli.configtest as cli_configtest

if __name__ == "__main__":
    cli_configtest.configtest_main()
