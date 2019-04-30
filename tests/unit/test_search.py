"""
Tests the backend methods and generators for the advanced search API
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import json

import candig.server.backend as backend
import candig.server.exceptions as exceptions
import candig.server.datarepo as datarepo
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
                    "fields": ["gender"]
                }
            ]
        }
        request = json.dumps(request)
        # assert error for empty access map
        with self.assertRaises(exceptions.NotAuthorizedException):
            self.backend.runCountQuery(request, "application/json", {})
        responseStr = self.backend.runCountQuery(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        self.assertEqual(response["patients"][0]["gender"]["male"], 5)

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
        self.assertEqual(len(response["patients"]), 3)

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
                    "fields": ["provinceOfResidence"]
                }
            ]
        }
        request = json.dumps(request)
        self.backend.setDpEpsilon(0.75)
        self.assertEqual(self.backend._dpEpsilon, 0.75)
        responseStr = self.backend.runCountQuery(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        fieldResponse = response["patients"][0]["provinceOfResidence"]
        self.assertGreater(fieldResponse["British Columbia"], fieldResponse.get("Quebec", 0))
        self.assertGreater(fieldResponse["British Columbia"], fieldResponse.get("New Brunswick", 0))

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
                    "fields": [
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

        responseStr = self.backend.runGetPatient("WyJkYXRhc2V0MSIsInBhdCIsIlBBVElFTlRfNDk4NDUiXQ", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["causeOfDeath"], "Pneumonia")

        responseStr = self.backend.runGetEnrollment("WyJkYXRhc2V0MSIsImVuciIsIlBBVElFTlRfMTI0NTdfMTIvMTkvMjAxMCJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["referringPhysicianName"], "Dr. Abdullahi Horne")

        responseStr = self.backend.runGetTreatment("WyJkYXRhc2V0MSIsInRyZSIsIlBBVElFTlRfMzIxNTVfMDIvMjIvMjAwNiJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["therapeuticModality"], "Immunotherapy")

        responseStr = self.backend.runGetSample("WyJkYXRhc2V0MSIsInNhbSIsIlBBVElFTlRfNDk4NDVfU0FNUExFXzU4NjI4Il0", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["cancerType"], "Cervical cancer")

        responseStr = self.backend.runGetDiagnosis("WyJkYXRhc2V0MSIsImRpYSIsIlBBVElFTlRfNDk4NDVfMTEvMDgvMjAwOCJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["tumorGrade"], "GX: Grade cannot be assessed (undetermined grade)")

        responseStr = self.backend.runGetTumourboard("WyJkYXRhc2V0MSIsInR1bSIsIlBBVElFTlRfNDk4NDVfMDcvMDkvMjAxNCJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["typeOfSampleAnalyzed"], "metastatic")

        responseStr = self.backend.runGetOutcome("WyJkYXRhc2V0MSIsIm91dCIsIlBBVElFTlRfNDk4NDVfMDgvMjIvMjAxMiJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["diseaseResponseOrStatus"], "Complete Response")

        responseStr = self.backend.runGetComplication("WyJkYXRhc2V0MSIsImNvbSIsIlBBVElFTlRfNDk4NDVfMTAvMTgvMjAwNiJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["date"], "10/18/2006")

        responseStr = self.backend.runGetConsent("WyJkYXRhc2V0MSIsImNvbiIsIlBBVElFTlRfNDk4NDVfMDMvMDYvMjAwNyJd", self.access_map, "application/json")
        response = json.loads(responseStr)
        self.assertEqual(response["consentDate"], "03/06/2007")

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
        self.assertEqual(len(response["variants"]), 1800)

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
        # dataset_id = self.dataset.getId()

        variantSets = self.dataset.getVariantSets()
        listOfIds = []

        for item in variantSets:
            listOfIds.append(item.getId())

        request = {
            "variantSetIds": listOfIds,
            "start": "1",
            "end": "1000000",
            "referenceName": "1"
        }

        request = json.dumps(request)
        responseStr = self.backend.runSearchVariants(request, "application/json", self.access_map)
        response = json.loads(responseStr)
        self.assertEqual(len(response["variants"]), 1800)

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
                        "variantSetIds": [variantSetId],
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