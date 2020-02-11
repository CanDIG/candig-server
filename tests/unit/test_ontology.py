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
        This is a valid input, as a correctly-formatted date is provided 
        for DUO:0000024
        """
        sample = {"duo": [{"id": "DUO:0000018"}, {"id": "DUO:0000024", "modifier": "2022-01-01"}]}

        parser = OntologyValidator(sample)

        self.assertTrue(parser.validate_duo())

    def testValidOntologyInput2(self):
        """
        This unit test loops through every valid Duo Term except 
        'DUO:0000024', which is covered in testValidOntologyInput1
        """
        listOfValidDuoIds = [
            "DUO:0000001", "DUO:0000004", "DUO:0000005",
            "DUO:0000006", "DUO:0000007", "DUO:0000011", 
            "DUO:0000012", "DUO:0000014", "DUO:0000015", 
            "DUO:0000016", "DUO:0000017", "DUO:0000018", 
            "DUO:0000019", "DUO:0000020", "DUO:0000021", 
            "DUO:0000026", "DUO:0000027", "DUO:0000028",
            "DUO:0000029", "DUO:0000042"
        ]

        for term in listOfValidDuoIds:

            sample = {"duo": [{"id": term}]}

            parser = OntologyValidator(sample)

            self.assertTrue(parser.validate_duo())


class TestOntologyInvalidInput(unittest.TestCase):
    """
    This class includes invalid ontology input json
    """

    def testInvalidOntologyInput1(self):
        """
        This is an invalid input, as id DUO:0000002 is not supported.
        """
        sample = {"duo": [{"id": "DUO:0000002"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput2(self):
        """
        This is an invalid input, as 'Duo' key should be lower case.
        """
        sample = {"Duo": [{"id": "DUO:0000018"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput3(self):
        """
        This is an invalid input, as 'duo' key is missing
        """
        sample = {"": [{"id": "DUO:0000018"}, {"id": "DUO:0000024", "modifier": "2022-01-01"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput4(self):
        """
        This is an invalid input, as 'id' key is missing
        """
        sample = {"duo": [{"": "DUO:0000018"}, {"id": "DUO:0000024", "modifier": "2022-01-01"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput5(self):
        """
        This is an invalid input, as there is no DUO Term under 'id'
        """
        sample = {"duo": [{"id": ""}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput6(self):
        """
        This is an invalid input, as there is no 'modifier' for DUO:0000024
        """
        sample = {"duo": [{"id": "DUO:0000024"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput7(self):
        """
        This is an invalid input, as date for 'DUO:0000024' does not follow 
        format YYYY-MM-DD
        """
        sample = {"duo": [{"id": "DUO:0000024", "modifier": "01-01-2022"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput8(self):
        """
        This is an invalid input, as 'DUO:0000024' modifier has an 
        invalid date
        """
        sample = {"duo": [{"id": "DUO:0000024", "modifier": "2022-20-20"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput9(self):
        """
        This is an invalid input, as 'Modifier' key word 
        should be lower case
        """
        sample = {"duo": [{"id": "DUO:0000024", "Modifier": "2022-01-01"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput10(self):
        """
        This is an invalid input, as the DUO term in totally invalid
        """
        sample = {"duo": [{"id": "DUO:0000089"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput11(self):
        """
        This in an invalid input, as the DUO word in 
        'id: DUO:0000018' is not uppercase
        """
        sample = {"duo": [{"id": "DUo:0000018"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput12(self):
        """
        This is an invalid imput, as the DUO Term does not follow 
        correct format
        """
        sample = {"duo": [{"id": "DUO:0018"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput13(self):
        """
        This in an invalid input, as there is only the integer part of the
        Duo Term under 'id'
        """
        sample = {"duo": [{"id": "18"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput14(self):
        """
        This is an invalid input, as there the list of Duo Terms is empty
        """
        sample = {"duo": []}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput15(self):
        """
        This is an invali input, as the Duo Term number is missing
        """
        sample = {"duo": [{"id": "DUO:"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())

    def testInvalidOntologyInput16(self):
        """
        This is an invalid input, as 'modifier' is supplied with 
        Duo Term that does not require it
        """
        sample = {"duo": [{"id": "DUO:0000018", "modifier": "2022-01-01"}]}

        parser = OntologyValidator(sample)

        self.assertFalse(parser.validate_duo())