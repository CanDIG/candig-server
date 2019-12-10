# CanDIG Server Style Guide

The code largely follows the guidelines of [PEP 8]
(<http://legacy.python.org/dev/peps/pep-0008>). Flake8 is used to lint the code.

## Naming
CamelCase is used.

## Length
Maximum length limit check (E501) is currently disabled.

## E251
Unexpected spaces around keyword / parameter equals (E251) check is currently disabled.
This is expected to be back in force in the future.

## Imports
Imports should be structured into the following groups:

1. Any standard library imports
2. Any third party library imports
3. Any package level imports from the current package
4. Any imports from other candig packages

This does not have any automated checks.
