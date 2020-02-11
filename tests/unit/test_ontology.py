"""
Ontology Parser Unit Test
"""

import unittest
from candig.server.ontology import OntologyValidator

class TestOntologyValidInput(unittest.TestCase):
    """
    This class includes some of the valid ontology input json
    """
    def testValidOntologyInput1(self):
        """
        This is a valid input, as a correctly-formatted date is provided for DUO:0000024
        """
        input = {"duo": [{"id": "DUO:0000018"}, {"id": "DUO:0000024", "modifier": "2022-01-01"}]}

        parser = OntologyValidator(input)

        self.assertTrue(parser.validate_duo())


class TestOntologyInvalidInput(unittest.TestCase):
    """
    This class includes invalid ontology input json
    """

    def testInvalidOntologyInput1(self):
        """
        This is an invalid input, as id DUO:0000002 is not supported.
        """
        input = {"duo": [{"id": "DUO:0000002"}]}

        parser = OntologyValidator(input)

        self.assertFalse(parser.validate_duo())
