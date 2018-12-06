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

    def testSearchQuery2(self):
        dataset_id = self.dataset.getId()
        request = {
            "dataset_id": dataset_id,
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
                    "consents": {
                        "filters": [
                            {
                                "field": "previouslyConsented",
                                "operator": "==",
                                "value": "Yes"
                            }
                        ]
                    }
                },
                {
                    "id": "B",
                    "outcomes": {
                        "filters": [
                            {
                                "field": "vitalStatus",
                                "operator": "!=",
                                "value": "Alive"
                            }
                        ]
                    }
                },
                {
                    "id": "C",
                    "complications": {
                        "filters": [
                            {
                                "field": "date",
                                "operator": "!=",
                                "value": "01/01/2001"
                            }
                        ]
                    }
                }
            ],
            "results": [
                {
                    "table": "tumourboards",
                    "field": [
                        "typeOfSampleAnalyzed"
                    ]
                }
            ]
        }
        request = json.dumps(request)
        # assert error for empty access map
        with self.assertRaises(exceptions.NotAuthorizedException):
            self.backend.runSearchQuery(request, "application/json", {})
        responseStr = self.backend.runSearchQuery(request, "application/json", {self.dataset.getLocalId(): 4})
        response = json.loads(responseStr)
        self.assertEqual(len(response["tumourboards"]), 7)

    def testClinicalGetQuery(self):

        responseStr = self.backend.runGetPatient("WyJkYXRhc2V0MSIsInBhdCIsIlBBVElFTlRfNzc5ODAiXQ", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["causeOfDeath"], "Coronary artery disease")

        responseStr = self.backend.runGetEnrollment("WyJkYXRhc2V0MSIsImVuciIsIlBBVElFTlRfODM0MDZfMDgvMjIvMjAxMiJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["referringPhysicianName"], "Dr. Mai Alfaro")

        responseStr = self.backend.runGetTreatment("WyJkYXRhc2V0MSIsInRyZSIsIlBBVElFTlRfOTI5NzZfMDUvMTQvMjAwNCJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["drugListOrAgent"], "Enzalutamide, Alectinib, Nilotinib, Streptozocin, Olaratumab")

        responseStr = self.backend.runGetSample("WyJkYXRhc2V0MSIsInNhbSIsIlBBVElFTlRfOTI5NzZfU0FNUExFXzg3NDA5Il0", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["cancerType"], "Skin cancer")

        responseStr = self.backend.runGetDiagnosis("WyJkYXRhc2V0MSIsImRpYSIsIlBBVElFTlRfOTI5NzZfMDUvMTcvMjAwNSJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["tumorGrade"], "G1: Well differentiated (low grade)")

        responseStr = self.backend.runGetTumourboard("WyJkYXRhc2V0MSIsInR1bSIsIlBBVElFTlRfOTI5NzZfMDYvMTUvMjAwOCJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["typeOfSampleAnalyzed"], "bone marrow")

        responseStr = self.backend.runGetOutcome("WyJkYXRhc2V0MSIsIm91dCIsIlBBVElFTlRfOTI5NzZfMTAvMTcvMjAxMSJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["diseaseResponseOrStatus"], "Partial Response")

        responseStr = self.backend.runGetComplication("WyJkYXRhc2V0MSIsImNvbSIsIlBBVElFTlRfOTI5NzZfMTEvMDIvMjAxMyJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["date"], "11/02/2013")

        responseStr = self.backend.runGetConsent("WyJkYXRhc2V0MSIsImNvbiIsIlBBVElFTlRfOTI5NzZfMDYvMzAvMjAwNSJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["consentDate"], "06/30/2005")

    def testVariantsByGeneSearch(self):
        dataset_id = self.dataset.getId()

        request = {
            "dataset_id": dataset_id,
            "gene": "AADACL3"
        }

        request = json.dumps(request)
        responseStr = self.backend.runSearchVariantsByGeneName(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        self.assertEqual(response, {})

        request = {
            "dataset_id": dataset_id,
            "start": "1",
            "end": "1000000",
            "referenceName": "1"
        }

        request = json.dumps(request)
        responseStr = self.backend.runSearchVariantsByGeneName(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        self.assertEqual(len(response["variants"]), 300)

    def testSearchQueryWithVariants(self):
        dataset_id = self.dataset.getId()
        request = {
            "dataset_id": dataset_id,
            "logic": {
                "id": "A"
            },
            "components": [
                {
                    "id": "A",
                    "consents": {
                        "filters": [
                            {
                                "field": "previouslyConsented",
                                "operator": "==",
                                "value": "Yes"
                            }
                        ]
                    }
                }
            ],
            "results": [
                {
                    "table": "variants",
                    "start": "1",
                    "end": "1000000",
                    "referenceName": "1"
                }
            ]
        }
        request = json.dumps(request)
        # assert error for empty access map
        with self.assertRaises(exceptions.NotAuthorizedException):
            self.backend.runSearchQuery(request, "application/json", {})
        responseStr = self.backend.runSearchQuery(request, "application/json", self.access_map)
        response = json.loads(responseStr)

        # Since the test variantSets do not link to any patient IDs, none of the variants should return
        self.assertEqual(len(response["variants"]), 0)

    def testVariantsWithListOfVariantSetIds(self):
        dataset_id = self.dataset.getId()

        variantSets = self.dataset.getVariantSets()
        listOfIds = []

        for item in variantSets:
            listOfIds.append(item.getId())

        request = {
            "dataset_id": dataset_id,
            "variantSetIds": listOfIds,
            "start": "1",
            "end": "1000000",
            "referenceName": "1"
        }

        request = json.dumps(request)
        responseStr = self.backend.runSearchVariants(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        self.assertEqual(len(response["variants"]), 300)

    def testInvalidSearchQuery(self):
        dataset_id = self.dataset.getId()

        # Given ID does not match with any component
        request = {
            "dataset_id": dataset_id,
            "logic": {
                "id": "A"
            },
            "components": [
                {
                    "id": "B",
                    "consents": {
                        "filters": [
                            {
                                "field": "previouslyConsented",
                                "operator": "==",
                                "value": "Yes"
                            }
                        ]
                    }
                }
            ],
            "results": [
                {
                    "table": "variants",
                    "start": "1",
                    "end": "1000000",
                    "referenceName": "1"
                }
            ]
        }
        request = json.dumps(request)
        # assert error for empty access map
        with self.assertRaises(exceptions.InvalidLogicException):
            self.backend.runSearchQuery(request, "application/json", self.access_map)

    def testSearchQueryWithVariantsAsComponent(self):
        dataset_id = self.dataset.getId()
        variantSetId = self.dataset.getVariantSets()[0].getId()
        
        request = {
            "dataset_id": dataset_id,
            "logic": {
                "id": "A"
            },
            "components": [
                {
                    "id": "A",
                    "variants": {
                        "variantSetId": variantSetId,
                        "table": "variants",
                        "start": "1",
                        "end": "1000000",
                        "referenceName": "1"
                    }
                }
            ],
            "results": [
                {
                    "table": "patients"
                }
            ]
        }
        request = json.dumps(request)
        # assert error for empty access map
        with self.assertRaises(exceptions.NotAuthorizedException):
            self.backend.runSearchQuery(request, "application/json", {})
        responseStr = self.backend.runSearchQuery(request, "application/json", self.access_map)
        response = json.loads(responseStr)

        # Since the test variantSets do not link to any patient IDs, none of the patients should return
        self.assertEqual(len(response["patients"]), 0)