"""
Tests the biodata module
"""

import unittest

import candig.server.datamodel.datasets as datasets
import candig.server.exceptions as exceptions
import candig.server.datamodel.bio_metadata as bioMetadata

import candig.schemas.protocol as protocol


class TestIndividuals(unittest.TestCase):
    """
    Tests the Individuals class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        term = protocol.OntologyTerm()
        term.term = "male genotypic sex"
        term.term_id = "PATO:0020001"
        # Write out a valid input
        print(protocol.toJsonDict(term))
        validIndividual = protocol.Individual(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            sex=term)
        validIndividual.attributes.attr['test']. \
            values.add().string_value = 'test-info'
        # pass through protocol creation
        individual = bioMetadata.Individual(
            dataset, "test")
        individual.populateFromJson(protocol.toJson(validIndividual))
        gaIndividual = individual.toProtocolElement()
        # Verify elements exist
        self.assertEqual(gaIndividual.created, validIndividual.created)
        self.assertEqual(gaIndividual.updated, validIndividual.updated)
        # Invalid input
        invalidIndividual = '{"bad:", "json"}'
        individual = bioMetadata.Individual(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            individual.populateFromJson,
            invalidIndividual)


class TestBiosamples(unittest.TestCase):
    """
    Tests the Biosamples class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        # Write out a valid input
        validBiosample = protocol.Biosample(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z")
        validBiosample.attributes.attr['test']. \
            values.add().string_value = 'test-info'
        # pass through protocol creation
        biosample = bioMetadata.Biosample(
            dataset, "test")
        biosample.populateFromJson(protocol.toJson(validBiosample))
        gaBiosample = biosample.toProtocolElement()
        # Verify elements exist
        self.assertEqual(gaBiosample.created, validBiosample.created)
        self.assertEqual(gaBiosample.updated, validBiosample.updated)
        # Invalid input
        invalidBiosample = '{"bad:", "json"}'
        biosample = bioMetadata.Individual(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            biosample.populateFromJson,
            invalidBiosample)
