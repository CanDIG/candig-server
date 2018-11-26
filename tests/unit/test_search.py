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
        self.dataset_id = self.dataset.getId()
        self.access_map = {self.dataset.getLocalId(): 4}

    def testCountQuery(self):
        request = {
            "dataset_id": self.dataset_id,
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
        responseStr = self.backend.runCountQuery(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        self.assertEqual(response["patients"][0]["gender"]["male"], 10)

    def testSearchQuery(self):
        request = {
            "dataset_id": self.dataset_id,
            "logic": {
                "and": [
                    {
                        "id": "A"
                    },
                    {
                        "or": [
                            {
                                "id": "B",
                                "negate": True
                            },
                            {
                                "id": "C"
                            }
                        ]
                    }
                ]
            },
            "components": [
                {
                    "id": "A",
                    "enrollments": {
                        "filters": [
                            {
                                "field": "treatingCentreName",
                                "operator": "!=",
                                "value": "Ontario"
                            }
                        ]
                    }
                },
                {
                    "id": "B",
                    "treatments": {
                        "filters": [
                            {
                                "field": "courseNumber",
                                "operator": "!=",
                                "value": "100"
                            }
                        ]
                    }
                },
                {
                    "id": "C",
                    "diagnoses": {
                        "filters": [
                            {
                                "field": "sampleType",
                                "operator": "==",
                                "value": "metastatic"
                            }
                        ]
                    }
                }
            ],
            "results": [
                {
                    "table": "samples",
                    "field": [
                        "sampleType",
                        "quantity"
                    ]
                }
            ]
        }
        request = json.dumps(request)
        # assert error for empty access map
        with self.assertRaises(exceptions.NotAuthorizedException):
            self.backend.runSearchQuery(request, "application/json", {})
        responseStr = self.backend.runSearchQuery(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        self.assertEqual(len(response["samples"]), 3)

    def testSequencingSearch(self):
        test_sample = "SAMPLE_74122"
        request = self.generateSampleAnalysisRequest(test_sample)
        responseStr = self.backend.runSearchSequencing(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        id = response["sequencing"][0].get("id")
        getResponseStr = self.backend.runGetSequencing(id, self.access_map, "application/json")
        getResponse = json.loads(getResponseStr)
        sample_id = getResponse.get("sampleId")
        self.assertEqual(sample_id, test_sample)

    def testExtractionSearch(self):
        test_sample = "SAMPLE_74122"
        request = self.generateSampleAnalysisRequest(test_sample)
        responseStr = self.backend.runSearchExtractions(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        id = response["extractions"][0].get("id")
        getResponseStr = self.backend.runGetExtraction(id, self.access_map, "application/json")
        getResponse = json.loads(getResponseStr)
        sample_id = getResponse.get("sampleId")
        self.assertEqual(sample_id, test_sample)

    def testAlignmentSearch(self):
        test_sample = "SAMPLE_74122"
        request = self.generateSampleAnalysisRequest(test_sample)
        responseStr = self.backend.runSearchAlignments(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        id = response["alignments"][0].get("id")
        getResponseStr = self.backend.runGetAlignment(id, self.access_map, "application/json")
        getResponse = json.loads(getResponseStr)
        sample_id = getResponse.get("sampleId")
        self.assertEqual(sample_id, test_sample)

    def testVariantCallingSearch(self):
        test_sample = "SAMPLE_74122"
        request = self.generateSampleAnalysisRequest(test_sample)
        responseStr = self.backend.runSearchVariantCalling(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        id = response["variantcalling"][0].get("id")
        getResponseStr = self.backend.runGetVariantCalling(id, self.access_map, "application/json")
        getResponse = json.loads(getResponseStr)
        sample_id = getResponse.get("sampleId")
        self.assertEqual(sample_id, test_sample)

    def testFusionDetectionSearch(self):
        test_sample = "SAMPLE_74122"
        request = self.generateSampleAnalysisRequest(test_sample)
        responseStr = self.backend.runSearchFusionDetection(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        id = response["fusiondetection"][0].get("id")
        getResponseStr = self.backend.runGetFusionDetection(id, self.access_map, "application/json")
        getResponse = json.loads(getResponseStr)
        sample_id = getResponse.get("sampleId")
        self.assertEqual(sample_id, test_sample)

    def testExpressionAnalysisSearch(self):
        test_sample = "SAMPLE_74122"
        request = self.generateSampleAnalysisRequest(test_sample)
        responseStr = self.backend.runSearchExpressionAnalysis(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        id = response["expressionanalysis"][0].get("id")
        getResponseStr = self.backend.runGetExpressionAnalysis(id, self.access_map, "application/json")
        getResponse = json.loads(getResponseStr)
        sample_id = getResponse.get("sampleId")
        self.assertEqual(sample_id, test_sample)

    def generateSampleAnalysisRequest(self, test_sample):
        request = {
            "datasetId": self.dataset_id,
            "filters": [
                {
                    "field": "sampleId",
                    "operator": "=",
                    "value": test_sample
                }
            ]
        }
        return json.dumps(request)

    def testDifferentialPrivacy(self):
        request = {
            "dataset_id": self.dataset_id,
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
                    "field": ["provinceOfResidence"]
                }
            ]
        }
        request = json.dumps(request)
        self.backend.setDpEpsilon(0.75)
        self.assertEqual(self.backend._dpEpsilon, 0.75)
        responseStr = self.backend.runCountQuery(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        fieldResponse = response["patients"][0]["provinceOfResidence"]
        self.assertGreater(fieldResponse["British Columbia"], fieldResponse["Quebec"])
        self.assertGreater(fieldResponse["British Columbia"], fieldResponse["Northwest Territories"])
