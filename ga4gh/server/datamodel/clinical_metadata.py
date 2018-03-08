"""
CanDIG - 2018-03-05

Clinical metadata objects

"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import json

import ga4gh.server.datamodel as datamodel
import ga4gh.server.exceptions as exceptions

import ga4gh.schemas.protocol as protocol


class Patient(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.PatientCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Patient, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._otherIds = None
        self._dateOfBirth = None
        self._gender = None
        self._ethnicity = None
        self._race = None
        self._provinceOfResidence = None
        self._dateOfDeath = None
        self._causeOfDeath = None
        self._autopsyTissueForResearch = None
        self._priorMalignancy = None
        self._dateOfPriorMalignancy = None
        self._familyHistoryAndRiskFactors = None
        self._familyHistoryOfPredispositionSyndrome = None
        self._detailsOfPredispositionSyndrome = None
        self._geneticCancerSyndrome = None
        self._otherGeneticConditionOrSignificantComorbidity = None
        self._occupationalOrEnvironmentalExposure = None

    def toProtocolElement(self):
        """
        """
        Patient = protocol.Patient(
            id = self.getId(),
            dataset_id = self._datasetId,
            created = self.getCreated(),
            updated = self.getUpdated(),
            name = self.getName(),
            description = self.getDescription(),

            # Unique fields
            patientId = self.getPatientId(),
            otherIds = self.getOtherIds(),
            dateOfBirth = self.getDateOfBirth(),
            gender = self.getGender(),
            ethnicity = self.getEthnicity(),
            race = self.getRace(),
            provinceOfResidence = self.getProvinceOfResidence(),
            dateOfDeath = self.getDateOfDeath(),
            causeOfDeath = self.getCauseOfDeath(),
            autopsyTissueForResearch = self.getAutopsyTissueForResearch(),
            priorMalignancy = self.getPriorMalignancy(),
            dateOfPriorMalignancy = self.getDateOfPriorMalignancy(),
            familyHistoryAndRiskFactors = self.getFamilyHistoryAndRiskFactors(),
            familyHistoryOfPredispositionSyndrome = self.getFamilyHistoryOfPredispositionSyndrome(),
            detailsOfPredispositionSyndrome = self.getDetailsOfPredispositionSyndrome(),
            geneticCancerSyndrome = self.getGeneticCancerSyndrome(),
            otherGeneticConditionOrSignificantComorbidity = self.getOtherGeneticConditionOrSignificantComorbidity(),
            occupationalOrEnvironmentalExposure = self.getOccupationalOrEnvironmentalExposure(),

            )
        self.serializeAttributes(Patient)
        return Patient

    def populateFromRow(self, PatientRecord):
        """
        """
        self._created = PatientRecord.created
        self._updated = PatientRecord.updated
        self._name = PatientRecord.name
        self._description = PatientRecord.description
        self.setAttributesJson(PatientRecord.attributes)

        # Unique fields
        self._patientId = PatientRecord.patientId
        self._otherIds = PatientRecord.otherIds
        self._dateOfBirth = PatientRecord.dateOfBirth
        self._gender = PatientRecord.gender
        self._ethnicity = PatientRecord.ethnicity
        self._race = PatientRecord.race
        self._provinceOfResidence = PatientRecord.provinceOfResidence
        self._dateOfDeath = PatientRecord.dateOfDeath
        self._causeOfDeath = PatientRecord.causeOfDeath
        self._autopsyTissueForResearch = PatientRecord.autopsyTissueForResearch
        self._priorMalignancy = PatientRecord.priorMalignancy
        self._dateOfPriorMalignancy = PatientRecord.dateOfPriorMalignancy
        self._familyHistoryAndRiskFactors = PatientRecord.familyHistoryAndRiskFactors
        self._familyHistoryOfPredispositionSyndrome = PatientRecord.familyHistoryOfPredispositionSyndrome
        self._detailsOfPredispositionSyndrome = PatientRecord.detailsOfPredispositionSyndrome
        self._geneticCancerSyndrome = PatientRecord.geneticCancerSyndrome
        self._otherGeneticConditionOrSignificantComorbidity = PatientRecord.otherGeneticConditionOrSignificantComorbidity
        self._occupationalOrEnvironmentalExposure = PatientRecord.occupationalOrEnvironmentalExposure

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Patient)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._otherIds = parsed.otherIds
        self._dateOfBirth = parsed.dateOfBirth
        self._gender = parsed.gender
        self._ethnicity = parsed.ethnicity
        self._race = parsed.race
        self._provinceOfResidence = parsed.provinceOfResidence
        self._dateOfDeath = parsed.dateOfDeath
        self._causeOfDeath = parsed.causeOfDeath
        self._autopsyTissueForResearch = parsed.autopsyTissueForResearch
        self._priorMalignancy = parsed.priorMalignancy
        self._dateOfPriorMalignancy = parsed.dateOfPriorMalignancy
        self._familyHistoryAndRiskFactors = parsed.familyHistoryAndRiskFactors
        self._familyHistoryOfPredispositionSyndrome = parsed.familyHistoryOfPredispositionSyndrome
        self._detailsOfPredispositionSyndrome = parsed.detailsOfPredispositionSyndrome
        self._geneticCancerSyndrome = parsed.geneticCancerSyndrome
        self._otherGeneticConditionOrSignificantComorbidity = parsed.otherGeneticConditionOrSignificantComorbidity
        self._occupationalOrEnvironmentalExposure = parsed.occupationalOrEnvironmentalExposure

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    # Unique field getters

    def getPatientId(self):
        return self._patientId

    def getOtherIds(self):
        return self._otherIds

    def getDateOfBirth(self):
        return self._dateOfBirth

    def getGender(self):
        return self._gender

    def getEthnicity(self):
        return self._ethnicity

    def getRace(self):
        return self._race

    def getProvinceOfResidence(self):
        return self._provinceOfResidence

    def getDateOfDeath(self):
        return self._dateOfDeath

    def getCauseOfDeath(self):
        return self._causeOfDeath

    def getAutopsyTissueForResearch(self):
        return self._autopsyTissueForResearch

    def getPriorMalignancy(self):
        return self._priorMalignancy

    def getDateOfPriorMalignancy(self):
        return self._dateOfPriorMalignancy

    def getFamilyHistoryAndRiskFactors(self):
        return self._familyHistoryAndRiskFactors

    def getFamilyHistoryOfPredispositionSyndrome(self):
        return self._familyHistoryOfPredispositionSyndrome

    def getDetailsOfPredispositionSyndrome(self):
        return self._detailsOfPredispositionSyndrome

    def getGeneticCancerSyndrome(self):
        return self._geneticCancerSyndrome

    def getOtherGeneticConditionOrSignificantComorbidity(self):
        return self._otherGeneticConditionOrSignificantComorbidity

    def getOccupationalOrEnvironmentalExposure(self):
        return self._occupationalOrEnvironmentalExposure



class Enrollment(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.EnrollmentCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Enrollment, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._enrollmentInstitution = None
        self._enrollmentApprovalDate = None
        self._crossEnrollment = None
        self._otherPersonalizedMedicineStudyName = None
        self._otherPersonalizedMedicineStudyId = None
        self._ageAtEnrollment = None
        self._eligibilityCategory = None
        self._statusAtEnrollment = None
        self._primaryOncologistName = None
        self._primaryOncologistContact = None
        self._referringPhysicianName = None
        self._referringPhysicianContact = None
        self._summaryOfIdRequest = None
        self._treatingCentreName = None
        self._treatingCentreProvince = None

    def toProtocolElement(self):
        """
        """
        Enrollment = protocol.Enrollment(
            id = self.getId(),
            dataset_id = self._datasetId,
            created = self.getCreated(),
            updated = self.getUpdated(),
            name = self.getName(),
            description = self.getDescription(),

            # Unique fields
            patientId = self.getPatientId(),
            enrollmentInstitution = self.getEnrollmentInstitution(),
            enrollmentApprovalDate = self.getEnrollmentApprovalDate(),
            crossEnrollment = self.getCrossEnrollment(),
            otherPersonalizedMedicineStudyName = self.getOtherPersonalizedMedicineStudyName(),
            otherPersonalizedMedicineStudyId = self.getOtherPersonalizedMedicineStudyId(),
            ageAtEnrollment = self.getAgeAtEnrollment(),
            eligibilityCategory = self.getEligibilityCategory(),
            statusAtEnrollment = self.getStatusAtEnrollment(),
            primaryOncologistName = self.getPrimaryOncologistName(),
            primaryOncologistContact = self.getPrimaryOncologistContact(),
            referringPhysicianName = self.getReferringPhysicianName(),
            referringPhysicianContact = self.getReferringPhysicianContact(),
            summaryOfIdRequest = self.getSummaryOfIdRequest(),
            treatingCentreName = self.getTreatingCentreName(),
            treatingCentreProvince = self.getTreatingCentreProvince(),

            )
        self.serializeAttributes(Enrollment)
        return Enrollment

    def populateFromRow(self, EnrollmentRecord):
        """
        """
        self._created = EnrollmentRecord.created
        self._updated = EnrollmentRecord.updated
        self._name = EnrollmentRecord.name
        self._description = EnrollmentRecord.description
        self.setAttributesJson(EnrollmentRecord.attributes)

        # Unique fields
        self._patientId = EnrollmentRecord.patientId
        self._enrollmentInstitution = EnrollmentRecord.enrollmentInstitution
        self._enrollmentApprovalDate = EnrollmentRecord.enrollmentApprovalDate
        self._crossEnrollment = EnrollmentRecord.crossEnrollment
        self._otherPersonalizedMedicineStudyName = EnrollmentRecord.otherPersonalizedMedicineStudyName
        self._otherPersonalizedMedicineStudyId = EnrollmentRecord.otherPersonalizedMedicineStudyId
        self._ageAtEnrollment = EnrollmentRecord.ageAtEnrollment
        self._eligibilityCategory = EnrollmentRecord.eligibilityCategory
        self._statusAtEnrollment = EnrollmentRecord.statusAtEnrollment
        self._primaryOncologistName = EnrollmentRecord.primaryOncologistName
        self._primaryOncologistContact = EnrollmentRecord.primaryOncologistContact
        self._referringPhysicianName = EnrollmentRecord.referringPhysicianName
        self._referringPhysicianContact = EnrollmentRecord.referringPhysicianContact
        self._summaryOfIdRequest = EnrollmentRecord.summaryOfIdRequest
        self._treatingCentreName = EnrollmentRecord.treatingCentreName
        self._treatingCentreProvince = EnrollmentRecord.treatingCentreProvince

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Enrollment)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._enrollmentInstitution = parsed.enrollmentInstitution
        self._enrollmentApprovalDate = parsed.enrollmentApprovalDate
        self._crossEnrollment = parsed.crossEnrollment
        self._otherPersonalizedMedicineStudyName = parsed.otherPersonalizedMedicineStudyName
        self._otherPersonalizedMedicineStudyId = parsed.otherPersonalizedMedicineStudyId
        self._ageAtEnrollment = parsed.ageAtEnrollment
        self._eligibilityCategory = parsed.eligibilityCategory
        self._statusAtEnrollment = parsed.statusAtEnrollment
        self._primaryOncologistName = parsed.primaryOncologistName
        self._primaryOncologistContact = parsed.primaryOncologistContact
        self._referringPhysicianName = parsed.referringPhysicianName
        self._referringPhysicianContact = parsed.referringPhysicianContact
        self._summaryOfIdRequest = parsed.summaryOfIdRequest
        self._treatingCentreName = parsed.treatingCentreName
        self._treatingCentreProvince = parsed.treatingCentreProvince

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    # Unique field getters

    def getPatientId(self):
        return self._patientId

    def getEnrollmentInstitution(self):
        return self._enrollmentInstitution

    def getEnrollmentApprovalDate(self):
        return self._enrollmentApprovalDate

    def getCrossEnrollment(self):
        return self._crossEnrollment

    def getOtherPersonalizedMedicineStudyName(self):
        return self._otherPersonalizedMedicineStudyName

    def getOtherPersonalizedMedicineStudyId(self):
        return self._otherPersonalizedMedicineStudyId

    def getAgeAtEnrollment(self):
        return self._ageAtEnrollment

    def getEligibilityCategory(self):
        return self._eligibilityCategory

    def getStatusAtEnrollment(self):
        return self._statusAtEnrollment

    def getPrimaryOncologistName(self):
        return self._primaryOncologistName

    def getPrimaryOncologistContact(self):
        return self._primaryOncologistContact

    def getReferringPhysicianName(self):
        return self._referringPhysicianName

    def getReferringPhysicianContact(self):
        return self._referringPhysicianContact

    def getSummaryOfIdRequest(self):
        return self._summaryOfIdRequest

    def getTreatingCentreName(self):
        return self._treatingCentreName

    def getTreatingCentreProvince(self):
        return self._treatingCentreProvince



class Consent(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.ConsentCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Consent, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._consentId = None
        self._consentDate = None
        self._consentVersion = None
        self._patientConsentedTo = None
        self._reasonForRejection = None
        self._wasAssentObtained = None
        self._dateOfAssent = None
        self._assentFormVersion = None
        self._ifAssentNotObtainedWhyNot = None
        self._reconsentDate = None
        self._reconsentVersion = None
        self._consentingCoordinatorName = None
        self._previouslyConsented = None
        self._nameOfOtherBiobank = None
        self._hasConsentBeenWithdrawn = None
        self._dateOfConsentWithdrawal = None
        self._typeOfConsentWithdrawal = None
        self._reasonForConsentWithdrawal = None
        self._consentFormComplete = None

    def toProtocolElement(self):
        """
        """
        Consent = protocol.Consent(
            id = self.getId(),
            dataset_id = self._datasetId,
            created = self.getCreated(),
            updated = self.getUpdated(),
            name = self.getName(),
            description = self.getDescription(),

            # Unique fields
            patientId = self.getPatientId(),
            consentId = self.getConsentId(),
            consentDate = self.getConsentDate(),
            consentVersion = self.getConsentVersion(),
            patientConsentedTo = self.getPatientConsentedTo(),
            reasonForRejection = self.getReasonForRejection(),
            wasAssentObtained = self.getWasAssentObtained(),
            dateOfAssent = self.getDateOfAssent(),
            assentFormVersion = self.getAssentFormVersion(),
            ifAssentNotObtainedWhyNot = self.getIfAssentNotObtainedWhyNot(),
            reconsentDate = self.getReconsentDate(),
            reconsentVersion = self.getReconsentVersion(),
            consentingCoordinatorName = self.getConsentingCoordinatorName(),
            previouslyConsented = self.getPreviouslyConsented(),
            nameOfOtherBiobank = self.getNameOfOtherBiobank(),
            hasConsentBeenWithdrawn = self.getHasConsentBeenWithdrawn(),
            dateOfConsentWithdrawal = self.getDateOfConsentWithdrawal(),
            typeOfConsentWithdrawal = self.getTypeOfConsentWithdrawal(),
            reasonForConsentWithdrawal = self.getReasonForConsentWithdrawal(),
            consentFormComplete = self.getConsentFormComplete(),

            )
        self.serializeAttributes(Consent)
        return Consent

    def populateFromRow(self, ConsentRecord):
        """
        """
        self._created = ConsentRecord.created
        self._updated = ConsentRecord.updated
        self._name = ConsentRecord.name
        self._description = ConsentRecord.description
        self.setAttributesJson(ConsentRecord.attributes)

        # Unique fields
        self._patientId = ConsentRecord.patientId
        self._consentId = ConsentRecord.consentId
        self._consentDate = ConsentRecord.consentDate
        self._consentVersion = ConsentRecord.consentVersion
        self._patientConsentedTo = ConsentRecord.patientConsentedTo
        self._reasonForRejection = ConsentRecord.reasonForRejection
        self._wasAssentObtained = ConsentRecord.wasAssentObtained
        self._dateOfAssent = ConsentRecord.dateOfAssent
        self._assentFormVersion = ConsentRecord.assentFormVersion
        self._ifAssentNotObtainedWhyNot = ConsentRecord.ifAssentNotObtainedWhyNot
        self._reconsentDate = ConsentRecord.reconsentDate
        self._reconsentVersion = ConsentRecord.reconsentVersion
        self._consentingCoordinatorName = ConsentRecord.consentingCoordinatorName
        self._previouslyConsented = ConsentRecord.previouslyConsented
        self._nameOfOtherBiobank = ConsentRecord.nameOfOtherBiobank
        self._hasConsentBeenWithdrawn = ConsentRecord.hasConsentBeenWithdrawn
        self._dateOfConsentWithdrawal = ConsentRecord.dateOfConsentWithdrawal
        self._typeOfConsentWithdrawal = ConsentRecord.typeOfConsentWithdrawal
        self._reasonForConsentWithdrawal = ConsentRecord.reasonForConsentWithdrawal
        self._consentFormComplete = ConsentRecord.consentFormComplete

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Consent)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._consentId = parsed.consentId
        self._consentDate = parsed.consentDate
        self._consentVersion = parsed.consentVersion
        self._patientConsentedTo = parsed.patientConsentedTo
        self._reasonForRejection = parsed.reasonForRejection
        self._wasAssentObtained = parsed.wasAssentObtained
        self._dateOfAssent = parsed.dateOfAssent
        self._assentFormVersion = parsed.assentFormVersion
        self._ifAssentNotObtainedWhyNot = parsed.ifAssentNotObtainedWhyNot
        self._reconsentDate = parsed.reconsentDate
        self._reconsentVersion = parsed.reconsentVersion
        self._consentingCoordinatorName = parsed.consentingCoordinatorName
        self._previouslyConsented = parsed.previouslyConsented
        self._nameOfOtherBiobank = parsed.nameOfOtherBiobank
        self._hasConsentBeenWithdrawn = parsed.hasConsentBeenWithdrawn
        self._dateOfConsentWithdrawal = parsed.dateOfConsentWithdrawal
        self._typeOfConsentWithdrawal = parsed.typeOfConsentWithdrawal
        self._reasonForConsentWithdrawal = parsed.reasonForConsentWithdrawal
        self._consentFormComplete = parsed.consentFormComplete

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    # Unique field getters

    def getPatientId(self):
        return self._patientId

    def getConsentId(self):
        return self._consentId

    def getConsentDate(self):
        return self._consentDate

    def getConsentVersion(self):
        return self._consentVersion

    def getPatientConsentedTo(self):
        return self._patientConsentedTo

    def getReasonForRejection(self):
        return self._reasonForRejection

    def getWasAssentObtained(self):
        return self._wasAssentObtained

    def getDateOfAssent(self):
        return self._dateOfAssent

    def getAssentFormVersion(self):
        return self._assentFormVersion

    def getIfAssentNotObtainedWhyNot(self):
        return self._ifAssentNotObtainedWhyNot

    def getReconsentDate(self):
        return self._reconsentDate

    def getReconsentVersion(self):
        return self._reconsentVersion

    def getConsentingCoordinatorName(self):
        return self._consentingCoordinatorName

    def getPreviouslyConsented(self):
        return self._previouslyConsented

    def getNameOfOtherBiobank(self):
        return self._nameOfOtherBiobank

    def getHasConsentBeenWithdrawn(self):
        return self._hasConsentBeenWithdrawn

    def getDateOfConsentWithdrawal(self):
        return self._dateOfConsentWithdrawal

    def getTypeOfConsentWithdrawal(self):
        return self._typeOfConsentWithdrawal

    def getReasonForConsentWithdrawal(self):
        return self._reasonForConsentWithdrawal

    def getConsentFormComplete(self):
        return self._consentFormComplete



class Diagnosis(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.DiagnosisCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Diagnosis, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._diagnosisId = None
        self._diagnosisDate = None
        self._ageAtDiagnosis = None
        self._cancerType = None
        self._classification = None
        self._cancerSite = None
        self._histology = None
        self._methodOfDefinitiveDiagnosis = None
        self._sampleType = None
        self._sampleSite = None
        self._tumorGrade = None
        self._gradingSystemUsed = None
        self._sitesOfMetastases = None
        self._stagingSystem = None
        self._versionOrEditionOfTheStagingSystem = None
        self._specificTumorStageAtDiagnosis = None
        self._prognosticBiomarkers = None
        self._biomarkerQuantification = None
        self._additionalMolecularTesting = None
        self._additionalTestType = None
        self._laboratoryName = None
        self._laboratoryAddress = None
        self._siteOfMetastases = None
        self._stagingSystemVersion = None
        self._specificStage = None
        self._cancerSpecificBiomarkers = None
        self._additionalMolecularDiagnosticTestingPerformed = None
        self._additionalTest = None

    def toProtocolElement(self):
        """
        """
        Diagnosis = protocol.Diagnosis(
            id = self.getId(),
            dataset_id = self._datasetId,
            created = self.getCreated(),
            updated = self.getUpdated(),
            name = self.getName(),
            description = self.getDescription(),

            # Unique fields
            patientId = self.getPatientId(),
            diagnosisId = self.getDiagnosisId(),
            diagnosisDate = self.getDiagnosisDate(),
            ageAtDiagnosis = self.getAgeAtDiagnosis(),
            cancerType = self.getCancerType(),
            classification = self.getClassification(),
            cancerSite = self.getCancerSite(),
            histology = self.getHistology(),
            methodOfDefinitiveDiagnosis = self.getMethodOfDefinitiveDiagnosis(),
            sampleType = self.getSampleType(),
            sampleSite = self.getSampleSite(),
            tumorGrade = self.getTumorGrade(),
            gradingSystemUsed = self.getGradingSystemUsed(),
            sitesOfMetastases = self.getSitesOfMetastases(),
            stagingSystem = self.getStagingSystem(),
            versionOrEditionOfTheStagingSystem = self.getVersionOrEditionOfTheStagingSystem(),
            specificTumorStageAtDiagnosis = self.getSpecificTumorStageAtDiagnosis(),
            prognosticBiomarkers = self.getPrognosticBiomarkers(),
            biomarkerQuantification = self.getBiomarkerQuantification(),
            additionalMolecularTesting = self.getAdditionalMolecularTesting(),
            additionalTestType = self.getAdditionalTestType(),
            laboratoryName = self.getLaboratoryName(),
            laboratoryAddress = self.getLaboratoryAddress(),
            siteOfMetastases = self.getSiteOfMetastases(),
            stagingSystemVersion = self.getStagingSystemVersion(),
            specificStage = self.getSpecificStage(),
            cancerSpecificBiomarkers = self.getCancerSpecificBiomarkers(),
            additionalMolecularDiagnosticTestingPerformed = self.getAdditionalMolecularDiagnosticTestingPerformed(),
            additionalTest = self.getAdditionalTest(),

            )
        self.serializeAttributes(Diagnosis)
        return Diagnosis

    def populateFromRow(self, DiagnosisRecord):
        """
        """
        self._created = DiagnosisRecord.created
        self._updated = DiagnosisRecord.updated
        self._name = DiagnosisRecord.name
        self._description = DiagnosisRecord.description
        self.setAttributesJson(DiagnosisRecord.attributes)

        # Unique fields
        self._patientId = DiagnosisRecord.patientId
        self._diagnosisId = DiagnosisRecord.diagnosisId
        self._diagnosisDate = DiagnosisRecord.diagnosisDate
        self._ageAtDiagnosis = DiagnosisRecord.ageAtDiagnosis
        self._cancerType = DiagnosisRecord.cancerType
        self._classification = DiagnosisRecord.classification
        self._cancerSite = DiagnosisRecord.cancerSite
        self._histology = DiagnosisRecord.histology
        self._methodOfDefinitiveDiagnosis = DiagnosisRecord.methodOfDefinitiveDiagnosis
        self._sampleType = DiagnosisRecord.sampleType
        self._sampleSite = DiagnosisRecord.sampleSite
        self._tumorGrade = DiagnosisRecord.tumorGrade
        self._gradingSystemUsed = DiagnosisRecord.gradingSystemUsed
        self._sitesOfMetastases = DiagnosisRecord.sitesOfMetastases
        self._stagingSystem = DiagnosisRecord.stagingSystem
        self._versionOrEditionOfTheStagingSystem = DiagnosisRecord.versionOrEditionOfTheStagingSystem
        self._specificTumorStageAtDiagnosis = DiagnosisRecord.specificTumorStageAtDiagnosis
        self._prognosticBiomarkers = DiagnosisRecord.prognosticBiomarkers
        self._biomarkerQuantification = DiagnosisRecord.biomarkerQuantification
        self._additionalMolecularTesting = DiagnosisRecord.additionalMolecularTesting
        self._additionalTestType = DiagnosisRecord.additionalTestType
        self._laboratoryName = DiagnosisRecord.laboratoryName
        self._laboratoryAddress = DiagnosisRecord.laboratoryAddress
        self._siteOfMetastases = DiagnosisRecord.siteOfMetastases
        self._stagingSystemVersion = DiagnosisRecord.stagingSystemVersion
        self._specificStage = DiagnosisRecord.specificStage
        self._cancerSpecificBiomarkers = DiagnosisRecord.cancerSpecificBiomarkers
        self._additionalMolecularDiagnosticTestingPerformed = DiagnosisRecord.additionalMolecularDiagnosticTestingPerformed
        self._additionalTest = DiagnosisRecord.additionalTest

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Diagnosis)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._diagnosisId = parsed.diagnosisId
        self._diagnosisDate = parsed.diagnosisDate
        self._ageAtDiagnosis = parsed.ageAtDiagnosis
        self._cancerType = parsed.cancerType
        self._classification = parsed.classification
        self._cancerSite = parsed.cancerSite
        self._histology = parsed.histology
        self._methodOfDefinitiveDiagnosis = parsed.methodOfDefinitiveDiagnosis
        self._sampleType = parsed.sampleType
        self._sampleSite = parsed.sampleSite
        self._tumorGrade = parsed.tumorGrade
        self._gradingSystemUsed = parsed.gradingSystemUsed
        self._sitesOfMetastases = parsed.sitesOfMetastases
        self._stagingSystem = parsed.stagingSystem
        self._versionOrEditionOfTheStagingSystem = parsed.versionOrEditionOfTheStagingSystem
        self._specificTumorStageAtDiagnosis = parsed.specificTumorStageAtDiagnosis
        self._prognosticBiomarkers = parsed.prognosticBiomarkers
        self._biomarkerQuantification = parsed.biomarkerQuantification
        self._additionalMolecularTesting = parsed.additionalMolecularTesting
        self._additionalTestType = parsed.additionalTestType
        self._laboratoryName = parsed.laboratoryName
        self._laboratoryAddress = parsed.laboratoryAddress
        self._siteOfMetastases = parsed.siteOfMetastases
        self._stagingSystemVersion = parsed.stagingSystemVersion
        self._specificStage = parsed.specificStage
        self._cancerSpecificBiomarkers = parsed.cancerSpecificBiomarkers
        self._additionalMolecularDiagnosticTestingPerformed = parsed.additionalMolecularDiagnosticTestingPerformed
        self._additionalTest = parsed.additionalTest

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    # Unique field getters

    def getPatientId(self):
        return self._patientId

    def getDiagnosisId(self):
        return self._diagnosisId

    def getDiagnosisDate(self):
        return self._diagnosisDate

    def getAgeAtDiagnosis(self):
        return self._ageAtDiagnosis

    def getCancerType(self):
        return self._cancerType

    def getClassification(self):
        return self._classification

    def getCancerSite(self):
        return self._cancerSite

    def getHistology(self):
        return self._histology

    def getMethodOfDefinitiveDiagnosis(self):
        return self._methodOfDefinitiveDiagnosis

    def getSampleType(self):
        return self._sampleType

    def getSampleSite(self):
        return self._sampleSite

    def getTumorGrade(self):
        return self._tumorGrade

    def getGradingSystemUsed(self):
        return self._gradingSystemUsed

    def getSitesOfMetastases(self):
        return self._sitesOfMetastases

    def getStagingSystem(self):
        return self._stagingSystem

    def getVersionOrEditionOfTheStagingSystem(self):
        return self._versionOrEditionOfTheStagingSystem

    def getSpecificTumorStageAtDiagnosis(self):
        return self._specificTumorStageAtDiagnosis

    def getPrognosticBiomarkers(self):
        return self._prognosticBiomarkers

    def getBiomarkerQuantification(self):
        return self._biomarkerQuantification

    def getAdditionalMolecularTesting(self):
        return self._additionalMolecularTesting

    def getAdditionalTestType(self):
        return self._additionalTestType

    def getLaboratoryName(self):
        return self._laboratoryName

    def getLaboratoryAddress(self):
        return self._laboratoryAddress

    def getSiteOfMetastases(self):
        return self._siteOfMetastases

    def getStagingSystemVersion(self):
        return self._stagingSystemVersion

    def getSpecificStage(self):
        return self._specificStage

    def getCancerSpecificBiomarkers(self):
        return self._cancerSpecificBiomarkers

    def getAdditionalMolecularDiagnosticTestingPerformed(self):
        return self._additionalMolecularDiagnosticTestingPerformed

    def getAdditionalTest(self):
        return self._additionalTest



class Sample(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.SampleCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Sample, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._sampleId = None
        self._diagnosisId = None
        self._localBiobankId = None
        self._collectionDate = None
        self._collectionHospital = None
        self._sampleType = None
        self._tissueDiseaseState = None
        self._anatomicSiteTheSampleObtainedFrom = None
        self._cancerType = None
        self._cancerSubtype = None
        self._pathologyReportId = None
        self._morphologicalCode = None
        self._topologicalCode = None
        self._shippingDate = None
        self._receivedDate = None
        self._qualityControlPerformed = None
        self._estimatedTumorContent = None
        self._quantity = None
        self._units = None
        self._associatedBiobank = None
        self._otherBiobank = None
        self._sopFollowed = None
        self._ifNotExplainAnyDeviation = None

    def toProtocolElement(self):
        """
        """
        Sample = protocol.Sample(
            id = self.getId(),
            dataset_id = self._datasetId,
            created = self.getCreated(),
            updated = self.getUpdated(),
            name = self.getName(),
            description = self.getDescription(),

            # Unique fields
            patientId = self.getPatientId(),
            sampleId = self.getSampleId(),
            diagnosisId = self.getDiagnosisId(),
            localBiobankId = self.getLocalBiobankId(),
            collectionDate = self.getCollectionDate(),
            collectionHospital = self.getCollectionHospital(),
            sampleType = self.getSampleType(),
            tissueDiseaseState = self.getTissueDiseaseState(),
            anatomicSiteTheSampleObtainedFrom = self.getAnatomicSiteTheSampleObtainedFrom(),
            cancerType = self.getCancerType(),
            cancerSubtype = self.getCancerSubtype(),
            pathologyReportId = self.getPathologyReportId(),
            morphologicalCode = self.getMorphologicalCode(),
            topologicalCode = self.getTopologicalCode(),
            shippingDate = self.getShippingDate(),
            receivedDate = self.getReceivedDate(),
            qualityControlPerformed = self.getQualityControlPerformed(),
            estimatedTumorContent = self.getEstimatedTumorContent(),
            quantity = self.getQuantity(),
            units = self.getUnits(),
            associatedBiobank = self.getAssociatedBiobank(),
            otherBiobank = self.getOtherBiobank(),
            sopFollowed = self.getSopFollowed(),
            ifNotExplainAnyDeviation = self.getIfNotExplainAnyDeviation(),

            )
        self.serializeAttributes(Sample)
        return Sample

    def populateFromRow(self, SampleRecord):
        """
        """
        self._created = SampleRecord.created
        self._updated = SampleRecord.updated
        self._name = SampleRecord.name
        self._description = SampleRecord.description
        self.setAttributesJson(SampleRecord.attributes)

        # Unique fields
        self._patientId = SampleRecord.patientId
        self._sampleId = SampleRecord.sampleId
        self._diagnosisId = SampleRecord.diagnosisId
        self._localBiobankId = SampleRecord.localBiobankId
        self._collectionDate = SampleRecord.collectionDate
        self._collectionHospital = SampleRecord.collectionHospital
        self._sampleType = SampleRecord.sampleType
        self._tissueDiseaseState = SampleRecord.tissueDiseaseState
        self._anatomicSiteTheSampleObtainedFrom = SampleRecord.anatomicSiteTheSampleObtainedFrom
        self._cancerType = SampleRecord.cancerType
        self._cancerSubtype = SampleRecord.cancerSubtype
        self._pathologyReportId = SampleRecord.pathologyReportId
        self._morphologicalCode = SampleRecord.morphologicalCode
        self._topologicalCode = SampleRecord.topologicalCode
        self._shippingDate = SampleRecord.shippingDate
        self._receivedDate = SampleRecord.receivedDate
        self._qualityControlPerformed = SampleRecord.qualityControlPerformed
        self._estimatedTumorContent = SampleRecord.estimatedTumorContent
        self._quantity = SampleRecord.quantity
        self._units = SampleRecord.units
        self._associatedBiobank = SampleRecord.associatedBiobank
        self._otherBiobank = SampleRecord.otherBiobank
        self._sopFollowed = SampleRecord.sopFollowed
        self._ifNotExplainAnyDeviation = SampleRecord.ifNotExplainAnyDeviation

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Sample)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._sampleId = parsed.sampleId
        self._diagnosisId = parsed.diagnosisId
        self._localBiobankId = parsed.localBiobankId
        self._collectionDate = parsed.collectionDate
        self._collectionHospital = parsed.collectionHospital
        self._sampleType = parsed.sampleType
        self._tissueDiseaseState = parsed.tissueDiseaseState
        self._anatomicSiteTheSampleObtainedFrom = parsed.anatomicSiteTheSampleObtainedFrom
        self._cancerType = parsed.cancerType
        self._cancerSubtype = parsed.cancerSubtype
        self._pathologyReportId = parsed.pathologyReportId
        self._morphologicalCode = parsed.morphologicalCode
        self._topologicalCode = parsed.topologicalCode
        self._shippingDate = parsed.shippingDate
        self._receivedDate = parsed.receivedDate
        self._qualityControlPerformed = parsed.qualityControlPerformed
        self._estimatedTumorContent = parsed.estimatedTumorContent
        self._quantity = parsed.quantity
        self._units = parsed.units
        self._associatedBiobank = parsed.associatedBiobank
        self._otherBiobank = parsed.otherBiobank
        self._sopFollowed = parsed.sopFollowed
        self._ifNotExplainAnyDeviation = parsed.ifNotExplainAnyDeviation

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    # Unique field getters

    def getPatientId(self):
        return self._patientId

    def getSampleId(self):
        return self._sampleId

    def getDiagnosisId(self):
        return self._diagnosisId

    def getLocalBiobankId(self):
        return self._localBiobankId

    def getCollectionDate(self):
        return self._collectionDate

    def getCollectionHospital(self):
        return self._collectionHospital

    def getSampleType(self):
        return self._sampleType

    def getTissueDiseaseState(self):
        return self._tissueDiseaseState

    def getAnatomicSiteTheSampleObtainedFrom(self):
        return self._anatomicSiteTheSampleObtainedFrom

    def getCancerType(self):
        return self._cancerType

    def getCancerSubtype(self):
        return self._cancerSubtype

    def getPathologyReportId(self):
        return self._pathologyReportId

    def getMorphologicalCode(self):
        return self._morphologicalCode

    def getTopologicalCode(self):
        return self._topologicalCode

    def getShippingDate(self):
        return self._shippingDate

    def getReceivedDate(self):
        return self._receivedDate

    def getQualityControlPerformed(self):
        return self._qualityControlPerformed

    def getEstimatedTumorContent(self):
        return self._estimatedTumorContent

    def getQuantity(self):
        return self._quantity

    def getUnits(self):
        return self._units

    def getAssociatedBiobank(self):
        return self._associatedBiobank

    def getOtherBiobank(self):
        return self._otherBiobank

    def getSopFollowed(self):
        return self._sopFollowed

    def getIfNotExplainAnyDeviation(self):
        return self._ifNotExplainAnyDeviation



class Treatment(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.TreatmentCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Treatment, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._courseNumber = None
        self._therapeuticModality = None
        self._systematicTherapyAgentName = None
        self._treatmentPlanType = None
        self._treatmentIntent = None
        self._startDate = None
        self._stopDate = None
        self._reasonForEndingTheTreatment = None
        self._protocolNumberOrCode = None
        self._surgeryDetails = None
        self._radiotherapyDetails = None
        self._chemotherapyDetails = None
        self._hematopoieticCellTransplant = None
        self._immunotherapyDetails = None
        self._responseToTreatment = None
        self._responseCriteriaUsed = None
        self._dateOfRecurrenceOrProgressionAfterThisTreatment = None
        self._unexpectedOrUnusualToxicityDuringTreatment = None
        self._drugListOrAgent = None
        self._drugIdNumbers = None

    def toProtocolElement(self):
        """
        """
        Treatment = protocol.Treatment(
            id = self.getId(),
            dataset_id = self._datasetId,
            created = self.getCreated(),
            updated = self.getUpdated(),
            name = self.getName(),
            description = self.getDescription(),

            # Unique fields
            patientId = self.getPatientId(),
            courseNumber = self.getCourseNumber(),
            therapeuticModality = self.getTherapeuticModality(),
            systematicTherapyAgentName = self.getSystematicTherapyAgentName(),
            treatmentPlanType = self.getTreatmentPlanType(),
            treatmentIntent = self.getTreatmentIntent(),
            startDate = self.getStartDate(),
            stopDate = self.getStopDate(),
            reasonForEndingTheTreatment = self.getReasonForEndingTheTreatment(),
            protocolNumberOrCode = self.getProtocolNumberOrCode(),
            surgeryDetails = self.getSurgeryDetails(),
            radiotherapyDetails = self.getRadiotherapyDetails(),
            chemotherapyDetails = self.getChemotherapyDetails(),
            hematopoieticCellTransplant = self.getHematopoieticCellTransplant(),
            immunotherapyDetails = self.getImmunotherapyDetails(),
            responseToTreatment = self.getResponseToTreatment(),
            responseCriteriaUsed = self.getResponseCriteriaUsed(),
            dateOfRecurrenceOrProgressionAfterThisTreatment = self.getDateOfRecurrenceOrProgressionAfterThisTreatment(),
            unexpectedOrUnusualToxicityDuringTreatment = self.getUnexpectedOrUnusualToxicityDuringTreatment(),
            drugListOrAgent = self.getDrugListOrAgent(),
            drugIdNumbers = self.getDrugIdNumbers(),

            )
        self.serializeAttributes(Treatment)
        return Treatment

    def populateFromRow(self, TreatmentRecord):
        """
        """
        self._created = TreatmentRecord.created
        self._updated = TreatmentRecord.updated
        self._name = TreatmentRecord.name
        self._description = TreatmentRecord.description
        self.setAttributesJson(TreatmentRecord.attributes)

        # Unique fields
        self._patientId = TreatmentRecord.patientId
        self._courseNumber = TreatmentRecord.courseNumber
        self._therapeuticModality = TreatmentRecord.therapeuticModality
        self._systematicTherapyAgentName = TreatmentRecord.systematicTherapyAgentName
        self._treatmentPlanType = TreatmentRecord.treatmentPlanType
        self._treatmentIntent = TreatmentRecord.treatmentIntent
        self._startDate = TreatmentRecord.startDate
        self._stopDate = TreatmentRecord.stopDate
        self._reasonForEndingTheTreatment = TreatmentRecord.reasonForEndingTheTreatment
        self._protocolNumberOrCode = TreatmentRecord.protocolNumberOrCode
        self._surgeryDetails = TreatmentRecord.surgeryDetails
        self._radiotherapyDetails = TreatmentRecord.radiotherapyDetails
        self._chemotherapyDetails = TreatmentRecord.chemotherapyDetails
        self._hematopoieticCellTransplant = TreatmentRecord.hematopoieticCellTransplant
        self._immunotherapyDetails = TreatmentRecord.immunotherapyDetails
        self._responseToTreatment = TreatmentRecord.responseToTreatment
        self._responseCriteriaUsed = TreatmentRecord.responseCriteriaUsed
        self._dateOfRecurrenceOrProgressionAfterThisTreatment = TreatmentRecord.dateOfRecurrenceOrProgressionAfterThisTreatment
        self._unexpectedOrUnusualToxicityDuringTreatment = TreatmentRecord.unexpectedOrUnusualToxicityDuringTreatment
        self._drugListOrAgent = TreatmentRecord.drugListOrAgent
        self._drugIdNumbers = TreatmentRecord.drugIdNumbers

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Treatment)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._courseNumber = parsed.courseNumber
        self._therapeuticModality = parsed.therapeuticModality
        self._systematicTherapyAgentName = parsed.systematicTherapyAgentName
        self._treatmentPlanType = parsed.treatmentPlanType
        self._treatmentIntent = parsed.treatmentIntent
        self._startDate = parsed.startDate
        self._stopDate = parsed.stopDate
        self._reasonForEndingTheTreatment = parsed.reasonForEndingTheTreatment
        self._protocolNumberOrCode = parsed.protocolNumberOrCode
        self._surgeryDetails = parsed.surgeryDetails
        self._radiotherapyDetails = parsed.radiotherapyDetails
        self._chemotherapyDetails = parsed.chemotherapyDetails
        self._hematopoieticCellTransplant = parsed.hematopoieticCellTransplant
        self._immunotherapyDetails = parsed.immunotherapyDetails
        self._responseToTreatment = parsed.responseToTreatment
        self._responseCriteriaUsed = parsed.responseCriteriaUsed
        self._dateOfRecurrenceOrProgressionAfterThisTreatment = parsed.dateOfRecurrenceOrProgressionAfterThisTreatment
        self._unexpectedOrUnusualToxicityDuringTreatment = parsed.unexpectedOrUnusualToxicityDuringTreatment
        self._drugListOrAgent = parsed.drugListOrAgent
        self._drugIdNumbers = parsed.drugIdNumbers

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    # Unique field getters

    def getPatientId(self):
        return self._patientId

    def getCourseNumber(self):
        return self._courseNumber

    def getTherapeuticModality(self):
        return self._therapeuticModality

    def getSystematicTherapyAgentName(self):
        return self._systematicTherapyAgentName

    def getTreatmentPlanType(self):
        return self._treatmentPlanType

    def getTreatmentIntent(self):
        return self._treatmentIntent

    def getStartDate(self):
        return self._startDate

    def getStopDate(self):
        return self._stopDate

    def getReasonForEndingTheTreatment(self):
        return self._reasonForEndingTheTreatment

    def getProtocolNumberOrCode(self):
        return self._protocolNumberOrCode

    def getSurgeryDetails(self):
        return self._surgeryDetails

    def getRadiotherapyDetails(self):
        return self._radiotherapyDetails

    def getChemotherapyDetails(self):
        return self._chemotherapyDetails

    def getHematopoieticCellTransplant(self):
        return self._hematopoieticCellTransplant

    def getImmunotherapyDetails(self):
        return self._immunotherapyDetails

    def getResponseToTreatment(self):
        return self._responseToTreatment

    def getResponseCriteriaUsed(self):
        return self._responseCriteriaUsed

    def getDateOfRecurrenceOrProgressionAfterThisTreatment(self):
        return self._dateOfRecurrenceOrProgressionAfterThisTreatment

    def getUnexpectedOrUnusualToxicityDuringTreatment(self):
        return self._unexpectedOrUnusualToxicityDuringTreatment

    def getDrugListOrAgent(self):
        return self._drugListOrAgent

    def getDrugIdNumbers(self):
        return self._drugIdNumbers



class Outcome(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.OutcomeCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Outcome, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._physicalExamId = None
        self._dateOfAssessment = None
        self._diseaseResponseOrStatus = None
        self._otherResponseClassification = None
        self._minimalResidualDiseaseAssessment = None
        self._methodOfResponseEvaluation = None
        self._responseCriteriaUsed = None
        self._summaryStage = None
        self._sitesOfAnyProgressionOrRecurrence = None
        self._vitalStatus = None
        self._height = None
        self._weight = None
        self._heightUnits = None
        self._weightUnits = None
        self._performanceStatus = None

    def toProtocolElement(self):
        """
        """
        Outcome = protocol.Outcome(
            id = self.getId(),
            dataset_id = self._datasetId,
            created = self.getCreated(),
            updated = self.getUpdated(),
            name = self.getName(),
            description = self.getDescription(),

            # Unique fields
            patientId = self.getPatientId(),
            physicalExamId = self.getPhysicalExamId(),
            dateOfAssessment = self.getDateOfAssessment(),
            diseaseResponseOrStatus = self.getDiseaseResponseOrStatus(),
            otherResponseClassification = self.getOtherResponseClassification(),
            minimalResidualDiseaseAssessment = self.getMinimalResidualDiseaseAssessment(),
            methodOfResponseEvaluation = self.getMethodOfResponseEvaluation(),
            responseCriteriaUsed = self.getResponseCriteriaUsed(),
            summaryStage = self.getSummaryStage(),
            sitesOfAnyProgressionOrRecurrence = self.getSitesOfAnyProgressionOrRecurrence(),
            vitalStatus = self.getVitalStatus(),
            height = self.getHeight(),
            weight = self.getWeight(),
            heightUnits = self.getHeightUnits(),
            weightUnits = self.getWeightUnits(),
            performanceStatus = self.getPerformanceStatus(),

            )
        self.serializeAttributes(Outcome)
        return Outcome

    def populateFromRow(self, OutcomeRecord):
        """
        """
        self._created = OutcomeRecord.created
        self._updated = OutcomeRecord.updated
        self._name = OutcomeRecord.name
        self._description = OutcomeRecord.description
        self.setAttributesJson(OutcomeRecord.attributes)

        # Unique fields
        self._patientId = OutcomeRecord.patientId
        self._physicalExamId = OutcomeRecord.physicalExamId
        self._dateOfAssessment = OutcomeRecord.dateOfAssessment
        self._diseaseResponseOrStatus = OutcomeRecord.diseaseResponseOrStatus
        self._otherResponseClassification = OutcomeRecord.otherResponseClassification
        self._minimalResidualDiseaseAssessment = OutcomeRecord.minimalResidualDiseaseAssessment
        self._methodOfResponseEvaluation = OutcomeRecord.methodOfResponseEvaluation
        self._responseCriteriaUsed = OutcomeRecord.responseCriteriaUsed
        self._summaryStage = OutcomeRecord.summaryStage
        self._sitesOfAnyProgressionOrRecurrence = OutcomeRecord.sitesOfAnyProgressionOrRecurrence
        self._vitalStatus = OutcomeRecord.vitalStatus
        self._height = OutcomeRecord.height
        self._weight = OutcomeRecord.weight
        self._heightUnits = OutcomeRecord.heightUnits
        self._weightUnits = OutcomeRecord.weightUnits
        self._performanceStatus = OutcomeRecord.performanceStatus

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Outcome)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._physicalExamId = parsed.physicalExamId
        self._dateOfAssessment = parsed.dateOfAssessment
        self._diseaseResponseOrStatus = parsed.diseaseResponseOrStatus
        self._otherResponseClassification = parsed.otherResponseClassification
        self._minimalResidualDiseaseAssessment = parsed.minimalResidualDiseaseAssessment
        self._methodOfResponseEvaluation = parsed.methodOfResponseEvaluation
        self._responseCriteriaUsed = parsed.responseCriteriaUsed
        self._summaryStage = parsed.summaryStage
        self._sitesOfAnyProgressionOrRecurrence = parsed.sitesOfAnyProgressionOrRecurrence
        self._vitalStatus = parsed.vitalStatus
        self._height = parsed.height
        self._weight = parsed.weight
        self._heightUnits = parsed.heightUnits
        self._weightUnits = parsed.weightUnits
        self._performanceStatus = parsed.performanceStatus

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    # Unique field getters

    def getPatientId(self):
        return self._patientId

    def getPhysicalExamId(self):
        return self._physicalExamId

    def getDateOfAssessment(self):
        return self._dateOfAssessment

    def getDiseaseResponseOrStatus(self):
        return self._diseaseResponseOrStatus

    def getOtherResponseClassification(self):
        return self._otherResponseClassification

    def getMinimalResidualDiseaseAssessment(self):
        return self._minimalResidualDiseaseAssessment

    def getMethodOfResponseEvaluation(self):
        return self._methodOfResponseEvaluation

    def getResponseCriteriaUsed(self):
        return self._responseCriteriaUsed

    def getSummaryStage(self):
        return self._summaryStage

    def getSitesOfAnyProgressionOrRecurrence(self):
        return self._sitesOfAnyProgressionOrRecurrence

    def getVitalStatus(self):
        return self._vitalStatus

    def getHeight(self):
        return self._height

    def getWeight(self):
        return self._weight

    def getHeightUnits(self):
        return self._heightUnits

    def getWeightUnits(self):
        return self._weightUnits

    def getPerformanceStatus(self):
        return self._performanceStatus



class Complication(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.ComplicationCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Complication, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._date = None
        self._lateComplicationOfTherapyDeveloped = None
        self._lateToxicityDetail = None
        self._suspectedTreatmentInducedNeoplasmDeveloped = None
        self._treatmentInducedNeoplasmDetails = None

    def toProtocolElement(self):
        """
        """
        Complication = protocol.Complication(
            id = self.getId(),
            dataset_id = self._datasetId,
            created = self.getCreated(),
            updated = self.getUpdated(),
            name = self.getName(),
            description = self.getDescription(),

            # Unique fields
            patientId = self.getPatientId(),
            date = self.getDate(),
            lateComplicationOfTherapyDeveloped = self.getLateComplicationOfTherapyDeveloped(),
            lateToxicityDetail = self.getLateToxicityDetail(),
            suspectedTreatmentInducedNeoplasmDeveloped = self.getSuspectedTreatmentInducedNeoplasmDeveloped(),
            treatmentInducedNeoplasmDetails = self.getTreatmentInducedNeoplasmDetails(),

            )
        self.serializeAttributes(Complication)
        return Complication

    def populateFromRow(self, ComplicationRecord):
        """
        """
        self._created = ComplicationRecord.created
        self._updated = ComplicationRecord.updated
        self._name = ComplicationRecord.name
        self._description = ComplicationRecord.description
        self.setAttributesJson(ComplicationRecord.attributes)

        # Unique fields
        self._patientId = ComplicationRecord.patientId
        self._date = ComplicationRecord.date
        self._lateComplicationOfTherapyDeveloped = ComplicationRecord.lateComplicationOfTherapyDeveloped
        self._lateToxicityDetail = ComplicationRecord.lateToxicityDetail
        self._suspectedTreatmentInducedNeoplasmDeveloped = ComplicationRecord.suspectedTreatmentInducedNeoplasmDeveloped
        self._treatmentInducedNeoplasmDetails = ComplicationRecord.treatmentInducedNeoplasmDetails

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Complication)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._date = parsed.date
        self._lateComplicationOfTherapyDeveloped = parsed.lateComplicationOfTherapyDeveloped
        self._lateToxicityDetail = parsed.lateToxicityDetail
        self._suspectedTreatmentInducedNeoplasmDeveloped = parsed.suspectedTreatmentInducedNeoplasmDeveloped
        self._treatmentInducedNeoplasmDetails = parsed.treatmentInducedNeoplasmDetails

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    # Unique field getters

    def getPatientId(self):
        return self._patientId

    def getDate(self):
        return self._date

    def getLateComplicationOfTherapyDeveloped(self):
        return self._lateComplicationOfTherapyDeveloped

    def getLateToxicityDetail(self):
        return self._lateToxicityDetail

    def getSuspectedTreatmentInducedNeoplasmDeveloped(self):
        return self._suspectedTreatmentInducedNeoplasmDeveloped

    def getTreatmentInducedNeoplasmDetails(self):
        return self._treatmentInducedNeoplasmDetails



class Tumourboard(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.TumourboardCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Tumourboard, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._dateOfMolecularTumorBoard = None
        self._typeOfSampleAnalyzed = None
        self._typeOfTumourSampleAnalyzed = None
        self._analysesDiscussed = None
        self._somaticSampleType = None
        self._normalExpressionComparator = None
        self._diseaseExpressionComparator = None
        self._hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer = None
        self._actionableTargetFound = None
        self._molecularTumorBoardRecommendation = None
        self._germlineDnaSampleId = None
        self._tumorDnaSampleId = None
        self._tumorRnaSampleId = None
        self._germlineSnvDiscussed = None
        self._somaticSnvDiscussed = None
        self._cnvsDiscussed = None
        self._structuralVariantDiscussed = None
        self._classificationOfVariants = None
        self._clinicalValidationProgress = None
        self._typeOfValidation = None
        self._agentOrDrugClass = None
        self._levelOfEvidenceForExpressionTargetAgentMatch = None
        self._didTreatmentPlanChangeBasedOnProfilingResult = None
        self._howTreatmentHasAlteredBasedOnProfiling = None
        self._reasonTreatmentPlanDidNotChangeBasedOnProfiling = None
        self._detailsOfTreatmentPlanImpact = None
        self._patientOrFamilyInformedOfGermlineVariant = None
        self._patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling = None
        self._summaryReport = None

    def toProtocolElement(self):
        """
        """
        Tumourboard = protocol.Tumourboard(
            id = self.getId(),
            dataset_id = self._datasetId,
            created = self.getCreated(),
            updated = self.getUpdated(),
            name = self.getName(),
            description = self.getDescription(),

            # Unique fields
            patientId = self.getPatientId(),
            dateOfMolecularTumorBoard = self.getDateOfMolecularTumorBoard(),
            typeOfSampleAnalyzed = self.getTypeOfSampleAnalyzed(),
            typeOfTumourSampleAnalyzed = self.getTypeOfTumourSampleAnalyzed(),
            analysesDiscussed = self.getAnalysesDiscussed(),
            somaticSampleType = self.getSomaticSampleType(),
            normalExpressionComparator = self.getNormalExpressionComparator(),
            diseaseExpressionComparator = self.getDiseaseExpressionComparator(),
            hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer = self.getHasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer(),
            actionableTargetFound = self.getActionableTargetFound(),
            molecularTumorBoardRecommendation = self.getMolecularTumorBoardRecommendation(),
            germlineDnaSampleId = self.getGermlineDnaSampleId(),
            tumorDnaSampleId = self.getTumorDnaSampleId(),
            tumorRnaSampleId = self.getTumorRnaSampleId(),
            germlineSnvDiscussed = self.getGermlineSnvDiscussed(),
            somaticSnvDiscussed = self.getSomaticSnvDiscussed(),
            cnvsDiscussed = self.getCnvsDiscussed(),
            structuralVariantDiscussed = self.getStructuralVariantDiscussed(),
            classificationOfVariants = self.getClassificationOfVariants(),
            clinicalValidationProgress = self.getClinicalValidationProgress(),
            typeOfValidation = self.getTypeOfValidation(),
            agentOrDrugClass = self.getAgentOrDrugClass(),
            levelOfEvidenceForExpressionTargetAgentMatch = self.getLevelOfEvidenceForExpressionTargetAgentMatch(),
            didTreatmentPlanChangeBasedOnProfilingResult = self.getDidTreatmentPlanChangeBasedOnProfilingResult(),
            howTreatmentHasAlteredBasedOnProfiling = self.getHowTreatmentHasAlteredBasedOnProfiling(),
            reasonTreatmentPlanDidNotChangeBasedOnProfiling = self.getReasonTreatmentPlanDidNotChangeBasedOnProfiling(),
            detailsOfTreatmentPlanImpact = self.getDetailsOfTreatmentPlanImpact(),
            patientOrFamilyInformedOfGermlineVariant = self.getPatientOrFamilyInformedOfGermlineVariant(),
            patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling = self.getPatientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling(),
            summaryReport = self.getSummaryReport(),

            )
        self.serializeAttributes(Tumourboard)
        return Tumourboard

    def populateFromRow(self, TumourboardRecord):
        """
        """
        self._created = TumourboardRecord.created
        self._updated = TumourboardRecord.updated
        self._name = TumourboardRecord.name
        self._description = TumourboardRecord.description
        self.setAttributesJson(TumourboardRecord.attributes)

        # Unique fields
        self._patientId = TumourboardRecord.patientId
        self._dateOfMolecularTumorBoard = TumourboardRecord.dateOfMolecularTumorBoard
        self._typeOfSampleAnalyzed = TumourboardRecord.typeOfSampleAnalyzed
        self._typeOfTumourSampleAnalyzed = TumourboardRecord.typeOfTumourSampleAnalyzed
        self._analysesDiscussed = TumourboardRecord.analysesDiscussed
        self._somaticSampleType = TumourboardRecord.somaticSampleType
        self._normalExpressionComparator = TumourboardRecord.normalExpressionComparator
        self._diseaseExpressionComparator = TumourboardRecord.diseaseExpressionComparator
        self._hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer = TumourboardRecord.hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer
        self._actionableTargetFound = TumourboardRecord.actionableTargetFound
        self._molecularTumorBoardRecommendation = TumourboardRecord.molecularTumorBoardRecommendation
        self._germlineDnaSampleId = TumourboardRecord.germlineDnaSampleId
        self._tumorDnaSampleId = TumourboardRecord.tumorDnaSampleId
        self._tumorRnaSampleId = TumourboardRecord.tumorRnaSampleId
        self._germlineSnvDiscussed = TumourboardRecord.germlineSnvDiscussed
        self._somaticSnvDiscussed = TumourboardRecord.somaticSnvDiscussed
        self._cnvsDiscussed = TumourboardRecord.cnvsDiscussed
        self._structuralVariantDiscussed = TumourboardRecord.structuralVariantDiscussed
        self._classificationOfVariants = TumourboardRecord.classificationOfVariants
        self._clinicalValidationProgress = TumourboardRecord.clinicalValidationProgress
        self._typeOfValidation = TumourboardRecord.typeOfValidation
        self._agentOrDrugClass = TumourboardRecord.agentOrDrugClass
        self._levelOfEvidenceForExpressionTargetAgentMatch = TumourboardRecord.levelOfEvidenceForExpressionTargetAgentMatch
        self._didTreatmentPlanChangeBasedOnProfilingResult = TumourboardRecord.didTreatmentPlanChangeBasedOnProfilingResult
        self._howTreatmentHasAlteredBasedOnProfiling = TumourboardRecord.howTreatmentHasAlteredBasedOnProfiling
        self._reasonTreatmentPlanDidNotChangeBasedOnProfiling = TumourboardRecord.reasonTreatmentPlanDidNotChangeBasedOnProfiling
        self._detailsOfTreatmentPlanImpact = TumourboardRecord.detailsOfTreatmentPlanImpact
        self._patientOrFamilyInformedOfGermlineVariant = TumourboardRecord.patientOrFamilyInformedOfGermlineVariant
        self._patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling = TumourboardRecord.patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling
        self._summaryReport = TumourboardRecord.summaryReport

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Tumourboard)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._dateOfMolecularTumorBoard = parsed.dateOfMolecularTumorBoard
        self._typeOfSampleAnalyzed = parsed.typeOfSampleAnalyzed
        self._typeOfTumourSampleAnalyzed = parsed.typeOfTumourSampleAnalyzed
        self._analysesDiscussed = parsed.analysesDiscussed
        self._somaticSampleType = parsed.somaticSampleType
        self._normalExpressionComparator = parsed.normalExpressionComparator
        self._diseaseExpressionComparator = parsed.diseaseExpressionComparator
        self._hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer = parsed.hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer
        self._actionableTargetFound = parsed.actionableTargetFound
        self._molecularTumorBoardRecommendation = parsed.molecularTumorBoardRecommendation
        self._germlineDnaSampleId = parsed.germlineDnaSampleId
        self._tumorDnaSampleId = parsed.tumorDnaSampleId
        self._tumorRnaSampleId = parsed.tumorRnaSampleId
        self._germlineSnvDiscussed = parsed.germlineSnvDiscussed
        self._somaticSnvDiscussed = parsed.somaticSnvDiscussed
        self._cnvsDiscussed = parsed.cnvsDiscussed
        self._structuralVariantDiscussed = parsed.structuralVariantDiscussed
        self._classificationOfVariants = parsed.classificationOfVariants
        self._clinicalValidationProgress = parsed.clinicalValidationProgress
        self._typeOfValidation = parsed.typeOfValidation
        self._agentOrDrugClass = parsed.agentOrDrugClass
        self._levelOfEvidenceForExpressionTargetAgentMatch = parsed.levelOfEvidenceForExpressionTargetAgentMatch
        self._didTreatmentPlanChangeBasedOnProfilingResult = parsed.didTreatmentPlanChangeBasedOnProfilingResult
        self._howTreatmentHasAlteredBasedOnProfiling = parsed.howTreatmentHasAlteredBasedOnProfiling
        self._reasonTreatmentPlanDidNotChangeBasedOnProfiling = parsed.reasonTreatmentPlanDidNotChangeBasedOnProfiling
        self._detailsOfTreatmentPlanImpact = parsed.detailsOfTreatmentPlanImpact
        self._patientOrFamilyInformedOfGermlineVariant = parsed.patientOrFamilyInformedOfGermlineVariant
        self._patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling = parsed.patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling
        self._summaryReport = parsed.summaryReport

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    # Unique field getters

    def getPatientId(self):
        return self._patientId

    def getDateOfMolecularTumorBoard(self):
        return self._dateOfMolecularTumorBoard

    def getTypeOfSampleAnalyzed(self):
        return self._typeOfSampleAnalyzed

    def getTypeOfTumourSampleAnalyzed(self):
        return self._typeOfTumourSampleAnalyzed

    def getAnalysesDiscussed(self):
        return self._analysesDiscussed

    def getSomaticSampleType(self):
        return self._somaticSampleType

    def getNormalExpressionComparator(self):
        return self._normalExpressionComparator

    def getDiseaseExpressionComparator(self):
        return self._diseaseExpressionComparator

    def getHasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer(self):
        return self._hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer

    def getActionableTargetFound(self):
        return self._actionableTargetFound

    def getMolecularTumorBoardRecommendation(self):
        return self._molecularTumorBoardRecommendation

    def getGermlineDnaSampleId(self):
        return self._germlineDnaSampleId

    def getTumorDnaSampleId(self):
        return self._tumorDnaSampleId

    def getTumorRnaSampleId(self):
        return self._tumorRnaSampleId

    def getGermlineSnvDiscussed(self):
        return self._germlineSnvDiscussed

    def getSomaticSnvDiscussed(self):
        return self._somaticSnvDiscussed

    def getCnvsDiscussed(self):
        return self._cnvsDiscussed

    def getStructuralVariantDiscussed(self):
        return self._structuralVariantDiscussed

    def getClassificationOfVariants(self):
        return self._classificationOfVariants

    def getClinicalValidationProgress(self):
        return self._clinicalValidationProgress

    def getTypeOfValidation(self):
        return self._typeOfValidation

    def getAgentOrDrugClass(self):
        return self._agentOrDrugClass

    def getLevelOfEvidenceForExpressionTargetAgentMatch(self):
        return self._levelOfEvidenceForExpressionTargetAgentMatch

    def getDidTreatmentPlanChangeBasedOnProfilingResult(self):
        return self._didTreatmentPlanChangeBasedOnProfilingResult

    def getHowTreatmentHasAlteredBasedOnProfiling(self):
        return self._howTreatmentHasAlteredBasedOnProfiling

    def getReasonTreatmentPlanDidNotChangeBasedOnProfiling(self):
        return self._reasonTreatmentPlanDidNotChangeBasedOnProfiling

    def getDetailsOfTreatmentPlanImpact(self):
        return self._detailsOfTreatmentPlanImpact

    def getPatientOrFamilyInformedOfGermlineVariant(self):
        return self._patientOrFamilyInformedOfGermlineVariant

    def getPatientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling(self):
        return self._patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling

    def getSummaryReport(self):
        return self._summaryReport

