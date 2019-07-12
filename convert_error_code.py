"""
Simple script to decode exception error codes. This translates
the error code received by clients into an exception class.
"""

import argparse

import candig.server.exceptions as exceptions


def parseArgs():
    parser = argparse.ArgumentParser(
        description=(
            "Converts an error code received by a clients to the  "
            "corresponding exception class."))
    parser.add_argument(
        "errorCode", type=int,
        help="The errorCode value in a GAException object.")
    args = parser.parse_args()
    return args


def main():
    args = parseArgs()
    exceptionClass = exceptions.getExceptionClass(args.errorCode)
    print(args.errorCode, exceptionClass, sep="\t")


if __name__ == '__main__':
    main()
