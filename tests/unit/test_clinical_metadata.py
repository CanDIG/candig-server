"""
Tests the clinical meta data models
"""

import unittest

import candig.server.datamodel.datasets as datasets
import candig.server.exceptions as exceptions
import candig.server.datamodel.clinical_metadata as clinMetadata

import candig.schemas.protocol as protocol


class TestPatients(unittest.TestCase):
    """
    Test the Patient class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validPatient = protocol.Patient(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId = "PATIENT_TEST",
            patientIdTier = 0,
            otherIds = "n/a",
            otherIdsTier = 0,
            dateOfBirth = "n/a",
            dateOfBirthTier = 0,
            gender = "Male",
            genderTier = 0,
            ethnicity = "n/a",
            ethnicityTier = 0,
            race = "n/a",
            raceTier = 0,
            provinceOfResidence = "British Columbia",
            provinceOfResidenceTier = 0,
            dateOfDeath = "n/a",
            dateOfDeathTier = 0,
            causeOfDeath = "n/a",
            causeOfDeathTier = 0,
            autopsyTissueForResearch = "n/a",
            autopsyTissueForResearchTier = 0,
            priorMalignancy = "n/a",
            priorMalignancyTier = 0,
            dateOfPriorMalignancy = "n/a",
            dateOfPriorMalignancyTier = 0,
            familyHistoryAndRiskFactors = "n/a",
            familyHistoryAndRiskFactorsTier = 0,
            familyHistoryOfPredispositionSyndrome = "n/a",
            familyHistoryOfPredispositionSyndromeTier = 0,
            detailsOfPredispositionSyndrome = "n/a",
            detailsOfPredispositionSyndromeTier = 0,
            geneticCancerSyndrome = "n/a",
            geneticCancerSyndromeTier = 0,
            otherGeneticConditionOrSignificantComorbidity = "n/a",
            otherGeneticConditionOrSignificantComorbidityTier = 0,
            occupationalOrEnvironmentalExposure = "n/a",
            occupationalOrEnvironmentalExposureTier = 0,
        )

        validPatient.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        patient = clinMetadata.Patient(
            dataset, "test")
        patient.populateFromJson(protocol.toJson(validPatient))
        gaPatient = patient.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaPatient.created, validPatient.created)
        self.assertEqual(gaPatient.updated, validPatient.updated)
        self.assertEqual(gaPatient.patientId, validPatient.patientId)
        self.assertEqual(gaPatient.otherIds, validPatient.otherIds)
        self.assertEqual(gaPatient.dateOfBirth, validPatient.dateOfBirth)
        self.assertEqual(gaPatient.gender, validPatient.gender)

        # Invalid input
        invalidPatient = '{"bad:", "json"}'
        patient = clinMetadata.Patient(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            patient.populateFromJson,
            invalidPatient)


class TestEnrollment(unittest.TestCase):
    """
    Test the Enrollment class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validEnrollment = protocol.Enrollment(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            enrollmentInstitution = "GSC",
            enrollmentInstitutionTier = 0,
            enrollmentApprovalDate = "n/a",
            enrollmentApprovalDateTier = 0,
            crossEnrollment = "n/a",
            crossEnrollmentTier = 0,
            otherPersonalizedMedicineStudyName = "n/a",
            otherPersonalizedMedicineStudyNameTier = 0,
            otherPersonalizedMedicineStudyId = "n/a",
            otherPersonalizedMedicineStudyIdTier = 0,
            ageAtEnrollment = "n/a",
            ageAtEnrollmentTier = 0,
            eligibilityCategory = "n/a",
            eligibilityCategoryTier = 0,
            statusAtEnrollment = "n/a",
            statusAtEnrollmentTier = 0,
            primaryOncologistName = "n/a",
            primaryOncologistNameTier = 0,
            primaryOncologistContact = "n/a",
            primaryOncologistContactTier = 0,
            referringPhysicianName = "n/a",
            referringPhysicianNameTier = 0,
            referringPhysicianContact = "n/a",
            referringPhysicianContactTier = 0,
            summaryOfIdRequest = "n/a",
            summaryOfIdRequestTier = 0,
            treatingCentreName = "n/a",
            treatingCentreNameTier = 0,
            treatingCentreProvince = "n/a",
            treatingCentreProvinceTier = 0
        )

        validEnrollment.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        enrollment = clinMetadata.Enrollment(
            dataset, "test")
        enrollment.populateFromJson(protocol.toJson(validEnrollment))
        gaEnrollment = enrollment.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaEnrollment.created, validEnrollment.created)
        self.assertEqual(gaEnrollment.updated, validEnrollment.updated)
        self.assertEqual(gaEnrollment.patientId, validEnrollment.patientId)
        self.assertEqual(gaEnrollment.enrollmentInstitution, validEnrollment.enrollmentInstitution)
        self.assertEqual(gaEnrollment.statusAtEnrollment, validEnrollment.statusAtEnrollment)
        self.assertEqual(gaEnrollment.treatingCentreProvince, validEnrollment.treatingCentreProvince)

        # Invalid input
        invalidEnrollment = '{"bad:", "json"}'
        enrollment = clinMetadata.Enrollment(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            enrollment.populateFromJson,
            invalidEnrollment)


class TestConsent(unittest.TestCase):
    """
    Test the Consent class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validConsent = protocol.Consent(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId = "PATIENT_TEST",
            patientIdTier = 0,
            consentId = "n/a",
            consentIdTier = 0,
            consentDate = "n/a",
            consentDateTier = 0,
            consentVersion = "n/a",
            consentVersionTier = 0,
            patientConsentedTo = "n/a",
            patientConsentedToTier = 0,
            reasonForRejection = "n/a",
            reasonForRejectionTier = 0,
            wasAssentObtained = "n/a",
            wasAssentObtainedTier = 0,
            dateOfAssent = "n/a",
            dateOfAssentTier = 0,
            assentFormVersion = "n/a",
            assentFormVersionTier = 0,
            ifAssentNotObtainedWhyNot = "n/a",
            ifAssentNotObtainedWhyNotTier = 0,
            reconsentDate = "n/a",
            reconsentDateTier = 0,
            reconsentVersion = "n/a",
            reconsentVersionTier = 0,
            consentingCoordinatorName = "n/a",
            consentingCoordinatorNameTier = 0,
            previouslyConsented = "n/a",
            previouslyConsentedTier = 0,
            nameOfOtherBiobank = "n/a",
            nameOfOtherBiobankTier = 0,
            hasConsentBeenWithdrawn = "n/a",
            hasConsentBeenWithdrawnTier = 0,
            dateOfConsentWithdrawal = "n/a",
            dateOfConsentWithdrawalTier = 0,
            typeOfConsentWithdrawal = "n/a",
            typeOfConsentWithdrawalTier = 0,
            reasonForConsentWithdrawal = "n/a",
            reasonForConsentWithdrawalTier = 0,
            consentFormComplete = "n/a",
            consentFormCompleteTier = 0
        )

        validConsent.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        consent = clinMetadata.Consent(
            dataset, "test")
        consent.populateFromJson(protocol.toJson(validConsent))
        gaConsent = consent.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaConsent.created, validConsent.created)
        self.assertEqual(gaConsent.updated, validConsent.updated)
        self.assertEqual(gaConsent.patientId, validConsent.patientId)
        self.assertEqual(gaConsent.consentId, validConsent.consentId)
        self.assertEqual(gaConsent.consentFormComplete, validConsent.consentFormComplete)
        self.assertEqual(gaConsent.previouslyConsented, validConsent.previouslyConsented)

        # Invalid input
        invalidConsent = '{"bad:", "json"}'
        consent = clinMetadata.Consent(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            consent.populateFromJson,
            invalidConsent)
        

class TestDiagnosis(unittest.TestCase):
    """
    Test the Diagnosis class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validDiagnosis = protocol.Diagnosis(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            diagnosisId = "n/a",
            diagnosisIdTier = 0,
            diagnosisDate = "n/a",
            diagnosisDateTier = 0,
            ageAtDiagnosis = "n/a",
            ageAtDiagnosisTier = 0,
            cancerType = "n/a",
            cancerTypeTier = 0,
            classification = "n/a",
            classificationTier = 0,
            cancerSite = "n/a",
            cancerSiteTier = 0,
            histology = "n/a",
            histologyTier = 0,
            methodOfDefinitiveDiagnosis = "n/a",
            methodOfDefinitiveDiagnosisTier = 0,
            sampleType = "n/a",
            sampleTypeTier = 0,
            sampleSite = "n/a",
            sampleSiteTier = 0,
            tumorGrade = "n/a",
            tumorGradeTier = 0,
            gradingSystemUsed = "n/a",
            gradingSystemUsedTier = 0,
            sitesOfMetastases = "n/a",
            sitesOfMetastasesTier = 0,
            stagingSystem = "n/a",
            stagingSystemTier = 0,
            versionOrEditionOfTheStagingSystem = "n/a",
            versionOrEditionOfTheStagingSystemTier = 0,
            specificTumorStageAtDiagnosis = "n/a",
            specificTumorStageAtDiagnosisTier = 0,
            prognosticBiomarkers = "n/a",
            prognosticBiomarkersTier = 0,
            biomarkerQuantification = "n/a",
            biomarkerQuantificationTier = 0,
            additionalMolecularTesting = "n/a",
            additionalMolecularTestingTier = 0,
            additionalTestType = "n/a",
            additionalTestTypeTier = 0,
            laboratoryName = "n/a",
            laboratoryNameTier = 0,
            laboratoryAddress = "n/a",
            laboratoryAddressTier = 0,
            siteOfMetastases = "n/a",
            siteOfMetastasesTier = 0,
            stagingSystemVersion = "n/a",
            stagingSystemVersionTier = 0,
            specificStage = "n/a",
            specificStageTier = 0,
            cancerSpecificBiomarkers = "n/a",
            cancerSpecificBiomarkersTier = 0,
            additionalMolecularDiagnosticTestingPerformed = "n/a",
            additionalMolecularDiagnosticTestingPerformedTier = 0,
            additionalTest = "n/a",
            additionalTestTier = 0
        )

        validDiagnosis.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        diagnosis = clinMetadata.Diagnosis(
            dataset, "test")
        diagnosis.populateFromJson(protocol.toJson(validDiagnosis))
        gaDiagnosis = diagnosis.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaDiagnosis.created, validDiagnosis.created)
        self.assertEqual(gaDiagnosis.updated, validDiagnosis.updated)
        self.assertEqual(gaDiagnosis.patientId, validDiagnosis.patientId)
        self.assertEqual(gaDiagnosis.cancerType, validDiagnosis.cancerType)
        self.assertEqual(gaDiagnosis.cancerSite, validDiagnosis.cancerSite)
        self.assertEqual(gaDiagnosis.additionalTest, validDiagnosis.additionalTest)

        # Invalid input
        invalidDiagnosis = '{"bad:", "json"}'
        diagnosis = clinMetadata.Diagnosis(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            diagnosis.populateFromJson,
            invalidDiagnosis)
        
        
class TestSample(unittest.TestCase):
    """
    Test the Sample class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validSample = protocol.Sample(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            sampleId = "SAMPLE_TEST",
            sampleIdTier = 0,
            diagnosisId = "DIAGNOSIS_TEST",
            diagnosisIdTier = 0,
            localBiobankId = "n/a",
            localBiobankIdTier = 0,
            collectionDate = "n/a",
            collectionDateTier = 0,
            collectionHospital = "n/a",
            collectionHospitalTier = 0,
            sampleType = "n/a",
            sampleTypeTier = 0,
            tissueDiseaseState = "n/a",
            tissueDiseaseStateTier = 0,
            anatomicSiteTheSampleObtainedFrom = "n/a",
            anatomicSiteTheSampleObtainedFromTier = 0,
            cancerType = "n/a",
            cancerTypeTier = 0,
            cancerSubtype = "n/a",
            cancerSubtypeTier = 0,
            pathologyReportId = "n/a",
            pathologyReportIdTier = 0,
            morphologicalCode = "n/a",
            morphologicalCodeTier = 0,
            topologicalCode = "n/a",
            topologicalCodeTier = 0,
            shippingDate = "n/a",
            shippingDateTier = 0,
            receivedDate = "n/a",
            receivedDateTier = 0,
            qualityControlPerformed = "n/a",
            qualityControlPerformedTier = 0,
            estimatedTumorContent = "n/a",
            estimatedTumorContentTier = 0,
            quantity = "n/a",
            quantityTier = 0,
            units = "n/a",
            unitsTier = 0,
            associatedBiobank = "n/a",
            associatedBiobankTier = 0,
            otherBiobank = "n/a",
            otherBiobankTier = 0,
            sopFollowed = "n/a",
            sopFollowedTier = 0,
            ifNotExplainAnyDeviation = "n/a",
            ifNotExplainAnyDeviationTier = 0
        )

        validSample.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        sample = clinMetadata.Sample(
            dataset, "test")
        sample.populateFromJson(protocol.toJson(validSample))
        gaSample = sample.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaSample.created, validSample.created)
        self.assertEqual(gaSample.updated, validSample.updated)
        self.assertEqual(gaSample.patientId, validSample.patientId)
        self.assertEqual(gaSample.sampleId, validSample.sampleId)
        self.assertEqual(gaSample.diagnosisId, validSample.diagnosisId)
        self.assertEqual(gaSample.associatedBiobankTier, validSample.associatedBiobankTier)

        # Invalid input
        invalidSample = '{"bad:", "json"}'
        sample = clinMetadata.Sample(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            sample.populateFromJson,
            invalidSample)
        

class TestTreatment(unittest.TestCase):
    """
    Test the Treatment class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validTreatment = protocol.Treatment(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            courseNumber = "n/a",
            courseNumberTier = 0,
            therapeuticModality = "n/a",
            therapeuticModalityTier = 0,
            treatmentPlanType = "n/a",
            treatmentPlanTypeTier = 0,
            treatmentIntent = "n/a",
            treatmentIntentTier = 0,
            startDate = "n/a",
            startDateTier = 0,
            stopDate = "n/a",
            stopDateTier = 0,
            reasonForEndingTheTreatment = "n/a",
            reasonForEndingTheTreatmentTier = 0,
            responseToTreatment = "n/a",
            responseToTreatmentTier = 0,
            responseCriteriaUsed = "n/a",
            responseCriteriaUsedTier = 0,
            dateOfRecurrenceOrProgressionAfterThisTreatment = "n/a",
            dateOfRecurrenceOrProgressionAfterThisTreatmentTier = 0,
            unexpectedOrUnusualToxicityDuringTreatment = "n/a",
            unexpectedOrUnusualToxicityDuringTreatmentTier = 0
        )

        validTreatment.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        treatment = clinMetadata.Treatment(
            dataset, "test")
        treatment.populateFromJson(protocol.toJson(validTreatment))
        gaTreatment = treatment.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaTreatment.created, validTreatment.created)
        self.assertEqual(gaTreatment.updated, validTreatment.updated)
        self.assertEqual(gaTreatment.patientId, validTreatment.patientId)
        self.assertEqual(gaTreatment.courseNumber, validTreatment.courseNumber)
        self.assertEqual(gaTreatment.startDate, validTreatment.startDate)

        # Invalid input
        invalidTreatment = '{"bad:", "json"}'
        treatment = clinMetadata.Treatment(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            treatment.populateFromJson,
            invalidTreatment)


class TestOutcome(unittest.TestCase):
    """
    Test the Outcome class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validOutcome = protocol.Outcome(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            physicalExamId = "n/a",
            physicalExamIdTier = 0,
            dateOfAssessment = "n/a",
            dateOfAssessmentTier = 0,
            diseaseResponseOrStatus = "n/a",
            diseaseResponseOrStatusTier = 0,
            otherResponseClassification = "n/a",
            otherResponseClassificationTier = 0,
            minimalResidualDiseaseAssessment = "n/a",
            minimalResidualDiseaseAssessmentTier = 0,
            methodOfResponseEvaluation = "n/a",
            methodOfResponseEvaluationTier = 0,
            responseCriteriaUsed = "n/a",
            responseCriteriaUsedTier = 0,
            summaryStage = "n/a",
            summaryStageTier = 0,
            sitesOfAnyProgressionOrRecurrence = "n/a",
            sitesOfAnyProgressionOrRecurrenceTier = 0,
            vitalStatus = "n/a",
            vitalStatusTier = 0,
            height = "n/a",
            heightTier = 0,
            weight = "n/a",
            weightTier = 0,
            heightUnits = "n/a",
            heightUnitsTier = 0,
            weightUnits = "n/a",
            weightUnitsTier = 0,
            performanceStatus = "n/a",
            performanceStatusTier = 0
        )

        validOutcome.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        outcome = clinMetadata.Outcome(
            dataset, "test")
        outcome.populateFromJson(protocol.toJson(validOutcome))
        gaOutcome = outcome.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaOutcome.created, validOutcome.created)
        self.assertEqual(gaOutcome.updated, validOutcome.updated)
        self.assertEqual(gaOutcome.patientId, validOutcome.patientId)
        self.assertEqual(gaOutcome.physicalExamId, validOutcome.physicalExamId)
        self.assertEqual(gaOutcome.summaryStage, validOutcome.summaryStage)
        self.assertEqual(gaOutcome.performanceStatusTier, validOutcome.performanceStatusTier)

        # Invalid input
        invalidOutcome = '{"bad:", "json"}'
        outcome = clinMetadata.Outcome(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            outcome.populateFromJson,
            invalidOutcome)
        
        
class TestComplication(unittest.TestCase):
    """
    Test the Complication class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validComplication = protocol.Complication(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            date = "n/a",
            dateTier = 0,
            lateComplicationOfTherapyDeveloped = "n/a",
            lateComplicationOfTherapyDevelopedTier = 0,
            lateToxicityDetail = "n/a",
            lateToxicityDetailTier = 0,
            suspectedTreatmentInducedNeoplasmDeveloped = "n/a",
            suspectedTreatmentInducedNeoplasmDevelopedTier = 0,
            treatmentInducedNeoplasmDetails = "n/a",
            treatmentInducedNeoplasmDetailsTier = 0
        )

        validComplication.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        complication = clinMetadata.Complication(
            dataset, "test")
        complication.populateFromJson(protocol.toJson(validComplication))
        gaComplication = complication.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaComplication.created, validComplication.created)
        self.assertEqual(gaComplication.updated, validComplication.updated)
        self.assertEqual(gaComplication.patientId, validComplication.patientId)
        self.assertEqual(gaComplication.date, validComplication.date)
        self.assertEqual(gaComplication.lateToxicityDetail, validComplication.lateToxicityDetail)
        self.assertEqual(gaComplication.treatmentInducedNeoplasmDetailsTier, validComplication.treatmentInducedNeoplasmDetailsTier)

        # Invalid input
        invalidComplication = '{"bad:", "json"}'
        complication = clinMetadata.Complication(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            complication.populateFromJson,
            invalidComplication)


class TestTumourboard(unittest.TestCase):
    """
    Test the Tumourboard class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validTumourboard = protocol.Tumourboard(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            dateOfMolecularTumorBoard = "n/a",
            dateOfMolecularTumorBoardTier = 0,
            typeOfSampleAnalyzed = "n/a",
            typeOfSampleAnalyzedTier = 0,
            typeOfTumourSampleAnalyzed = "n/a",
            typeOfTumourSampleAnalyzedTier = 0,
            analysesDiscussed = "n/a",
            analysesDiscussedTier = 0,
            somaticSampleType = "n/a",
            somaticSampleTypeTier = 0,
            normalExpressionComparator = "n/a",
            normalExpressionComparatorTier = 0,
            diseaseExpressionComparator = "n/a",
            diseaseExpressionComparatorTier = 0,
            hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer = "n/a",
            hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancerTier = 0,
            actionableTargetFound = "n/a",
            actionableTargetFoundTier = 0,
            molecularTumorBoardRecommendation = "n/a",
            molecularTumorBoardRecommendationTier = 0,
            germlineDnaSampleId = "n/a",
            germlineDnaSampleIdTier = 0,
            tumorDnaSampleId = "n/a",
            tumorDnaSampleIdTier = 0,
            tumorRnaSampleId = "n/a",
            tumorRnaSampleIdTier = 0,
            germlineSnvDiscussed = "n/a",
            germlineSnvDiscussedTier = 0,
            somaticSnvDiscussed = "n/a",
            somaticSnvDiscussedTier = 0,
            cnvsDiscussed = "n/a",
            cnvsDiscussedTier = 0,
            structuralVariantDiscussed = "n/a",
            structuralVariantDiscussedTier = 0,
            classificationOfVariants = "n/a",
            classificationOfVariantsTier = 0,
            clinicalValidationProgress = "n/a",
            clinicalValidationProgressTier = 0,
            typeOfValidation = "n/a",
            typeOfValidationTier = 0,
            agentOrDrugClass = "n/a",
            agentOrDrugClassTier = 0,
            levelOfEvidenceForExpressionTargetAgentMatch = "n/a",
            levelOfEvidenceForExpressionTargetAgentMatchTier = 0,
            didTreatmentPlanChangeBasedOnProfilingResult = "n/a",
            didTreatmentPlanChangeBasedOnProfilingResultTier = 0,
            howTreatmentHasAlteredBasedOnProfiling = "n/a",
            howTreatmentHasAlteredBasedOnProfilingTier = 0,
            reasonTreatmentPlanDidNotChangeBasedOnProfiling = "n/a",
            reasonTreatmentPlanDidNotChangeBasedOnProfilingTier = 0,
            detailsOfTreatmentPlanImpact = "n/a",
            detailsOfTreatmentPlanImpactTier = 0,
            patientOrFamilyInformedOfGermlineVariant = "n/a",
            patientOrFamilyInformedOfGermlineVariantTier = 0,
            patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling = "n/a",
            patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfilingTier = 0,
            summaryReport = "n/a",
            summaryReportTier = 0
        )

        validTumourboard.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        tumourboard = clinMetadata.Tumourboard(
            dataset, "test")
        tumourboard.populateFromJson(protocol.toJson(validTumourboard))
        gaTumourboard = tumourboard.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaTumourboard.created, validTumourboard.created)
        self.assertEqual(gaTumourboard.updated, validTumourboard.updated)
        self.assertEqual(gaTumourboard.patientId, validTumourboard.patientId)
        self.assertEqual(gaTumourboard.dateOfMolecularTumorBoard, validTumourboard.dateOfMolecularTumorBoard)
        self.assertEqual(gaTumourboard.typeOfValidation, validTumourboard.typeOfValidation)
        self.assertEqual(gaTumourboard.summaryReportTier, validTumourboard.summaryReportTier)

        # Invalid input
        invalidTumourboard = '{"bad:", "json"}'
        tumourboard = clinMetadata.Tumourboard(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            tumourboard.populateFromJson,
            invalidTumourboard)


class TestStudy(unittest.TestCase):
    """
    Test the Study class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validStudy = protocol.Study(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            startDate = "n/a",
            startDateTier=0,
            endDate="n/a",
            endDateTier=0,
            status="n/a",
            statusTier=0,
            recordingDate="n/a",
            recordingDateTier=0
        )

        validStudy.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        study = clinMetadata.Study(
            dataset, "test")
        study.populateFromJson(protocol.toJson(validStudy))
        gaStudy = study.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaStudy.created, validStudy.created)
        self.assertEqual(gaStudy.updated, validStudy.updated)
        self.assertEqual(gaStudy.patientId, validStudy.patientId)
        self.assertEqual(gaStudy.startDate, validStudy.startDate)
        self.assertEqual(gaStudy.status, validStudy.status)
        self.assertEqual(gaStudy.recordingDateTier, validStudy.recordingDateTier)

        # Invalid input
        invalidStudy = '{"bad:", "json"}'
        study = clinMetadata.Study(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            study.populateFromJson,
            invalidStudy)


class TestLabtest(unittest.TestCase):
    """
    Test the Labtest class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validLabtest = protocol.Labtest(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            startDate="n/a",
            startDateTier = 0,
            collectionDate ="n/a",
            collectionDateTier=0,
            endDate ="n/a",
            endDateTier=0,
            eventType ="n/a",
            eventTypeTier=0,
            testResults ="n/a",
            testResultsTier=0,
            timePoint ="n/a",
            timePointTier=0,
            recordingDate ="n/a",
            recordingDateTier=0,
        )

        validLabtest.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        labtest = clinMetadata.Labtest(
            dataset, "test")
        labtest.populateFromJson(protocol.toJson(validLabtest))
        gaLabtest = labtest.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaLabtest.created, validLabtest.created)
        self.assertEqual(gaLabtest.updated, validLabtest.updated)
        self.assertEqual(gaLabtest.patientId, validLabtest.patientId)
        self.assertEqual(gaLabtest.eventType, validLabtest.eventType)
        self.assertEqual(gaLabtest.collectionDate, validLabtest.collectionDate)
        self.assertEqual(gaLabtest.recordingDateTier, validLabtest.recordingDateTier)

        # Invalid input
        invalidLabtest = '{"bad:", "json"}'
        labtest = clinMetadata.Labtest(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            labtest.populateFromJson,
            invalidLabtest)


class TestSlide(unittest.TestCase):
    """
    Test the Slide class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validSlide = protocol.Slide(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            sampleId ="n/a",
            sampleIdTier=0,
            slideId ="n/a",
            slideIdTier=0,
            slideOtherId ="n/a",
            slideOtherIdTier=0,
            lymphocyteInfiltrationPercent ="n/a",
            lymphocyteInfiltrationPercentTier=0,
            tumorNucleiPercent ="n/a",
            tumorNucleiPercentTier=0,
            monocyteInfiltrationPercent ="n/a",
            monocyteInfiltrationPercentTier=0,
            normalCellsPercent ="n/a",
            normalCellsPercentTier=0,
            tumorCellsPercent ="n/a",
            tumorCellsPercentTier=0,
            stromalCellsPercent ="n/a",
            stromalCellsPercentTier=0,
            eosinophilInfiltrationPercent ="n/a",
            eosinophilInfiltrationPercentTier=0,
            neutrophilInfiltrationPercent ="n/a",
            neutrophilInfiltrationPercentTier=0,
            granulocyteInfiltrationPercent ="n/a",
            granulocyteInfiltrationPercentTier=0,
            necrosisPercent ="n/a",
            necrosisPercentTier=0,
            inflammatoryInfiltrationPercent ="n/a",
            inflammatoryInfiltrationPercentTier=0,
            proliferatingCellsNumber ="n/a",
            proliferatingCellsNumberTier=0,
            sectionLocation ="n/a",
            sectionLocationTier=0
        )

        validSlide.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        slide = clinMetadata.Slide(
            dataset, "test")
        slide.populateFromJson(protocol.toJson(validSlide))
        gaSlide = slide.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaSlide.created, validSlide.created)
        self.assertEqual(gaSlide.updated, validSlide.updated)
        self.assertEqual(gaSlide.patientId, validSlide.patientId)
        self.assertEqual(gaSlide.slideId, validSlide.slideId)
        self.assertEqual(gaSlide.granulocyteInfiltrationPercent, validSlide.granulocyteInfiltrationPercent)
        self.assertEqual(gaSlide.sectionLocationTier, validSlide.sectionLocationTier)

        # Invalid input
        invalidSlide = '{"bad:", "json"}'
        slide = clinMetadata.Slide(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            slide.populateFromJson,
            invalidSlide)


class TestChemotherapy(unittest.TestCase):
    """
    Test the Chemotherapy class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validChemotherapy = protocol.Chemotherapy(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            courseNumber="n/a",
            courseNumberTier=0,
            startDate="n/a",
            startDateTier=0,
            stopDate="n/a",
            stopDateTier=0,
            systematicTherapyAgentName="n/a",
            systematicTherapyAgentNameTier=0,
            route="n/a",
            routeTier=0,
            dose="n/a",
            doseTier=0,
            doseFrequency="n/a",
            doseFrequencyTier=0,
            doseUnit="n/a",
            doseUnitTier=0,
            daysPerCycle="n/a",
            daysPerCycleTier=0,
            numberOfCycle="n/a",
            numberOfCycleTier=0,
            treatmentIntent="n/a",
            treatmentIntentTier=0,
            treatingCentreName="n/a",
            treatingCentreNameTier=0,
            type="n/a",
            typeTier=0,
            protocolCode="n/a",
            protocolCodeTier=0,
            recordingDate="n/a",
            recordingDateTier=0,
            treatmentPlanId="n/a",
            treatmentPlanIdTier=0
        )

        validChemotherapy.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        chemotherapy = clinMetadata.Chemotherapy(
            dataset, "test")
        chemotherapy.populateFromJson(protocol.toJson(validChemotherapy))
        gaChemotherapy = chemotherapy.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaChemotherapy.created, validChemotherapy.created)
        self.assertEqual(gaChemotherapy.updated, validChemotherapy.updated)
        self.assertEqual(gaChemotherapy.patientId, validChemotherapy.patientId)
        self.assertEqual(gaChemotherapy.systematicTherapyAgentName, validChemotherapy.systematicTherapyAgentName)
        self.assertEqual(gaChemotherapy.protocolCode, validChemotherapy.protocolCode)
        self.assertEqual(gaChemotherapy.treatmentPlanIdTier, validChemotherapy.treatmentPlanIdTier)

        # Invalid input
        invalidChemotherapy = '{"bad:", "json"}'
        chemotherapy = clinMetadata.Chemotherapy(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            chemotherapy.populateFromJson,
            invalidChemotherapy)


class TestRadiotherapy(unittest.TestCase):
    """
    Test the Radiotherapy class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validRadiotherapy = protocol.Radiotherapy(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            courseNumber="n/a",
            courseNumberTier=0,
            startDate="n/a",
            startDateTier=0,
            stopDate="n/a",
            stopDateTier=0,
            therapeuticModality="n/a",
            therapeuticModalityTier=0,
            baseline="n/a",
            baselineTier=0,
            testResult="n/a",
            testResultTier=0,
            testResultStd="n/a",
            testResultStdTier=0,
            treatingCentreName="n/a",
            treatingCentreNameTier=0,
            startIntervalRad="n/a",
            startIntervalRadTier=0,
            startIntervalRadRaw="n/a",
            startIntervalRadRawTier=0,
            recordingDate="n/a",
            recordingDateTier=0,
            adjacentFields="n/a",
            adjacentFieldsTier=0,
            adjacentFractions="n/a",
            adjacentFractionsTier=0,
            complete="n/a",
            completeTier=0,
            brachytherapyDose="n/a",
            brachytherapyDoseTier=0,
            radiotherapyDose="n/a",
            radiotherapyDoseTier=0,
            siteNumber="n/a",
            siteNumberTier=0,
            technique="n/a",
            techniqueTier=0,
            treatedRegion="n/a",
            treatedRegionTier=0,
            treatmentPlanId="n/a",
            treatmentPlanIdTier=0,
            radiationType="n/a",
            radiationTypeTier=0,
            radiationSite="n/a",
            radiationSiteTier=0,
            totalDose="n/a",
            totalDoseTier=0,
            boostSite="n/a",
            boostSiteTier=0,
            boostDose="n/a",
            boostDoseTier=0
        )

        validRadiotherapy.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        radiotherapy = clinMetadata.Radiotherapy(
            dataset, "test")
        radiotherapy.populateFromJson(protocol.toJson(validRadiotherapy))
        gaRadiotherapy = radiotherapy.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaRadiotherapy.created, validRadiotherapy.created)
        self.assertEqual(gaRadiotherapy.updated, validRadiotherapy.updated)
        self.assertEqual(gaRadiotherapy.patientId, validRadiotherapy.patientId)
        self.assertEqual(gaRadiotherapy.brachytherapyDose, validRadiotherapy.brachytherapyDose)
        self.assertEqual(gaRadiotherapy.adjacentFractions, validRadiotherapy.adjacentFractions)
        self.assertEqual(gaRadiotherapy.treatmentPlanIdTier, validRadiotherapy.treatmentPlanIdTier)

        # Invalid input
        invalidRadiotherapy = '{"bad:", "json"}'
        radiotherapy = clinMetadata.Radiotherapy(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            radiotherapy.populateFromJson,
            invalidRadiotherapy)


class TestSurgery(unittest.TestCase):
    """
    Test the Surgery class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validSurgery = protocol.Surgery(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            startDate="n/a",
            startDateTier=0,
            stopDate="n/a",
            stopDateTier=0,
            sampleId="n/a",
            sampleIdTier=0,
            collectionTimePoint="n/a",
            collectionTimePointTier=0,
            diagnosisDate="n/a",
            diagnosisDateTier=0,
            site="n/a",
            siteTier=0,
            type="n/a",
            typeTier=0,
            recordingDate="n/a",
            recordingDateTier=0,
            treatmentPlanId="n/a",
            treatmentPlanIdTier=0,
            courseNumber="1",
            courseNumberTier=0
        )

        validSurgery.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        surgery = clinMetadata.Surgery(
            dataset, "test")
        surgery.populateFromJson(protocol.toJson(validSurgery))
        gaSurgery = surgery.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaSurgery.created, validSurgery.created)
        self.assertEqual(gaSurgery.updated, validSurgery.updated)
        self.assertEqual(gaSurgery.patientId, validSurgery.patientId)
        self.assertEqual(gaSurgery.collectionTimePoint, validSurgery.collectionTimePoint)
        self.assertEqual(gaSurgery.recordingDate, validSurgery.recordingDate)
        self.assertEqual(gaSurgery.treatmentPlanIdTier, validSurgery.treatmentPlanIdTier)

        # Invalid input
        invalidSurgery = '{"bad:", "json"}'
        surgery = clinMetadata.Surgery(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            surgery.populateFromJson,
            invalidSurgery)


class TestImmunotherapy(unittest.TestCase):
    """
    Test the Immunotherapy class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validImmunotherapy = protocol.Immunotherapy(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            startDate="n/a",
            startDateTier=0,
            immunotherapyType="n/a",
            immunotherapyTypeTier=0,
            immunotherapyTarget="n/a",
            immunotherapyTargetTier=0,
            immunotherapyDetail="n/a",
            immunotherapyDetailTier=0,
            treatmentPlanId="n/a",
            treatmentPlanIdTier=0,
            courseNumber="1",
            courseNumberTier=0
        )

        validImmunotherapy.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        immunotherapy = clinMetadata.Immunotherapy(
            dataset, "test")
        immunotherapy.populateFromJson(protocol.toJson(validImmunotherapy))
        gaImmunotherapy = immunotherapy.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaImmunotherapy.created, validImmunotherapy.created)
        self.assertEqual(gaImmunotherapy.updated, validImmunotherapy.updated)
        self.assertEqual(gaImmunotherapy.patientId, validImmunotherapy.patientId)
        self.assertEqual(gaImmunotherapy.immunotherapyType, validImmunotherapy.immunotherapyType)
        self.assertEqual(gaImmunotherapy.immunotherapyDetailTier, validImmunotherapy.immunotherapyDetailTier)
        self.assertEqual(gaImmunotherapy.treatmentPlanId, validImmunotherapy.treatmentPlanId)

        # Invalid input
        invalidImmunotherapy = '{"bad:", "json"}'
        immunotherapy = clinMetadata.Immunotherapy(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            immunotherapy.populateFromJson,
            invalidImmunotherapy)


class TestCelltransplant(unittest.TestCase):
    """
        Test the Celltransplant class
        """

    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validCelltransplant = protocol.Celltransplant(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            patientId="PATIENT_TEST",
            patientIdTier=0,
            startDate="n/a",
            startDateTier=0,
            cellSource="n/a",
            cellSourceTier=0,
            donorType="n/a",
            donorTypeTier=0,
            treatmentPlanId="PATIENT_TEST_1",
            treatmentPlanIdTier=0,
            courseNumber="1",
            courseNumberTier=0
        )

        validCelltransplant.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        celltransplant = clinMetadata.Celltransplant(
            dataset, "test")
        celltransplant.populateFromJson(protocol.toJson(validCelltransplant))
        gaCelltransplant = celltransplant.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaCelltransplant.created, validCelltransplant.created)
        self.assertEqual(gaCelltransplant.updated, validCelltransplant.updated)
        self.assertEqual(gaCelltransplant.patientId, validCelltransplant.patientId)
        self.assertEqual(gaCelltransplant.cellSource, validCelltransplant.cellSource)
        self.assertEqual(gaCelltransplant.courseNumber, validCelltransplant.courseNumber)
        self.assertEqual(gaCelltransplant.treatmentPlanId, validCelltransplant.treatmentPlanId)

        # Invalid input
        invalidCelltransplant = '{"bad:", "json"}'
        celltransplant = clinMetadata.Celltransplant(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            celltransplant.populateFromJson,
            invalidCelltransplant)
