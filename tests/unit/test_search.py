"""
Tests the backend methods and generators for the advanced search API
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import json

import ga4gh.server.backend as backend
import ga4gh.server.exceptions as exceptions
import ga4gh.server.datarepo as datarepo
import tests.paths as paths


class TestSearchGenerator(unittest.TestCase):
    """
    Tests the logic of searchGenerator
    """
    def setUp(self):
        dataRepository = datarepo.SqlDataRepository(paths.testDataRepo)
        dataRepository.open(datarepo.MODE_READ)
        self.backend = backend.Backend(dataRepository)
        self.dataset = self.backend.getDataRepository().getDatasets()[0]

    def testCountQuery1(self):
        dataset_id = self.dataset.getId()
        request = {
            "dataset_id": dataset_id,
            "logic": {
                "id": "A"
            },
            "components": [
                {
                    "id": "A",
                    "patients": {}
                }
            ],
            "results": [
                {
                    "table": "patients",
                    "field": ["gender"]
                }
            ]
        }
        request = json.dumps(request)
        # assert error for empty access map
        with self.assertRaises(exceptions.NotAuthorizedException):
            self.backend.runCountQuery(request, "application/json", {})
        responseStr = self.backend.runCountQuery(request, "application/json", {self.dataset.getLocalId(): 4})
        response = json.loads(responseStr)
        self.assertEqual(response["patients"][0]["gender"]["male"], 10)