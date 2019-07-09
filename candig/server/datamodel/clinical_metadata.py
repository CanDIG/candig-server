"""
CanDIG - 2018-03-05

Clinical metadata objects

"""

import datetime
# import json

import candig.server.datamodel as datamodel
import candig.server.exceptions as exceptions

import candig.schemas.protocol as protocol


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
        self._patientIdTier = None
        self._otherIds = None
        self._otherIdsTier = None
        self._dateOfBirth = None
        self._dateOfBirthTier = None
        self._gender = None
        self._genderTier = None
        self._ethnicity = None
        self._ethnicityTier = None
        self._race = None
        self._raceTier = None
        self._provinceOfResidence = None
        self._provinceOfResidenceTier = None
        self._dateOfDeath = None
        self._dateOfDeathTier = None
        self._causeOfDeath = None
        self._causeOfDeathTier = None
        self._autopsyTissueForResearch = None
        self._autopsyTissueForResearchTier = None
        self._priorMalignancy = None
        self._priorMalignancyTier = None
        self._dateOfPriorMalignancy = None
        self._dateOfPriorMalignancyTier = None
        self._familyHistoryAndRiskFactors = None
        self._familyHistoryAndRiskFactorsTier = None
        self._familyHistoryOfPredispositionSyndrome = None
        self._familyHistoryOfPredispositionSyndromeTier = None
        self._detailsOfPredispositionSyndrome = None
        self._detailsOfPredispositionSyndromeTier = None
        self._geneticCancerSyndrome = None
        self._geneticCancerSyndromeTier = None
        self._otherGeneticConditionOrSignificantComorbidity = None
        self._otherGeneticConditionOrSignificantComorbidityTier = None
        self._occupationalOrEnvironmentalExposure = None
        self._occupationalOrEnvironmentalExposureTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "otherIds": self.getOtherIds,
            "dateOfBirth": self.getDateOfBirth,
            "gender": self.getGender,
            "ethnicity": self.getEthnicity,
            "race": self.getRace,
            "provinceOfResidence": self.getProvinceOfResidence,
            "dateOfDeath": self.getDateOfDeath,
            "causeOfDeath": self.getCauseOfDeath,
            "autopsyTissueForResearch": self.getAutopsyTissueForResearch,
            "priorMalignancy": self.getPriorMalignancy,
            "dateOfPriorMalignancy": self.getDateOfPriorMalignancy,
            "familyHistoryAndRiskFactors": self.getFamilyHistoryAndRiskFactors,
            "familyHistoryOfPredispositionSyndrome": self.getFamilyHistoryOfPredispositionSyndrome,
            "detailsOfPredispositionSyndrome": self.getDetailsOfPredispositionSyndrome,
            "geneticCancerSyndrome": self.getGeneticCancerSyndrome,
            "otherGeneticConditionOrSignificantComorbidity": self.getOtherGeneticConditionOrSignificantComorbidity,
            "occupationalOrEnvironmentalExposure": self.getOccupationalOrEnvironmentalExposure,
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        try:
            # Unique fields
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getOtherIdsTier():
                record['otherIds'] = self.getOtherIds()
            if tier >= self.getDateOfBirthTier():
                record['dateOfBirth'] = self.getDateOfBirth()
            if tier >= self.getGenderTier():
                record['gender'] = self.getGender()
            if tier >= self.getEthnicityTier():
                record['ethnicity'] = self.getEthnicity()
            if tier >= self.getRaceTier():
                record['race'] = self.getRace()
            if tier >= self.getProvinceOfResidenceTier():
                record['provinceOfResidence'] = self.getProvinceOfResidence()
            if tier >= self.getDateOfDeathTier():
                record['dateOfDeath'] = self.getDateOfDeath()
            if tier >= self.getCauseOfDeathTier():
                record['causeOfDeath'] = self.getCauseOfDeath()
            if tier >= self.getAutopsyTissueForResearchTier():
                record['autopsyTissueForResearch'] = self.getAutopsyTissueForResearch()
            if tier >= self.getPriorMalignancyTier():
                record['priorMalignancy'] = self.getPriorMalignancy()
            if tier >= self.getDateOfPriorMalignancyTier():
                record['dateOfPriorMalignancy'] = self.getDateOfPriorMalignancy()
            if tier >= self.getFamilyHistoryAndRiskFactorsTier():
                record['familyHistoryAndRiskFactors'] = self.getFamilyHistoryAndRiskFactors()
            if tier >= self.getFamilyHistoryOfPredispositionSyndromeTier():
                record['familyHistoryOfPredispositionSyndrome'] = self.getFamilyHistoryOfPredispositionSyndrome()
            if tier >= self.getDetailsOfPredispositionSyndromeTier():
                record['detailsOfPredispositionSyndrome'] = self.getDetailsOfPredispositionSyndrome()
            if tier >= self.getGeneticCancerSyndromeTier():
                record['geneticCancerSyndrome'] = self.getGeneticCancerSyndrome()
            if tier >= self.getOtherGeneticConditionOrSignificantComorbidityTier():
                record['otherGeneticConditionOrSignificantComorbidity'] = self.getOtherGeneticConditionOrSignificantComorbidity()
            if tier >= self.getOccupationalOrEnvironmentalExposureTier():
                record['occupationalOrEnvironmentalExposure'] = self.getOccupationalOrEnvironmentalExposure()
        except TypeError:
            pass

        Patient = protocol.Patient(**record)
        self.serializeMetadataAttributes(Patient)

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
        self._patientIdTier = PatientRecord.patientIdTier
        self._otherIds = PatientRecord.otherIds
        self._otherIdsTier = PatientRecord.otherIdsTier
        self._dateOfBirth = PatientRecord.dateOfBirth
        self._dateOfBirthTier = PatientRecord.dateOfBirthTier
        self._gender = PatientRecord.gender
        self._genderTier = PatientRecord.genderTier
        self._ethnicity = PatientRecord.ethnicity
        self._ethnicityTier = PatientRecord.ethnicityTier
        self._race = PatientRecord.race
        self._raceTier = PatientRecord.raceTier
        self._provinceOfResidence = PatientRecord.provinceOfResidence
        self._provinceOfResidenceTier = PatientRecord.provinceOfResidenceTier
        self._dateOfDeath = PatientRecord.dateOfDeath
        self._dateOfDeathTier = PatientRecord.dateOfDeathTier
        self._causeOfDeath = PatientRecord.causeOfDeath
        self._causeOfDeathTier = PatientRecord.causeOfDeathTier
        self._autopsyTissueForResearch = PatientRecord.autopsyTissueForResearch
        self._autopsyTissueForResearchTier = PatientRecord.autopsyTissueForResearchTier
        self._priorMalignancy = PatientRecord.priorMalignancy
        self._priorMalignancyTier = PatientRecord.priorMalignancyTier
        self._dateOfPriorMalignancy = PatientRecord.dateOfPriorMalignancy
        self._dateOfPriorMalignancyTier = PatientRecord.dateOfPriorMalignancyTier
        self._familyHistoryAndRiskFactors = PatientRecord.familyHistoryAndRiskFactors
        self._familyHistoryAndRiskFactorsTier = PatientRecord.familyHistoryAndRiskFactorsTier
        self._familyHistoryOfPredispositionSyndrome = PatientRecord.familyHistoryOfPredispositionSyndrome
        self._familyHistoryOfPredispositionSyndromeTier = PatientRecord.familyHistoryOfPredispositionSyndromeTier
        self._detailsOfPredispositionSyndrome = PatientRecord.detailsOfPredispositionSyndrome
        self._detailsOfPredispositionSyndromeTier = PatientRecord.detailsOfPredispositionSyndromeTier
        self._geneticCancerSyndrome = PatientRecord.geneticCancerSyndrome
        self._geneticCancerSyndromeTier = PatientRecord.geneticCancerSyndromeTier
        self._otherGeneticConditionOrSignificantComorbidity = PatientRecord.otherGeneticConditionOrSignificantComorbidity
        self._otherGeneticConditionOrSignificantComorbidityTier = PatientRecord.otherGeneticConditionOrSignificantComorbidityTier
        self._occupationalOrEnvironmentalExposure = PatientRecord.occupationalOrEnvironmentalExposure
        self._occupationalOrEnvironmentalExposureTier = PatientRecord.occupationalOrEnvironmentalExposureTier

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
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._otherIds = parsed.otherIds
        self._otherIdsTier = parsed.otherIdsTier
        self._dateOfBirth = parsed.dateOfBirth
        self._dateOfBirthTier = parsed.dateOfBirthTier
        self._gender = parsed.gender
        self._genderTier = parsed.genderTier
        self._ethnicity = parsed.ethnicity
        self._ethnicityTier = parsed.ethnicityTier
        self._race = parsed.race
        self._raceTier = parsed.raceTier
        self._provinceOfResidence = parsed.provinceOfResidence
        self._provinceOfResidenceTier = parsed.provinceOfResidenceTier
        self._dateOfDeath = parsed.dateOfDeath
        self._dateOfDeathTier = parsed.dateOfDeathTier
        self._causeOfDeath = parsed.causeOfDeath
        self._causeOfDeathTier = parsed.causeOfDeathTier
        self._autopsyTissueForResearch = parsed.autopsyTissueForResearch
        self._autopsyTissueForResearchTier = parsed.autopsyTissueForResearchTier
        self._priorMalignancy = parsed.priorMalignancy
        self._priorMalignancyTier = parsed.priorMalignancyTier
        self._dateOfPriorMalignancy = parsed.dateOfPriorMalignancy
        self._dateOfPriorMalignancyTier = parsed.dateOfPriorMalignancyTier
        self._familyHistoryAndRiskFactors = parsed.familyHistoryAndRiskFactors
        self._familyHistoryAndRiskFactorsTier = parsed.familyHistoryAndRiskFactorsTier
        self._familyHistoryOfPredispositionSyndrome = parsed.familyHistoryOfPredispositionSyndrome
        self._familyHistoryOfPredispositionSyndromeTier = parsed.familyHistoryOfPredispositionSyndromeTier
        self._detailsOfPredispositionSyndrome = parsed.detailsOfPredispositionSyndrome
        self._detailsOfPredispositionSyndromeTier = parsed.detailsOfPredispositionSyndromeTier
        self._geneticCancerSyndrome = parsed.geneticCancerSyndrome
        self._geneticCancerSyndromeTier = parsed.geneticCancerSyndromeTier
        self._otherGeneticConditionOrSignificantComorbidity = parsed.otherGeneticConditionOrSignificantComorbidity
        self._otherGeneticConditionOrSignificantComorbidityTier = parsed.otherGeneticConditionOrSignificantComorbidityTier
        self._occupationalOrEnvironmentalExposure = parsed.occupationalOrEnvironmentalExposure
        self._occupationalOrEnvironmentalExposureTier = parsed.occupationalOrEnvironmentalExposureTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getOtherIds(self):
        return self._otherIds

    def getOtherIdsTier(self):
        return self._otherIdsTier

    def getDateOfBirth(self):
        return self._dateOfBirth

    def getDateOfBirthTier(self):
        return self._dateOfBirthTier

    def getGender(self):
        return self._gender

    def getGenderTier(self):
        return self._genderTier

    def getEthnicity(self):
        return self._ethnicity

    def getEthnicityTier(self):
        return self._ethnicityTier

    def getRace(self):
        return self._race

    def getRaceTier(self):
        return self._raceTier

    def getProvinceOfResidence(self):
        return self._provinceOfResidence

    def getProvinceOfResidenceTier(self):
        return self._provinceOfResidenceTier

    def getDateOfDeath(self):
        return self._dateOfDeath

    def getDateOfDeathTier(self):
        return self._dateOfDeathTier

    def getCauseOfDeath(self):
        return self._causeOfDeath

    def getCauseOfDeathTier(self):
        return self._causeOfDeathTier

    def getAutopsyTissueForResearch(self):
        return self._autopsyTissueForResearch

    def getAutopsyTissueForResearchTier(self):
        return self._autopsyTissueForResearchTier

    def getPriorMalignancy(self):
        return self._priorMalignancy

    def getPriorMalignancyTier(self):
        return self._priorMalignancyTier

    def getDateOfPriorMalignancy(self):
        return self._dateOfPriorMalignancy

    def getDateOfPriorMalignancyTier(self):
        return self._dateOfPriorMalignancyTier

    def getFamilyHistoryAndRiskFactors(self):
        return self._familyHistoryAndRiskFactors

    def getFamilyHistoryAndRiskFactorsTier(self):
        return self._familyHistoryAndRiskFactorsTier

    def getFamilyHistoryOfPredispositionSyndrome(self):
        return self._familyHistoryOfPredispositionSyndrome

    def getFamilyHistoryOfPredispositionSyndromeTier(self):
        return self._familyHistoryOfPredispositionSyndromeTier

    def getDetailsOfPredispositionSyndrome(self):
        return self._detailsOfPredispositionSyndrome

    def getDetailsOfPredispositionSyndromeTier(self):
        return self._detailsOfPredispositionSyndromeTier

    def getGeneticCancerSyndrome(self):
        return self._geneticCancerSyndrome

    def getGeneticCancerSyndromeTier(self):
        return self._geneticCancerSyndromeTier

    def getOtherGeneticConditionOrSignificantComorbidity(self):
        return self._otherGeneticConditionOrSignificantComorbidity

    def getOtherGeneticConditionOrSignificantComorbidityTier(self):
        return self._otherGeneticConditionOrSignificantComorbidityTier

    def getOccupationalOrEnvironmentalExposure(self):
        return self._occupationalOrEnvironmentalExposure

    def getOccupationalOrEnvironmentalExposureTier(self):
        return self._occupationalOrEnvironmentalExposureTier


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
        self._patientIdTier = None
        self._enrollmentInstitution = None
        self._enrollmentInstitutionTier = None
        self._enrollmentApprovalDate = None
        self._enrollmentApprovalDateTier = None
        self._crossEnrollment = None
        self._crossEnrollmentTier = None
        self._otherPersonalizedMedicineStudyName = None
        self._otherPersonalizedMedicineStudyNameTier = None
        self._otherPersonalizedMedicineStudyId = None
        self._otherPersonalizedMedicineStudyIdTier = None
        self._ageAtEnrollment = None
        self._ageAtEnrollmentTier = None
        self._eligibilityCategory = None
        self._eligibilityCategoryTier = None
        self._statusAtEnrollment = None
        self._statusAtEnrollmentTier = None
        self._primaryOncologistName = None
        self._primaryOncologistNameTier = None
        self._primaryOncologistContact = None
        self._primaryOncologistContactTier = None
        self._referringPhysicianName = None
        self._referringPhysicianNameTier = None
        self._referringPhysicianContact = None
        self._referringPhysicianContactTier = None
        self._summaryOfIdRequest = None
        self._summaryOfIdRequestTier = None
        self._treatingCentreName = None
        self._treatingCentreNameTier = None
        self._treatingCentreProvince = None
        self._treatingCentreProvinceTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "enrollmentInstitution": self.getEnrollmentInstitution,
            "enrollmentApprovalDate": self.getEnrollmentApprovalDate,
            "crossEnrollment": self.getCrossEnrollment,
            "otherPersonalizedMedicineStudyName": self.getOtherPersonalizedMedicineStudyName,
            "otherPersonalizedMedicineStudyId": self.getOtherPersonalizedMedicineStudyId,
            "ageAtEnrollment": self.getAgeAtEnrollment,
            "eligibilityCategory": self.getEligibilityCategory,
            "statusAtEnrollment": self.getStatusAtEnrollment,
            "primaryOncologistName": self.getPrimaryOncologistName,
            "primaryOncologistContact": self.getPrimaryOncologistContact,
            "referringPhysicianName": self.getReferringPhysicianName,
            "referringPhysicianContact": self.getReferringPhysicianContact,
            "summaryOfIdRequest": self.getSummaryOfIdRequest,
            "treatingCentreName": self.getTreatingCentreName,
            "treatingCentreProvince": self.getTreatingCentreProvince
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        try:
            # Unique fields
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getEnrollmentInstitutionTier():
                record['enrollmentInstitution'] = self.getEnrollmentInstitution()
            if tier >= self.getEnrollmentApprovalDateTier():
                record['enrollmentApprovalDate'] = self.getEnrollmentApprovalDate()
            if tier >= self.getCrossEnrollmentTier():
                record['crossEnrollment'] = self.getCrossEnrollment()
            if tier >= self.getOtherPersonalizedMedicineStudyNameTier():
                record['otherPersonalizedMedicineStudyName'] = self.getOtherPersonalizedMedicineStudyName()
            if tier >= self.getOtherPersonalizedMedicineStudyIdTier():
                record['otherPersonalizedMedicineStudyId'] = self.getOtherPersonalizedMedicineStudyId()
            if tier >= self.getAgeAtEnrollmentTier():
                record['ageAtEnrollment'] = self.getAgeAtEnrollment()
            if tier >= self.getEligibilityCategoryTier():
                record['eligibilityCategory'] = self.getEligibilityCategory()
            if tier >= self.getStatusAtEnrollmentTier():
                record['statusAtEnrollment'] = self.getStatusAtEnrollment()
            if tier >= self.getPrimaryOncologistNameTier():
                record['primaryOncologistName'] = self.getPrimaryOncologistName()
            if tier >= self.getPrimaryOncologistContactTier():
                record['primaryOncologistContact'] = self.getPrimaryOncologistContact()
            if tier >= self.getReferringPhysicianNameTier():
                record['referringPhysicianName'] = self.getReferringPhysicianName()
            if tier >= self.getReferringPhysicianContactTier():
                record['referringPhysicianContact'] = self.getReferringPhysicianContact()
            if tier >= self.getSummaryOfIdRequestTier():
                record['summaryOfIdRequest'] = self.getSummaryOfIdRequest()
            if tier >= self.getTreatingCentreNameTier():
                record['treatingCentreName'] = self.getTreatingCentreName()
            if tier >= self.getTreatingCentreProvinceTier():
                record['treatingCentreProvince'] = self.getTreatingCentreProvince()
        except TypeError:
            pass

        Enrollment = protocol.Enrollment(**record)
        self.serializeMetadataAttributes(Enrollment)

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
        self._patientIdTier = EnrollmentRecord.patientIdTier
        self._enrollmentInstitution = EnrollmentRecord.enrollmentInstitution
        self._enrollmentInstitutionTier = EnrollmentRecord.enrollmentInstitutionTier
        self._enrollmentApprovalDate = EnrollmentRecord.enrollmentApprovalDate
        self._enrollmentApprovalDateTier = EnrollmentRecord.enrollmentApprovalDateTier
        self._crossEnrollment = EnrollmentRecord.crossEnrollment
        self._crossEnrollmentTier = EnrollmentRecord.crossEnrollmentTier
        self._otherPersonalizedMedicineStudyName = EnrollmentRecord.otherPersonalizedMedicineStudyName
        self._otherPersonalizedMedicineStudyNameTier = EnrollmentRecord.otherPersonalizedMedicineStudyNameTier
        self._otherPersonalizedMedicineStudyId = EnrollmentRecord.otherPersonalizedMedicineStudyId
        self._otherPersonalizedMedicineStudyIdTier = EnrollmentRecord.otherPersonalizedMedicineStudyIdTier
        self._ageAtEnrollment = EnrollmentRecord.ageAtEnrollment
        self._ageAtEnrollmentTier = EnrollmentRecord.ageAtEnrollmentTier
        self._eligibilityCategory = EnrollmentRecord.eligibilityCategory
        self._eligibilityCategoryTier = EnrollmentRecord.eligibilityCategoryTier
        self._statusAtEnrollment = EnrollmentRecord.statusAtEnrollment
        self._statusAtEnrollmentTier = EnrollmentRecord.statusAtEnrollmentTier
        self._primaryOncologistName = EnrollmentRecord.primaryOncologistName
        self._primaryOncologistNameTier = EnrollmentRecord.primaryOncologistNameTier
        self._primaryOncologistContact = EnrollmentRecord.primaryOncologistContact
        self._primaryOncologistContactTier = EnrollmentRecord.primaryOncologistContactTier
        self._referringPhysicianName = EnrollmentRecord.referringPhysicianName
        self._referringPhysicianNameTier = EnrollmentRecord.referringPhysicianNameTier
        self._referringPhysicianContact = EnrollmentRecord.referringPhysicianContact
        self._referringPhysicianContactTier = EnrollmentRecord.referringPhysicianContactTier
        self._summaryOfIdRequest = EnrollmentRecord.summaryOfIdRequest
        self._summaryOfIdRequestTier = EnrollmentRecord.summaryOfIdRequestTier
        self._treatingCentreName = EnrollmentRecord.treatingCentreName
        self._treatingCentreNameTier = EnrollmentRecord.treatingCentreNameTier
        self._treatingCentreProvince = EnrollmentRecord.treatingCentreProvince
        self._treatingCentreProvinceTier = EnrollmentRecord.treatingCentreProvinceTier

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
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._enrollmentInstitution = parsed.enrollmentInstitution
        self._enrollmentInstitutionTier = parsed.enrollmentInstitutionTier
        self._enrollmentApprovalDate = parsed.enrollmentApprovalDate
        self._enrollmentApprovalDateTier = parsed.enrollmentApprovalDateTier
        self._crossEnrollment = parsed.crossEnrollment
        self._crossEnrollmentTier = parsed.crossEnrollmentTier
        self._otherPersonalizedMedicineStudyName = parsed.otherPersonalizedMedicineStudyName
        self._otherPersonalizedMedicineStudyNameTier = parsed.otherPersonalizedMedicineStudyNameTier
        self._otherPersonalizedMedicineStudyId = parsed.otherPersonalizedMedicineStudyId
        self._otherPersonalizedMedicineStudyIdTier = parsed.otherPersonalizedMedicineStudyIdTier
        self._ageAtEnrollment = parsed.ageAtEnrollment
        self._ageAtEnrollmentTier = parsed.ageAtEnrollmentTier
        self._eligibilityCategory = parsed.eligibilityCategory
        self._eligibilityCategoryTier = parsed.eligibilityCategoryTier
        self._statusAtEnrollment = parsed.statusAtEnrollment
        self._statusAtEnrollmentTier = parsed.statusAtEnrollmentTier
        self._primaryOncologistName = parsed.primaryOncologistName
        self._primaryOncologistNameTier = parsed.primaryOncologistNameTier
        self._primaryOncologistContact = parsed.primaryOncologistContact
        self._primaryOncologistContactTier = parsed.primaryOncologistContactTier
        self._referringPhysicianName = parsed.referringPhysicianName
        self._referringPhysicianNameTier = parsed.referringPhysicianNameTier
        self._referringPhysicianContact = parsed.referringPhysicianContact
        self._referringPhysicianContactTier = parsed.referringPhysicianContactTier
        self._summaryOfIdRequest = parsed.summaryOfIdRequest
        self._summaryOfIdRequestTier = parsed.summaryOfIdRequestTier
        self._treatingCentreName = parsed.treatingCentreName
        self._treatingCentreNameTier = parsed.treatingCentreNameTier
        self._treatingCentreProvince = parsed.treatingCentreProvince
        self._treatingCentreProvinceTier = parsed.treatingCentreProvinceTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getEnrollmentInstitution(self):
        return self._enrollmentInstitution

    def getEnrollmentInstitutionTier(self):
        return self._enrollmentInstitutionTier

    def getEnrollmentApprovalDate(self):
        return self._enrollmentApprovalDate

    def getEnrollmentApprovalDateTier(self):
        return self._enrollmentApprovalDateTier

    def getCrossEnrollment(self):
        return self._crossEnrollment

    def getCrossEnrollmentTier(self):
        return self._crossEnrollmentTier

    def getOtherPersonalizedMedicineStudyName(self):
        return self._otherPersonalizedMedicineStudyName

    def getOtherPersonalizedMedicineStudyNameTier(self):
        return self._otherPersonalizedMedicineStudyNameTier

    def getOtherPersonalizedMedicineStudyId(self):
        return self._otherPersonalizedMedicineStudyId

    def getOtherPersonalizedMedicineStudyIdTier(self):
        return self._otherPersonalizedMedicineStudyIdTier

    def getAgeAtEnrollment(self):
        return self._ageAtEnrollment

    def getAgeAtEnrollmentTier(self):
        return self._ageAtEnrollmentTier

    def getEligibilityCategory(self):
        return self._eligibilityCategory

    def getEligibilityCategoryTier(self):
        return self._eligibilityCategoryTier

    def getStatusAtEnrollment(self):
        return self._statusAtEnrollment

    def getStatusAtEnrollmentTier(self):
        return self._statusAtEnrollmentTier

    def getPrimaryOncologistName(self):
        return self._primaryOncologistName

    def getPrimaryOncologistNameTier(self):
        return self._primaryOncologistNameTier

    def getPrimaryOncologistContact(self):
        return self._primaryOncologistContact

    def getPrimaryOncologistContactTier(self):
        return self._primaryOncologistContactTier

    def getReferringPhysicianName(self):
        return self._referringPhysicianName

    def getReferringPhysicianNameTier(self):
        return self._referringPhysicianNameTier

    def getReferringPhysicianContact(self):
        return self._referringPhysicianContact

    def getReferringPhysicianContactTier(self):
        return self._referringPhysicianContactTier

    def getSummaryOfIdRequest(self):
        return self._summaryOfIdRequest

    def getSummaryOfIdRequestTier(self):
        return self._summaryOfIdRequestTier

    def getTreatingCentreName(self):
        return self._treatingCentreName

    def getTreatingCentreNameTier(self):
        return self._treatingCentreNameTier

    def getTreatingCentreProvince(self):
        return self._treatingCentreProvince

    def getTreatingCentreProvinceTier(self):
        return self._treatingCentreProvinceTier


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
        self._patientIdTier = None
        self._consentId = None
        self._consentIdTier = None
        self._consentDate = None
        self._consentDateTier = None
        self._consentVersion = None
        self._consentVersionTier = None
        self._patientConsentedTo = None
        self._patientConsentedToTier = None
        self._reasonForRejection = None
        self._reasonForRejectionTier = None
        self._wasAssentObtained = None
        self._wasAssentObtainedTier = None
        self._dateOfAssent = None
        self._dateOfAssentTier = None
        self._assentFormVersion = None
        self._assentFormVersionTier = None
        self._ifAssentNotObtainedWhyNot = None
        self._ifAssentNotObtainedWhyNotTier = None
        self._reconsentDate = None
        self._reconsentDateTier = None
        self._reconsentVersion = None
        self._reconsentVersionTier = None
        self._consentingCoordinatorName = None
        self._consentingCoordinatorNameTier = None
        self._previouslyConsented = None
        self._previouslyConsentedTier = None
        self._nameOfOtherBiobank = None
        self._nameOfOtherBiobankTier = None
        self._hasConsentBeenWithdrawn = None
        self._hasConsentBeenWithdrawnTier = None
        self._dateOfConsentWithdrawal = None
        self._dateOfConsentWithdrawalTier = None
        self._typeOfConsentWithdrawal = None
        self._typeOfConsentWithdrawalTier = None
        self._reasonForConsentWithdrawal = None
        self._reasonForConsentWithdrawalTier = None
        self._consentFormComplete = None
        self._consentFormCompleteTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "consentId": self.getConsentId,
            "consentDate": self.getConsentDate,
            "consentVersion": self.getConsentVersion,
            "patientConsentedTo": self.getPatientConsentedTo,
            "reasonForRejection": self.getReasonForRejection,
            "wasAssentObtained": self.getWasAssentObtained,
            "dateOfAssent": self.getDateOfAssent,
            "assentFormVersion": self.getAssentFormVersion,
            "ifAssentNotObtainedWhyNot": self.getIfAssentNotObtainedWhyNot,
            "reconsentDate": self.getReconsentDate,
            "reconsentVersion": self.getReconsentVersion,
            "consentingCoordinatorName": self.getConsentingCoordinatorName,
            "previouslyConsented": self.getPreviouslyConsented,
            "nameOfOtherBiobank": self.getNameOfOtherBiobank,
            "hasConsentBeenWithdrawn": self.getHasConsentBeenWithdrawn,
            "dateOfConsentWithdrawal": self.getDateOfConsentWithdrawal,
            "typeOfConsentWithdrawal": self.getTypeOfConsentWithdrawal,
            "reasonForConsentWithdrawal": self.getReasonForConsentWithdrawal,
            "consentFormComplete": self.getConsentFormComplete
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        try:
            # Unique fields
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getConsentIdTier():
                record['consentId'] = self.getConsentId()
            if tier >= self.getConsentDateTier():
                record['consentDate'] = self.getConsentDate()
            if tier >= self.getConsentVersionTier():
                record['consentVersion'] = self.getConsentVersion()
            if tier >= self.getPatientConsentedToTier():
                record['patientConsentedTo'] = self.getPatientConsentedTo()
            if tier >= self.getReasonForRejectionTier():
                record['reasonForRejection'] = self.getReasonForRejection()
            if tier >= self.getWasAssentObtainedTier():
                record['wasAssentObtained'] = self.getWasAssentObtained()
            if tier >= self.getDateOfAssentTier():
                record['dateOfAssent'] = self.getDateOfAssent()
            if tier >= self.getAssentFormVersionTier():
                record['assentFormVersion'] = self.getAssentFormVersion()
            if tier >= self.getIfAssentNotObtainedWhyNotTier():
                record['ifAssentNotObtainedWhyNot'] = self.getIfAssentNotObtainedWhyNot()
            if tier >= self.getReconsentDateTier():
                record['reconsentDate'] = self.getReconsentDate()
            if tier >= self.getReconsentVersionTier():
                record['reconsentVersion'] = self.getReconsentVersion()
            if tier >= self.getConsentingCoordinatorNameTier():
                record['consentingCoordinatorName'] = self.getConsentingCoordinatorName()
            if tier >= self.getPreviouslyConsentedTier():
                record['previouslyConsented'] = self.getPreviouslyConsented()
            if tier >= self.getNameOfOtherBiobankTier():
                record['nameOfOtherBiobank'] = self.getNameOfOtherBiobank()
            if tier >= self.getHasConsentBeenWithdrawnTier():
                record['hasConsentBeenWithdrawn'] = self.getHasConsentBeenWithdrawn()
            if tier >= self.getDateOfConsentWithdrawalTier():
                record['dateOfConsentWithdrawal'] = self.getDateOfConsentWithdrawal()
            if tier >= self.getTypeOfConsentWithdrawalTier():
                record['typeOfConsentWithdrawal'] = self.getTypeOfConsentWithdrawal()
            if tier >= self.getReasonForConsentWithdrawalTier():
                record['reasonForConsentWithdrawal'] = self.getReasonForConsentWithdrawal()
            if tier >= self.getConsentFormCompleteTier():
                record['consentFormComplete'] = self.getConsentFormComplete()
        except TypeError:
            pass

        Consent = protocol.Consent(**record)
        self.serializeMetadataAttributes(Consent)

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
        self._patientIdTier = ConsentRecord.patientIdTier
        self._consentId = ConsentRecord.consentId
        self._consentIdTier = ConsentRecord.consentIdTier
        self._consentDate = ConsentRecord.consentDate
        self._consentDateTier = ConsentRecord.consentDateTier
        self._consentVersion = ConsentRecord.consentVersion
        self._consentVersionTier = ConsentRecord.consentVersionTier
        self._patientConsentedTo = ConsentRecord.patientConsentedTo
        self._patientConsentedToTier = ConsentRecord.patientConsentedToTier
        self._reasonForRejection = ConsentRecord.reasonForRejection
        self._reasonForRejectionTier = ConsentRecord.reasonForRejectionTier
        self._wasAssentObtained = ConsentRecord.wasAssentObtained
        self._wasAssentObtainedTier = ConsentRecord.wasAssentObtainedTier
        self._dateOfAssent = ConsentRecord.dateOfAssent
        self._dateOfAssentTier = ConsentRecord.dateOfAssentTier
        self._assentFormVersion = ConsentRecord.assentFormVersion
        self._assentFormVersionTier = ConsentRecord.assentFormVersionTier
        self._ifAssentNotObtainedWhyNot = ConsentRecord.ifAssentNotObtainedWhyNot
        self._ifAssentNotObtainedWhyNotTier = ConsentRecord.ifAssentNotObtainedWhyNotTier
        self._reconsentDate = ConsentRecord.reconsentDate
        self._reconsentDateTier = ConsentRecord.reconsentDateTier
        self._reconsentVersion = ConsentRecord.reconsentVersion
        self._reconsentVersionTier = ConsentRecord.reconsentVersionTier
        self._consentingCoordinatorName = ConsentRecord.consentingCoordinatorName
        self._consentingCoordinatorNameTier = ConsentRecord.consentingCoordinatorNameTier
        self._previouslyConsented = ConsentRecord.previouslyConsented
        self._previouslyConsentedTier = ConsentRecord.previouslyConsentedTier
        self._nameOfOtherBiobank = ConsentRecord.nameOfOtherBiobank
        self._nameOfOtherBiobankTier = ConsentRecord.nameOfOtherBiobankTier
        self._hasConsentBeenWithdrawn = ConsentRecord.hasConsentBeenWithdrawn
        self._hasConsentBeenWithdrawnTier = ConsentRecord.hasConsentBeenWithdrawnTier
        self._dateOfConsentWithdrawal = ConsentRecord.dateOfConsentWithdrawal
        self._dateOfConsentWithdrawalTier = ConsentRecord.dateOfConsentWithdrawalTier
        self._typeOfConsentWithdrawal = ConsentRecord.typeOfConsentWithdrawal
        self._typeOfConsentWithdrawalTier = ConsentRecord.typeOfConsentWithdrawalTier
        self._reasonForConsentWithdrawal = ConsentRecord.reasonForConsentWithdrawal
        self._reasonForConsentWithdrawalTier = ConsentRecord.reasonForConsentWithdrawalTier
        self._consentFormComplete = ConsentRecord.consentFormComplete
        self._consentFormCompleteTier = ConsentRecord.consentFormCompleteTier

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
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._consentId = parsed.consentId
        self._consentIdTier = parsed.consentIdTier
        self._consentDate = parsed.consentDate
        self._consentDateTier = parsed.consentDateTier
        self._consentVersion = parsed.consentVersion
        self._consentVersionTier = parsed.consentVersionTier
        self._patientConsentedTo = parsed.patientConsentedTo
        self._patientConsentedToTier = parsed.patientConsentedToTier
        self._reasonForRejection = parsed.reasonForRejection
        self._reasonForRejectionTier = parsed.reasonForRejectionTier
        self._wasAssentObtained = parsed.wasAssentObtained
        self._wasAssentObtainedTier = parsed.wasAssentObtainedTier
        self._dateOfAssent = parsed.dateOfAssent
        self._dateOfAssentTier = parsed.dateOfAssentTier
        self._assentFormVersion = parsed.assentFormVersion
        self._assentFormVersionTier = parsed.assentFormVersionTier
        self._ifAssentNotObtainedWhyNot = parsed.ifAssentNotObtainedWhyNot
        self._ifAssentNotObtainedWhyNotTier = parsed.ifAssentNotObtainedWhyNotTier
        self._reconsentDate = parsed.reconsentDate
        self._reconsentDateTier = parsed.reconsentDateTier
        self._reconsentVersion = parsed.reconsentVersion
        self._reconsentVersionTier = parsed.reconsentVersionTier
        self._consentingCoordinatorName = parsed.consentingCoordinatorName
        self._consentingCoordinatorNameTier = parsed.consentingCoordinatorNameTier
        self._previouslyConsented = parsed.previouslyConsented
        self._previouslyConsentedTier = parsed.previouslyConsentedTier
        self._nameOfOtherBiobank = parsed.nameOfOtherBiobank
        self._nameOfOtherBiobankTier = parsed.nameOfOtherBiobankTier
        self._hasConsentBeenWithdrawn = parsed.hasConsentBeenWithdrawn
        self._hasConsentBeenWithdrawnTier = parsed.hasConsentBeenWithdrawnTier
        self._dateOfConsentWithdrawal = parsed.dateOfConsentWithdrawal
        self._dateOfConsentWithdrawalTier = parsed.dateOfConsentWithdrawalTier
        self._typeOfConsentWithdrawal = parsed.typeOfConsentWithdrawal
        self._typeOfConsentWithdrawalTier = parsed.typeOfConsentWithdrawalTier
        self._reasonForConsentWithdrawal = parsed.reasonForConsentWithdrawal
        self._reasonForConsentWithdrawalTier = parsed.reasonForConsentWithdrawalTier
        self._consentFormComplete = parsed.consentFormComplete
        self._consentFormCompleteTier = parsed.consentFormCompleteTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getConsentId(self):
        return self._consentId

    def getConsentIdTier(self):
        return self._consentIdTier

    def getConsentDate(self):
        return self._consentDate

    def getConsentDateTier(self):
        return self._consentDateTier

    def getConsentVersion(self):
        return self._consentVersion

    def getConsentVersionTier(self):
        return self._consentVersionTier

    def getPatientConsentedTo(self):
        return self._patientConsentedTo

    def getPatientConsentedToTier(self):
        return self._patientConsentedToTier

    def getReasonForRejection(self):
        return self._reasonForRejection

    def getReasonForRejectionTier(self):
        return self._reasonForRejectionTier

    def getWasAssentObtained(self):
        return self._wasAssentObtained

    def getWasAssentObtainedTier(self):
        return self._wasAssentObtainedTier

    def getDateOfAssent(self):
        return self._dateOfAssent

    def getDateOfAssentTier(self):
        return self._dateOfAssentTier

    def getAssentFormVersion(self):
        return self._assentFormVersion

    def getAssentFormVersionTier(self):
        return self._assentFormVersionTier

    def getIfAssentNotObtainedWhyNot(self):
        return self._ifAssentNotObtainedWhyNot

    def getIfAssentNotObtainedWhyNotTier(self):
        return self._ifAssentNotObtainedWhyNotTier

    def getReconsentDate(self):
        return self._reconsentDate

    def getReconsentDateTier(self):
        return self._reconsentDateTier

    def getReconsentVersion(self):
        return self._reconsentVersion

    def getReconsentVersionTier(self):
        return self._reconsentVersionTier

    def getConsentingCoordinatorName(self):
        return self._consentingCoordinatorName

    def getConsentingCoordinatorNameTier(self):
        return self._consentingCoordinatorNameTier

    def getPreviouslyConsented(self):
        return self._previouslyConsented

    def getPreviouslyConsentedTier(self):
        return self._previouslyConsentedTier

    def getNameOfOtherBiobank(self):
        return self._nameOfOtherBiobank

    def getNameOfOtherBiobankTier(self):
        return self._nameOfOtherBiobankTier

    def getHasConsentBeenWithdrawn(self):
        return self._hasConsentBeenWithdrawn

    def getHasConsentBeenWithdrawnTier(self):
        return self._hasConsentBeenWithdrawnTier

    def getDateOfConsentWithdrawal(self):
        return self._dateOfConsentWithdrawal

    def getDateOfConsentWithdrawalTier(self):
        return self._dateOfConsentWithdrawalTier

    def getTypeOfConsentWithdrawal(self):
        return self._typeOfConsentWithdrawal

    def getTypeOfConsentWithdrawalTier(self):
        return self._typeOfConsentWithdrawalTier

    def getReasonForConsentWithdrawal(self):
        return self._reasonForConsentWithdrawal

    def getReasonForConsentWithdrawalTier(self):
        return self._reasonForConsentWithdrawalTier

    def getConsentFormComplete(self):
        return self._consentFormComplete

    def getConsentFormCompleteTier(self):
        return self._consentFormCompleteTier


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
        self._patientIdTier = None
        self._diagnosisId = None
        self._diagnosisIdTier = None
        self._diagnosisDate = None
        self._diagnosisDateTier = None
        self._ageAtDiagnosis = None
        self._ageAtDiagnosisTier = None
        self._cancerType = None
        self._cancerTypeTier = None
        self._classification = None
        self._classificationTier = None
        self._cancerSite = None
        self._cancerSiteTier = None
        self._histology = None
        self._histologyTier = None
        self._methodOfDefinitiveDiagnosis = None
        self._methodOfDefinitiveDiagnosisTier = None
        self._sampleType = None
        self._sampleTypeTier = None
        self._sampleSite = None
        self._sampleSiteTier = None
        self._tumorGrade = None
        self._tumorGradeTier = None
        self._gradingSystemUsed = None
        self._gradingSystemUsedTier = None
        self._sitesOfMetastases = None
        self._sitesOfMetastasesTier = None
        self._stagingSystem = None
        self._stagingSystemTier = None
        self._versionOrEditionOfTheStagingSystem = None
        self._versionOrEditionOfTheStagingSystemTier = None
        self._specificTumorStageAtDiagnosis = None
        self._specificTumorStageAtDiagnosisTier = None
        self._prognosticBiomarkers = None
        self._prognosticBiomarkersTier = None
        self._biomarkerQuantification = None
        self._biomarkerQuantificationTier = None
        self._additionalMolecularTesting = None
        self._additionalMolecularTestingTier = None
        self._additionalTestType = None
        self._additionalTestTypeTier = None
        self._laboratoryName = None
        self._laboratoryNameTier = None
        self._laboratoryAddress = None
        self._laboratoryAddressTier = None
        self._siteOfMetastases = None
        self._siteOfMetastasesTier = None
        self._stagingSystemVersion = None
        self._stagingSystemVersionTier = None
        self._specificStage = None
        self._specificStageTier = None
        self._cancerSpecificBiomarkers = None
        self._cancerSpecificBiomarkersTier = None
        self._additionalMolecularDiagnosticTestingPerformed = None
        self._additionalMolecularDiagnosticTestingPerformedTier = None
        self._additionalTest = None
        self._additionalTestTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "diagnosisId": self.getDiagnosisId,
            "diagnosisDate": self.getDiagnosisDate,
            "ageAtDiagnosis": self.getAgeAtDiagnosis,
            "cancerType": self.getCancerType,
            "classification": self.getClassification,
            "cancerSite": self.getCancerSite,
            "histology": self.getHistology,
            "methodOfDefinitiveDiagnosis": self.getMethodOfDefinitiveDiagnosis,
            "sampleType": self.getSampleType,
            "sampleSite": self.getSampleSite,
            "tumorGrade": self.getTumorGrade,
            "gradingSystemUsed": self.getGradingSystemUsed,
            "sitesOfMetastases": self.getSitesOfMetastases,
            "stagingSystem": self.getStagingSystem,
            "versionOrEditionOfTheStagingSystem": self.getVersionOrEditionOfTheStagingSystem,
            "specificTumorStageAtDiagnosis": self.getSpecificTumorStageAtDiagnosis,
            "prognosticBiomarkers": self.getPrognosticBiomarkers,
            "biomarkerQuantification": self.getBiomarkerQuantification,
            "additionalMolecularTesting": self.getAdditionalMolecularTesting,
            "additionalTestType": self.getAdditionalTestType,
            "laboratoryName": self.getLaboratoryName,
            "laboratoryAddress": self.getLaboratoryAddress,
            "siteOfMetastases": self.getSiteOfMetastases,
            "stagingSystemVersion": self.getStagingSystemVersion,
            "specificStage": self.getSpecificStage,
            "cancerSpecificBiomarkers": self.getCancerSpecificBiomarkers,
            "additionalMolecularDiagnosticTestingPerformed": self.getAdditionalMolecularDiagnosticTestingPerformed,
            "additionalTest": self.getAdditionalTest
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        try:
            # Unique fields
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getDiagnosisIdTier():
                record['diagnosisId'] = self.getDiagnosisId()
            if tier >= self.getDiagnosisDateTier():
                record['diagnosisDate'] = self.getDiagnosisDate()
            if tier >= self.getAgeAtDiagnosisTier():
                record['ageAtDiagnosis'] = self.getAgeAtDiagnosis()
            if tier >= self.getCancerTypeTier():
                record['cancerType'] = self.getCancerType()
            if tier >= self.getClassificationTier():
                record['classification'] = self.getClassification()
            if tier >= self.getCancerSiteTier():
                record['cancerSite'] = self.getCancerSite()
            if tier >= self.getHistologyTier():
                record['histology'] = self.getHistology()
            if tier >= self.getMethodOfDefinitiveDiagnosisTier():
                record['methodOfDefinitiveDiagnosis'] = self.getMethodOfDefinitiveDiagnosis()
            if tier >= self.getSampleTypeTier():
                record['sampleType'] = self.getSampleType()
            if tier >= self.getSampleSiteTier():
                record['sampleSite'] = self.getSampleSite()
            if tier >= self.getTumorGradeTier():
                record['tumorGrade'] = self.getTumorGrade()
            if tier >= self.getGradingSystemUsedTier():
                record['gradingSystemUsed'] = self.getGradingSystemUsed()
            if tier >= self.getSitesOfMetastasesTier():
                record['sitesOfMetastases'] = self.getSitesOfMetastases()
            if tier >= self.getStagingSystemTier():
                record['stagingSystem'] = self.getStagingSystem()
            if tier >= self.getVersionOrEditionOfTheStagingSystemTier():
                record['versionOrEditionOfTheStagingSystem'] = self.getVersionOrEditionOfTheStagingSystem()
            if tier >= self.getSpecificTumorStageAtDiagnosisTier():
                record['specificTumorStageAtDiagnosis'] = self.getSpecificTumorStageAtDiagnosis()
            if tier >= self.getPrognosticBiomarkersTier():
                record['prognosticBiomarkers'] = self.getPrognosticBiomarkers()
            if tier >= self.getBiomarkerQuantificationTier():
                record['biomarkerQuantification'] = self.getBiomarkerQuantification()
            if tier >= self.getAdditionalMolecularTestingTier():
                record['additionalMolecularTesting'] = self.getAdditionalMolecularTesting()
            if tier >= self.getAdditionalTestTypeTier():
                record['additionalTestType'] = self.getAdditionalTestType()
            if tier >= self.getLaboratoryNameTier():
                record['laboratoryName'] = self.getLaboratoryName()
            if tier >= self.getLaboratoryAddressTier():
                record['laboratoryAddress'] = self.getLaboratoryAddress()
            if tier >= self.getSiteOfMetastasesTier():
                record['siteOfMetastases'] = self.getSiteOfMetastases()
            if tier >= self.getStagingSystemVersionTier():
                record['stagingSystemVersion'] = self.getStagingSystemVersion()
            if tier >= self.getSpecificStageTier():
                record['specificStage'] = self.getSpecificStage()
            if tier >= self.getCancerSpecificBiomarkersTier():
                record['cancerSpecificBiomarkers'] = self.getCancerSpecificBiomarkers()
            if tier >= self.getAdditionalMolecularDiagnosticTestingPerformedTier():
                record['additionalMolecularDiagnosticTestingPerformed'] = self.getAdditionalMolecularDiagnosticTestingPerformed()
            if tier >= self.getAdditionalTestTier():
                record['additionalTest'] = self.getAdditionalTest()
        except TypeError:
            pass

        Diagnosis = protocol.Diagnosis(**record)
        self.serializeMetadataAttributes(Diagnosis)

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
        self._patientIdTier = DiagnosisRecord.patientIdTier
        self._diagnosisId = DiagnosisRecord.diagnosisId
        self._diagnosisIdTier = DiagnosisRecord.diagnosisIdTier
        self._diagnosisDate = DiagnosisRecord.diagnosisDate
        self._diagnosisDateTier = DiagnosisRecord.diagnosisDateTier
        self._ageAtDiagnosis = DiagnosisRecord.ageAtDiagnosis
        self._ageAtDiagnosisTier = DiagnosisRecord.ageAtDiagnosisTier
        self._cancerType = DiagnosisRecord.cancerType
        self._cancerTypeTier = DiagnosisRecord.cancerTypeTier
        self._classification = DiagnosisRecord.classification
        self._classificationTier = DiagnosisRecord.classificationTier
        self._cancerSite = DiagnosisRecord.cancerSite
        self._cancerSiteTier = DiagnosisRecord.cancerSiteTier
        self._histology = DiagnosisRecord.histology
        self._histologyTier = DiagnosisRecord.histologyTier
        self._methodOfDefinitiveDiagnosis = DiagnosisRecord.methodOfDefinitiveDiagnosis
        self._methodOfDefinitiveDiagnosisTier = DiagnosisRecord.methodOfDefinitiveDiagnosisTier
        self._sampleType = DiagnosisRecord.sampleType
        self._sampleTypeTier = DiagnosisRecord.sampleTypeTier
        self._sampleSite = DiagnosisRecord.sampleSite
        self._sampleSiteTier = DiagnosisRecord.sampleSiteTier
        self._tumorGrade = DiagnosisRecord.tumorGrade
        self._tumorGradeTier = DiagnosisRecord.tumorGradeTier
        self._gradingSystemUsed = DiagnosisRecord.gradingSystemUsed
        self._gradingSystemUsedTier = DiagnosisRecord.gradingSystemUsedTier
        self._sitesOfMetastases = DiagnosisRecord.sitesOfMetastases
        self._sitesOfMetastasesTier = DiagnosisRecord.sitesOfMetastasesTier
        self._stagingSystem = DiagnosisRecord.stagingSystem
        self._stagingSystemTier = DiagnosisRecord.stagingSystemTier
        self._versionOrEditionOfTheStagingSystem = DiagnosisRecord.versionOrEditionOfTheStagingSystem
        self._versionOrEditionOfTheStagingSystemTier = DiagnosisRecord.versionOrEditionOfTheStagingSystemTier
        self._specificTumorStageAtDiagnosis = DiagnosisRecord.specificTumorStageAtDiagnosis
        self._specificTumorStageAtDiagnosisTier = DiagnosisRecord.specificTumorStageAtDiagnosisTier
        self._prognosticBiomarkers = DiagnosisRecord.prognosticBiomarkers
        self._prognosticBiomarkersTier = DiagnosisRecord.prognosticBiomarkersTier
        self._biomarkerQuantification = DiagnosisRecord.biomarkerQuantification
        self._biomarkerQuantificationTier = DiagnosisRecord.biomarkerQuantificationTier
        self._additionalMolecularTesting = DiagnosisRecord.additionalMolecularTesting
        self._additionalMolecularTestingTier = DiagnosisRecord.additionalMolecularTestingTier
        self._additionalTestType = DiagnosisRecord.additionalTestType
        self._additionalTestTypeTier = DiagnosisRecord.additionalTestTypeTier
        self._laboratoryName = DiagnosisRecord.laboratoryName
        self._laboratoryNameTier = DiagnosisRecord.laboratoryNameTier
        self._laboratoryAddress = DiagnosisRecord.laboratoryAddress
        self._laboratoryAddressTier = DiagnosisRecord.laboratoryAddressTier
        self._siteOfMetastases = DiagnosisRecord.siteOfMetastases
        self._siteOfMetastasesTier = DiagnosisRecord.siteOfMetastasesTier
        self._stagingSystemVersion = DiagnosisRecord.stagingSystemVersion
        self._stagingSystemVersionTier = DiagnosisRecord.stagingSystemVersionTier
        self._specificStage = DiagnosisRecord.specificStage
        self._specificStageTier = DiagnosisRecord.specificStageTier
        self._cancerSpecificBiomarkers = DiagnosisRecord.cancerSpecificBiomarkers
        self._cancerSpecificBiomarkersTier = DiagnosisRecord.cancerSpecificBiomarkersTier
        self._additionalMolecularDiagnosticTestingPerformed = DiagnosisRecord.additionalMolecularDiagnosticTestingPerformed
        self._additionalMolecularDiagnosticTestingPerformedTier = DiagnosisRecord.additionalMolecularDiagnosticTestingPerformedTier
        self._additionalTest = DiagnosisRecord.additionalTest
        self._additionalTestTier = DiagnosisRecord.additionalTestTier

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
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._diagnosisId = parsed.diagnosisId
        self._diagnosisIdTier = parsed.diagnosisIdTier
        self._diagnosisDate = parsed.diagnosisDate
        self._diagnosisDateTier = parsed.diagnosisDateTier
        self._ageAtDiagnosis = parsed.ageAtDiagnosis
        self._ageAtDiagnosisTier = parsed.ageAtDiagnosisTier
        self._cancerType = parsed.cancerType
        self._cancerTypeTier = parsed.cancerTypeTier
        self._classification = parsed.classification
        self._classificationTier = parsed.classificationTier
        self._cancerSite = parsed.cancerSite
        self._cancerSiteTier = parsed.cancerSiteTier
        self._histology = parsed.histology
        self._histologyTier = parsed.histologyTier
        self._methodOfDefinitiveDiagnosis = parsed.methodOfDefinitiveDiagnosis
        self._methodOfDefinitiveDiagnosisTier = parsed.methodOfDefinitiveDiagnosisTier
        self._sampleType = parsed.sampleType
        self._sampleTypeTier = parsed.sampleTypeTier
        self._sampleSite = parsed.sampleSite
        self._sampleSiteTier = parsed.sampleSiteTier
        self._tumorGrade = parsed.tumorGrade
        self._tumorGradeTier = parsed.tumorGradeTier
        self._gradingSystemUsed = parsed.gradingSystemUsed
        self._gradingSystemUsedTier = parsed.gradingSystemUsedTier
        self._sitesOfMetastases = parsed.sitesOfMetastases
        self._sitesOfMetastasesTier = parsed.sitesOfMetastasesTier
        self._stagingSystem = parsed.stagingSystem
        self._stagingSystemTier = parsed.stagingSystemTier
        self._versionOrEditionOfTheStagingSystem = parsed.versionOrEditionOfTheStagingSystem
        self._versionOrEditionOfTheStagingSystemTier = parsed.versionOrEditionOfTheStagingSystemTier
        self._specificTumorStageAtDiagnosis = parsed.specificTumorStageAtDiagnosis
        self._specificTumorStageAtDiagnosisTier = parsed.specificTumorStageAtDiagnosisTier
        self._prognosticBiomarkers = parsed.prognosticBiomarkers
        self._prognosticBiomarkersTier = parsed.prognosticBiomarkersTier
        self._biomarkerQuantification = parsed.biomarkerQuantification
        self._biomarkerQuantificationTier = parsed.biomarkerQuantificationTier
        self._additionalMolecularTesting = parsed.additionalMolecularTesting
        self._additionalMolecularTestingTier = parsed.additionalMolecularTestingTier
        self._additionalTestType = parsed.additionalTestType
        self._additionalTestTypeTier = parsed.additionalTestTypeTier
        self._laboratoryName = parsed.laboratoryName
        self._laboratoryNameTier = parsed.laboratoryNameTier
        self._laboratoryAddress = parsed.laboratoryAddress
        self._laboratoryAddressTier = parsed.laboratoryAddressTier
        self._siteOfMetastases = parsed.siteOfMetastases
        self._siteOfMetastasesTier = parsed.siteOfMetastasesTier
        self._stagingSystemVersion = parsed.stagingSystemVersion
        self._stagingSystemVersionTier = parsed.stagingSystemVersionTier
        self._specificStage = parsed.specificStage
        self._specificStageTier = parsed.specificStageTier
        self._cancerSpecificBiomarkers = parsed.cancerSpecificBiomarkers
        self._cancerSpecificBiomarkersTier = parsed.cancerSpecificBiomarkersTier
        self._additionalMolecularDiagnosticTestingPerformed = parsed.additionalMolecularDiagnosticTestingPerformed
        self._additionalMolecularDiagnosticTestingPerformedTier = parsed.additionalMolecularDiagnosticTestingPerformedTier
        self._additionalTest = parsed.additionalTest
        self._additionalTestTier = parsed.additionalTestTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getDiagnosisId(self):
        return self._diagnosisId

    def getDiagnosisIdTier(self):
        return self._diagnosisIdTier

    def getDiagnosisDate(self):
        return self._diagnosisDate

    def getDiagnosisDateTier(self):
        return self._diagnosisDateTier

    def getAgeAtDiagnosis(self):
        return self._ageAtDiagnosis

    def getAgeAtDiagnosisTier(self):
        return self._ageAtDiagnosisTier

    def getCancerType(self):
        return self._cancerType

    def getCancerTypeTier(self):
        return self._cancerTypeTier

    def getClassification(self):
        return self._classification

    def getClassificationTier(self):
        return self._classificationTier

    def getCancerSite(self):
        return self._cancerSite

    def getCancerSiteTier(self):
        return self._cancerSiteTier

    def getHistology(self):
        return self._histology

    def getHistologyTier(self):
        return self._histologyTier

    def getMethodOfDefinitiveDiagnosis(self):
        return self._methodOfDefinitiveDiagnosis

    def getMethodOfDefinitiveDiagnosisTier(self):
        return self._methodOfDefinitiveDiagnosisTier

    def getSampleType(self):
        return self._sampleType

    def getSampleTypeTier(self):
        return self._sampleTypeTier

    def getSampleSite(self):
        return self._sampleSite

    def getSampleSiteTier(self):
        return self._sampleSiteTier

    def getTumorGrade(self):
        return self._tumorGrade

    def getTumorGradeTier(self):
        return self._tumorGradeTier

    def getGradingSystemUsed(self):
        return self._gradingSystemUsed

    def getGradingSystemUsedTier(self):
        return self._gradingSystemUsedTier

    def getSitesOfMetastases(self):
        return self._sitesOfMetastases

    def getSitesOfMetastasesTier(self):
        return self._sitesOfMetastasesTier

    def getStagingSystem(self):
        return self._stagingSystem

    def getStagingSystemTier(self):
        return self._stagingSystemTier

    def getVersionOrEditionOfTheStagingSystem(self):
        return self._versionOrEditionOfTheStagingSystem

    def getVersionOrEditionOfTheStagingSystemTier(self):
        return self._versionOrEditionOfTheStagingSystemTier

    def getSpecificTumorStageAtDiagnosis(self):
        return self._specificTumorStageAtDiagnosis

    def getSpecificTumorStageAtDiagnosisTier(self):
        return self._specificTumorStageAtDiagnosisTier

    def getPrognosticBiomarkers(self):
        return self._prognosticBiomarkers

    def getPrognosticBiomarkersTier(self):
        return self._prognosticBiomarkersTier

    def getBiomarkerQuantification(self):
        return self._biomarkerQuantification

    def getBiomarkerQuantificationTier(self):
        return self._biomarkerQuantificationTier

    def getAdditionalMolecularTesting(self):
        return self._additionalMolecularTesting

    def getAdditionalMolecularTestingTier(self):
        return self._additionalMolecularTestingTier

    def getAdditionalTestType(self):
        return self._additionalTestType

    def getAdditionalTestTypeTier(self):
        return self._additionalTestTypeTier

    def getLaboratoryName(self):
        return self._laboratoryName

    def getLaboratoryNameTier(self):
        return self._laboratoryNameTier

    def getLaboratoryAddress(self):
        return self._laboratoryAddress

    def getLaboratoryAddressTier(self):
        return self._laboratoryAddressTier

    def getSiteOfMetastases(self):
        return self._siteOfMetastases

    def getSiteOfMetastasesTier(self):
        return self._siteOfMetastasesTier

    def getStagingSystemVersion(self):
        return self._stagingSystemVersion

    def getStagingSystemVersionTier(self):
        return self._stagingSystemVersionTier

    def getSpecificStage(self):
        return self._specificStage

    def getSpecificStageTier(self):
        return self._specificStageTier

    def getCancerSpecificBiomarkers(self):
        return self._cancerSpecificBiomarkers

    def getCancerSpecificBiomarkersTier(self):
        return self._cancerSpecificBiomarkersTier

    def getAdditionalMolecularDiagnosticTestingPerformed(self):
        return self._additionalMolecularDiagnosticTestingPerformed

    def getAdditionalMolecularDiagnosticTestingPerformedTier(self):
        return self._additionalMolecularDiagnosticTestingPerformedTier

    def getAdditionalTest(self):
        return self._additionalTest

    def getAdditionalTestTier(self):
        return self._additionalTestTier


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
        self._patientIdTier = None
        self._sampleId = None
        self._sampleIdTier = None
        self._diagnosisId = None
        self._diagnosisIdTier = None
        self._localBiobankId = None
        self._localBiobankIdTier = None
        self._collectionDate = None
        self._collectionDateTier = None
        self._collectionHospital = None
        self._collectionHospitalTier = None
        self._sampleType = None
        self._sampleTypeTier = None
        self._tissueDiseaseState = None
        self._tissueDiseaseStateTier = None
        self._anatomicSiteTheSampleObtainedFrom = None
        self._anatomicSiteTheSampleObtainedFromTier = None
        self._cancerType = None
        self._cancerTypeTier = None
        self._cancerSubtype = None
        self._cancerSubtypeTier = None
        self._pathologyReportId = None
        self._pathologyReportIdTier = None
        self._morphologicalCode = None
        self._morphologicalCodeTier = None
        self._topologicalCode = None
        self._topologicalCodeTier = None
        self._shippingDate = None
        self._shippingDateTier = None
        self._receivedDate = None
        self._receivedDateTier = None
        self._qualityControlPerformed = None
        self._qualityControlPerformedTier = None
        self._estimatedTumorContent = None
        self._estimatedTumorContentTier = None
        self._quantity = None
        self._quantityTier = None
        self._units = None
        self._unitsTier = None
        self._associatedBiobank = None
        self._associatedBiobankTier = None
        self._otherBiobank = None
        self._otherBiobankTier = None
        self._sopFollowed = None
        self._sopFollowedTier = None
        self._ifNotExplainAnyDeviation = None
        self._ifNotExplainAnyDeviationTier = None
        self._recordingDate = None
        self._recordingDateTier = None
        self._startInterval = None
        self._startIntervalTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "sampleId": self.getSampleId,
            "diagnosisId": self.getDiagnosisId,
            "localBiobankId": self.getLocalBiobankId,
            "collectionDate": self.getCollectionDate,
            "collectionHospital": self.getCollectionHospital,
            "sampleType": self.getSampleType,
            "tissueDiseaseState": self.getTissueDiseaseState,
            "anatomicSiteTheSampleObtainedFrom": self.getAnatomicSiteTheSampleObtainedFrom,
            "cancerType": self.getCancerType,
            "cancerSubtype": self.getCancerSubtype,
            "pathologyReportId": self.getPathologyReportId,
            "morphologicalCode": self.getMorphologicalCode,
            "topologicalCode": self.getTopologicalCode,
            "shippingDate": self.getShippingDate,
            "receivedDate": self.getReceivedDate,
            "qualityControlPerformed": self.getQualityControlPerformed,
            "estimatedTumorContent": self.getEstimatedTumorContent,
            "quantity": self.getQuantity,
            "units": self.getUnits,
            "associatedBiobank": self.getAssociatedBiobank,
            "otherBiobank": self.getOtherBiobank,
            "sopFollowed": self.getSopFollowed,
            "ifNotExplainAnyDeviation": self.getIfNotExplainAnyDeviation,
            "recordingDate": self.getRecordingDate,
            "startInterval": self.getStartInterval
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        try:
            # Unique fields
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getSampleIdTier():
                record['sampleId'] = self.getSampleId()
            if tier >= self.getDiagnosisIdTier():
                record['diagnosisId'] = self.getDiagnosisId()
            if tier >= self.getLocalBiobankIdTier():
                record['localBiobankId'] = self.getLocalBiobankId()
            if tier >= self.getCollectionDateTier():
                record['collectionDate'] = self.getCollectionDate()
            if tier >= self.getCollectionHospitalTier():
                record['collectionHospital'] = self.getCollectionHospital()
            if tier >= self.getSampleTypeTier():
                record['sampleType'] = self.getSampleType()
            if tier >= self.getTissueDiseaseStateTier():
                record['tissueDiseaseState'] = self.getTissueDiseaseState()
            if tier >= self.getAnatomicSiteTheSampleObtainedFromTier():
                record['anatomicSiteTheSampleObtainedFrom'] = self.getAnatomicSiteTheSampleObtainedFrom()
            if tier >= self.getCancerTypeTier():
                record['cancerType'] = self.getCancerType()
            if tier >= self.getCancerSubtypeTier():
                record['cancerSubtype'] = self.getCancerSubtype()
            if tier >= self.getPathologyReportIdTier():
                record['pathologyReportId'] = self.getPathologyReportId()
            if tier >= self.getMorphologicalCodeTier():
                record['morphologicalCode'] = self.getMorphologicalCode()
            if tier >= self.getTopologicalCodeTier():
                record['topologicalCode'] = self.getTopologicalCode()
            if tier >= self.getShippingDateTier():
                record['shippingDate'] = self.getShippingDate()
            if tier >= self.getReceivedDateTier():
                record['receivedDate'] = self.getReceivedDate()
            if tier >= self.getQualityControlPerformedTier():
                record['qualityControlPerformed'] = self.getQualityControlPerformed()
            if tier >= self.getEstimatedTumorContentTier():
                record['estimatedTumorContent'] = self.getEstimatedTumorContent()
            if tier >= self.getQuantityTier():
                record['quantity'] = self.getQuantity()
            if tier >= self.getUnitsTier():
                record['units'] = self.getUnits()
            if tier >= self.getAssociatedBiobankTier():
                record['associatedBiobank'] = self.getAssociatedBiobank()
            if tier >= self.getOtherBiobankTier():
                record['otherBiobank'] = self.getOtherBiobank()
            if tier >= self.getSopFollowedTier():
                record['sopFollowed'] = self.getSopFollowed()
            if tier >= self.getIfNotExplainAnyDeviationTier():
                record['ifNotExplainAnyDeviation'] = self.getIfNotExplainAnyDeviation()
            if tier >= self.getRecordingDateTier():
                record['recordingDate'] = self.getRecordingDate()
            if tier >= self.getStartIntervalTier():
                record['startInterval'] = self.getStartInterval()
        except TypeError:
            pass

        Sample = protocol.Sample(**record)
        self.serializeMetadataAttributes(Sample)

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
        self._patientIdTier = SampleRecord.patientIdTier
        self._sampleId = SampleRecord.sampleId
        self._sampleIdTier = SampleRecord.sampleIdTier
        self._diagnosisId = SampleRecord.diagnosisId
        self._diagnosisIdTier = SampleRecord.diagnosisIdTier
        self._localBiobankId = SampleRecord.localBiobankId
        self._localBiobankIdTier = SampleRecord.localBiobankIdTier
        self._collectionDate = SampleRecord.collectionDate
        self._collectionDateTier = SampleRecord.collectionDateTier
        self._collectionHospital = SampleRecord.collectionHospital
        self._collectionHospitalTier = SampleRecord.collectionHospitalTier
        self._sampleType = SampleRecord.sampleType
        self._sampleTypeTier = SampleRecord.sampleTypeTier
        self._tissueDiseaseState = SampleRecord.tissueDiseaseState
        self._tissueDiseaseStateTier = SampleRecord.tissueDiseaseStateTier
        self._anatomicSiteTheSampleObtainedFrom = SampleRecord.anatomicSiteTheSampleObtainedFrom
        self._anatomicSiteTheSampleObtainedFromTier = SampleRecord.anatomicSiteTheSampleObtainedFromTier
        self._cancerType = SampleRecord.cancerType
        self._cancerTypeTier = SampleRecord.cancerTypeTier
        self._cancerSubtype = SampleRecord.cancerSubtype
        self._cancerSubtypeTier = SampleRecord.cancerSubtypeTier
        self._pathologyReportId = SampleRecord.pathologyReportId
        self._pathologyReportIdTier = SampleRecord.pathologyReportIdTier
        self._morphologicalCode = SampleRecord.morphologicalCode
        self._morphologicalCodeTier = SampleRecord.morphologicalCodeTier
        self._topologicalCode = SampleRecord.topologicalCode
        self._topologicalCodeTier = SampleRecord.topologicalCodeTier
        self._shippingDate = SampleRecord.shippingDate
        self._shippingDateTier = SampleRecord.shippingDateTier
        self._receivedDate = SampleRecord.receivedDate
        self._receivedDateTier = SampleRecord.receivedDateTier
        self._qualityControlPerformed = SampleRecord.qualityControlPerformed
        self._qualityControlPerformedTier = SampleRecord.qualityControlPerformedTier
        self._estimatedTumorContent = SampleRecord.estimatedTumorContent
        self._estimatedTumorContentTier = SampleRecord.estimatedTumorContentTier
        self._quantity = SampleRecord.quantity
        self._quantityTier = SampleRecord.quantityTier
        self._units = SampleRecord.units
        self._unitsTier = SampleRecord.unitsTier
        self._associatedBiobank = SampleRecord.associatedBiobank
        self._associatedBiobankTier = SampleRecord.associatedBiobankTier
        self._otherBiobank = SampleRecord.otherBiobank
        self._otherBiobankTier = SampleRecord.otherBiobankTier
        self._sopFollowed = SampleRecord.sopFollowed
        self._sopFollowedTier = SampleRecord.sopFollowedTier
        self._ifNotExplainAnyDeviation = SampleRecord.ifNotExplainAnyDeviation
        self._ifNotExplainAnyDeviationTier = SampleRecord.ifNotExplainAnyDeviationTier
        self._recordingDate = SampleRecord.recordingDate
        self._recordingDateTier = SampleRecord.recordingDateTier
        self._startInterval = SampleRecord.startInterval
        self._startIntervalTier = SampleRecord.startIntervalTier

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
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._sampleId = parsed.sampleId
        self._sampleIdTier = parsed.sampleIdTier
        self._diagnosisId = parsed.diagnosisId
        self._diagnosisIdTier = parsed.diagnosisIdTier
        self._localBiobankId = parsed.localBiobankId
        self._localBiobankIdTier = parsed.localBiobankIdTier
        self._collectionDate = parsed.collectionDate
        self._collectionDateTier = parsed.collectionDateTier
        self._collectionHospital = parsed.collectionHospital
        self._collectionHospitalTier = parsed.collectionHospitalTier
        self._sampleType = parsed.sampleType
        self._sampleTypeTier = parsed.sampleTypeTier
        self._tissueDiseaseState = parsed.tissueDiseaseState
        self._tissueDiseaseStateTier = parsed.tissueDiseaseStateTier
        self._anatomicSiteTheSampleObtainedFrom = parsed.anatomicSiteTheSampleObtainedFrom
        self._anatomicSiteTheSampleObtainedFromTier = parsed.anatomicSiteTheSampleObtainedFromTier
        self._cancerType = parsed.cancerType
        self._cancerTypeTier = parsed.cancerTypeTier
        self._cancerSubtype = parsed.cancerSubtype
        self._cancerSubtypeTier = parsed.cancerSubtypeTier
        self._pathologyReportId = parsed.pathologyReportId
        self._pathologyReportIdTier = parsed.pathologyReportIdTier
        self._morphologicalCode = parsed.morphologicalCode
        self._morphologicalCodeTier = parsed.morphologicalCodeTier
        self._topologicalCode = parsed.topologicalCode
        self._topologicalCodeTier = parsed.topologicalCodeTier
        self._shippingDate = parsed.shippingDate
        self._shippingDateTier = parsed.shippingDateTier
        self._receivedDate = parsed.receivedDate
        self._receivedDateTier = parsed.receivedDateTier
        self._qualityControlPerformed = parsed.qualityControlPerformed
        self._qualityControlPerformedTier = parsed.qualityControlPerformedTier
        self._estimatedTumorContent = parsed.estimatedTumorContent
        self._estimatedTumorContentTier = parsed.estimatedTumorContentTier
        self._quantity = parsed.quantity
        self._quantityTier = parsed.quantityTier
        self._units = parsed.units
        self._unitsTier = parsed.unitsTier
        self._associatedBiobank = parsed.associatedBiobank
        self._associatedBiobankTier = parsed.associatedBiobankTier
        self._otherBiobank = parsed.otherBiobank
        self._otherBiobankTier = parsed.otherBiobankTier
        self._sopFollowed = parsed.sopFollowed
        self._sopFollowedTier = parsed.sopFollowedTier
        self._ifNotExplainAnyDeviation = parsed.ifNotExplainAnyDeviation
        self._ifNotExplainAnyDeviationTier = parsed.ifNotExplainAnyDeviationTier
        self._recordingDate = parsed.recordingDate
        self._recordingDateTier = parsed.recordingDateTier
        self._startInterval = parsed.startInterval
        self._startIntervalTier = parsed.startIntervalTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getSampleId(self):
        return self._sampleId

    def getSampleIdTier(self):
        return self._sampleIdTier

    def getDiagnosisId(self):
        return self._diagnosisId

    def getDiagnosisIdTier(self):
        return self._diagnosisIdTier

    def getLocalBiobankId(self):
        return self._localBiobankId

    def getLocalBiobankIdTier(self):
        return self._localBiobankIdTier

    def getCollectionDate(self):
        return self._collectionDate

    def getCollectionDateTier(self):
        return self._collectionDateTier

    def getCollectionHospital(self):
        return self._collectionHospital

    def getCollectionHospitalTier(self):
        return self._collectionHospitalTier

    def getSampleType(self):
        return self._sampleType

    def getSampleTypeTier(self):
        return self._sampleTypeTier

    def getTissueDiseaseState(self):
        return self._tissueDiseaseState

    def getTissueDiseaseStateTier(self):
        return self._tissueDiseaseStateTier

    def getAnatomicSiteTheSampleObtainedFrom(self):
        return self._anatomicSiteTheSampleObtainedFrom

    def getAnatomicSiteTheSampleObtainedFromTier(self):
        return self._anatomicSiteTheSampleObtainedFromTier

    def getCancerType(self):
        return self._cancerType

    def getCancerTypeTier(self):
        return self._cancerTypeTier

    def getCancerSubtype(self):
        return self._cancerSubtype

    def getCancerSubtypeTier(self):
        return self._cancerSubtypeTier

    def getPathologyReportId(self):
        return self._pathologyReportId

    def getPathologyReportIdTier(self):
        return self._pathologyReportIdTier

    def getMorphologicalCode(self):
        return self._morphologicalCode

    def getMorphologicalCodeTier(self):
        return self._morphologicalCodeTier

    def getTopologicalCode(self):
        return self._topologicalCode

    def getTopologicalCodeTier(self):
        return self._topologicalCodeTier

    def getShippingDate(self):
        return self._shippingDate

    def getShippingDateTier(self):
        return self._shippingDateTier

    def getReceivedDate(self):
        return self._receivedDate

    def getReceivedDateTier(self):
        return self._receivedDateTier

    def getQualityControlPerformed(self):
        return self._qualityControlPerformed

    def getQualityControlPerformedTier(self):
        return self._qualityControlPerformedTier

    def getEstimatedTumorContent(self):
        return self._estimatedTumorContent

    def getEstimatedTumorContentTier(self):
        return self._estimatedTumorContentTier

    def getQuantity(self):
        return self._quantity

    def getQuantityTier(self):
        return self._quantityTier

    def getUnits(self):
        return self._units

    def getUnitsTier(self):
        return self._unitsTier

    def getAssociatedBiobank(self):
        return self._associatedBiobank

    def getAssociatedBiobankTier(self):
        return self._associatedBiobankTier

    def getOtherBiobank(self):
        return self._otherBiobank

    def getOtherBiobankTier(self):
        return self._otherBiobankTier

    def getSopFollowed(self):
        return self._sopFollowed

    def getSopFollowedTier(self):
        return self._sopFollowedTier

    def getIfNotExplainAnyDeviation(self):
        return self._ifNotExplainAnyDeviation

    def getIfNotExplainAnyDeviationTier(self):
        return self._ifNotExplainAnyDeviationTier

    def getRecordingDate(self):
        return self._recordingDate

    def getRecordingDateTier(self):
        return self._recordingDateTier

    def getStartInterval(self):
        return self._startInterval

    def getStartIntervalTier(self):
        return self._startIntervalTier


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
        self._patientIdTier = None
        self._courseNumber = None
        self._courseNumberTier = None
        self._therapeuticModality = None
        self._therapeuticModalityTier = None
        self._treatmentPlanType = None
        self._treatmentPlanTypeTier = None
        self._treatmentIntent = None
        self._treatmentIntentTier = None
        self._startDate = None
        self._startDateTier = None
        self._stopDate = None
        self._stopDateTier = None
        self._reasonForEndingTheTreatment = None
        self._reasonForEndingTheTreatmentTier = None
        self._responseToTreatment = None
        self._responseToTreatmentTier = None
        self._responseCriteriaUsed = None
        self._responseCriteriaUsedTier = None
        self._dateOfRecurrenceOrProgressionAfterThisTreatment = None
        self._dateOfRecurrenceOrProgressionAfterThisTreatmentTier = None
        self._unexpectedOrUnusualToxicityDuringTreatment = None
        self._unexpectedOrUnusualToxicityDuringTreatmentTier = None
        self._diagnosisId = None
        self._diagnosisIdTier = None
        self._treatmentPlanId = None
        self._treatmentPlanIdTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "courseNumber": self.getCourseNumber,
            "therapeuticModality": self.getTherapeuticModality,
            "treatmentPlanType": self.getTreatmentPlanType,
            "treatmentIntent": self.getTreatmentIntent,
            "startDate": self.getStartDate,
            "stopDate": self.getStopDate,
            "reasonForEndingTheTreatment": self.getReasonForEndingTheTreatment,
            "responseToTreatment": self.getResponseToTreatment,
            "responseCriteriaUsed": self.getResponseCriteriaUsed,
            "dateOfRecurrenceOrProgressionAfterThisTreatment": self.getDateOfRecurrenceOrProgressionAfterThisTreatment,
            'unexpectedOrUnusualToxicityDuringTreatment': self.getUnexpectedOrUnusualToxicityDuringTreatment,
            "diagnosisId": self.getDiagnosisId,
            "treatmentPlanId": self.getTreatmentPlanId,
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        try:
            # Unique fields
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getCourseNumberTier():
                record['courseNumber'] = self.getCourseNumber()
            if tier >= self.getTherapeuticModalityTier():
                record['therapeuticModality'] = self.getTherapeuticModality()
            if tier >= self.getTreatmentPlanTypeTier():
                record['treatmentPlanType'] = self.getTreatmentPlanType()
            if tier >= self.getTreatmentIntentTier():
                record['treatmentIntent'] = self.getTreatmentIntent()
            if tier >= self.getStartDateTier():
                record['startDate'] = self.getStartDate()
            if tier >= self.getStopDateTier():
                record['stopDate'] = self.getStopDate()
            if tier >= self.getReasonForEndingTheTreatmentTier():
                record['reasonForEndingTheTreatment'] = self.getReasonForEndingTheTreatment()
            if tier >= self.getResponseToTreatmentTier():
                record['responseToTreatment'] = self.getResponseToTreatment()
            if tier >= self.getResponseCriteriaUsedTier():
                record['responseCriteriaUsed'] = self.getResponseCriteriaUsed()
            if tier >= self.getDateOfRecurrenceOrProgressionAfterThisTreatmentTier():
                record['dateOfRecurrenceOrProgressionAfterThisTreatment'] = self.getDateOfRecurrenceOrProgressionAfterThisTreatment()
            if tier >= self.getUnexpectedOrUnusualToxicityDuringTreatmentTier():
                record['unexpectedOrUnusualToxicityDuringTreatment'] = self.getUnexpectedOrUnusualToxicityDuringTreatment()
            if tier >= self.getDiagnosisIdTier():
                record['diagnosisId'] = self.getDiagnosisId()
            if tier >= self.getTreatmentPlanIdTier():
                record['treatmentPlanId'] = self.getTreatmentPlanId()
        except TypeError:
            pass

        Treatment = protocol.Treatment(**record)
        self.serializeMetadataAttributes(Treatment)

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
        self._patientIdTier = TreatmentRecord.patientIdTier
        self._courseNumber = TreatmentRecord.courseNumber
        self._courseNumberTier = TreatmentRecord.courseNumberTier
        self._therapeuticModality = TreatmentRecord.therapeuticModality
        self._therapeuticModalityTier = TreatmentRecord.therapeuticModalityTier
        self._treatmentPlanType = TreatmentRecord.treatmentPlanType
        self._treatmentPlanTypeTier = TreatmentRecord.treatmentPlanTypeTier
        self._treatmentIntent = TreatmentRecord.treatmentIntent
        self._treatmentIntentTier = TreatmentRecord.treatmentIntentTier
        self._startDate = TreatmentRecord.startDate
        self._startDateTier = TreatmentRecord.startDateTier
        self._stopDate = TreatmentRecord.stopDate
        self._stopDateTier = TreatmentRecord.stopDateTier
        self._reasonForEndingTheTreatment = TreatmentRecord.reasonForEndingTheTreatment
        self._reasonForEndingTheTreatmentTier = TreatmentRecord.reasonForEndingTheTreatmentTier
        self._responseToTreatment = TreatmentRecord.responseToTreatment
        self._responseToTreatmentTier = TreatmentRecord.responseToTreatmentTier
        self._responseCriteriaUsed = TreatmentRecord.responseCriteriaUsed
        self._responseCriteriaUsedTier = TreatmentRecord.responseCriteriaUsedTier
        self._dateOfRecurrenceOrProgressionAfterThisTreatment = TreatmentRecord.dateOfRecurrenceOrProgressionAfterThisTreatment
        self._dateOfRecurrenceOrProgressionAfterThisTreatmentTier = TreatmentRecord.dateOfRecurrenceOrProgressionAfterThisTreatmentTier
        self._unexpectedOrUnusualToxicityDuringTreatment = TreatmentRecord.unexpectedOrUnusualToxicityDuringTreatment
        self._unexpectedOrUnusualToxicityDuringTreatmentTier = TreatmentRecord.unexpectedOrUnusualToxicityDuringTreatmentTier
        self._diagnosisId = TreatmentRecord.diagnosisId
        self._diagnosisIdTier = TreatmentRecord.diagnosisIdTier
        self._treatmentPlanId = TreatmentRecord.treatmentPlanId
        self._treatmentPlanIdTier = TreatmentRecord.treatmentPlanIdTier

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
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._courseNumber = parsed.courseNumber
        self._courseNumberTier = parsed.courseNumberTier
        self._therapeuticModality = parsed.therapeuticModality
        self._therapeuticModalityTier = parsed.therapeuticModalityTier
        self._treatmentPlanType = parsed.treatmentPlanType
        self._treatmentPlanTypeTier = parsed.treatmentPlanTypeTier
        self._treatmentIntent = parsed.treatmentIntent
        self._treatmentIntentTier = parsed.treatmentIntentTier
        self._startDate = parsed.startDate
        self._startDateTier = parsed.startDateTier
        self._stopDate = parsed.stopDate
        self._stopDateTier = parsed.stopDateTier
        self._reasonForEndingTheTreatment = parsed.reasonForEndingTheTreatment
        self._reasonForEndingTheTreatmentTier = parsed.reasonForEndingTheTreatmentTier
        self._responseToTreatment = parsed.responseToTreatment
        self._responseToTreatmentTier = parsed.responseToTreatmentTier
        self._responseCriteriaUsed = parsed.responseCriteriaUsed
        self._responseCriteriaUsedTier = parsed.responseCriteriaUsedTier
        self._dateOfRecurrenceOrProgressionAfterThisTreatment = parsed.dateOfRecurrenceOrProgressionAfterThisTreatment
        self._dateOfRecurrenceOrProgressionAfterThisTreatmentTier = parsed.dateOfRecurrenceOrProgressionAfterThisTreatmentTier
        self._unexpectedOrUnusualToxicityDuringTreatment = parsed.unexpectedOrUnusualToxicityDuringTreatment
        self._unexpectedOrUnusualToxicityDuringTreatmentTier = parsed.unexpectedOrUnusualToxicityDuringTreatmentTier
        self._diagnosisId = parsed.diagnosisId
        self._diagnosisIdTier = parsed.diagnosisIdTier
        self._treatmentPlanId = parsed.treatmentPlanId
        self._treatmentPlanIdTier = parsed.treatmentPlanIdTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getCourseNumber(self):
        return self._courseNumber

    def getCourseNumberTier(self):
        return self._courseNumberTier

    def getTherapeuticModality(self):
        return self._therapeuticModality

    def getTherapeuticModalityTier(self):
        return self._therapeuticModalityTier

    def getTreatmentPlanType(self):
        return self._treatmentPlanType

    def getTreatmentPlanTypeTier(self):
        return self._treatmentPlanTypeTier

    def getTreatmentIntent(self):
        return self._treatmentIntent

    def getTreatmentIntentTier(self):
        return self._treatmentIntentTier

    def getStartDate(self):
        return self._startDate

    def getStartDateTier(self):
        return self._startDateTier

    def getStopDate(self):
        return self._stopDate

    def getStopDateTier(self):
        return self._stopDateTier

    def getReasonForEndingTheTreatment(self):
        return self._reasonForEndingTheTreatment

    def getReasonForEndingTheTreatmentTier(self):
        return self._reasonForEndingTheTreatmentTier

    def getResponseToTreatment(self):
        return self._responseToTreatment

    def getResponseToTreatmentTier(self):
        return self._responseToTreatmentTier

    def getResponseCriteriaUsed(self):
        return self._responseCriteriaUsed

    def getResponseCriteriaUsedTier(self):
        return self._responseCriteriaUsedTier

    def getDateOfRecurrenceOrProgressionAfterThisTreatment(self):
        return self._dateOfRecurrenceOrProgressionAfterThisTreatment

    def getDateOfRecurrenceOrProgressionAfterThisTreatmentTier(self):
        return self._dateOfRecurrenceOrProgressionAfterThisTreatmentTier

    def getUnexpectedOrUnusualToxicityDuringTreatment(self):
        return self._unexpectedOrUnusualToxicityDuringTreatment

    def getUnexpectedOrUnusualToxicityDuringTreatmentTier(self):
        return self._unexpectedOrUnusualToxicityDuringTreatmentTier

    def getDiagnosisId(self):
        return self._diagnosisId

    def getDiagnosisIdTier(self):
        return self._diagnosisIdTier

    def getTreatmentPlanId(self):
        return self._treatmentPlanId

    def getTreatmentPlanIdTier(self):
        return self._treatmentPlanIdTier


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
        self._patientIdTier = None
        self._physicalExamId = None
        self._physicalExamIdTier = None
        self._dateOfAssessment = None
        self._dateOfAssessmentTier = None
        self._diseaseResponseOrStatus = None
        self._diseaseResponseOrStatusTier = None
        self._otherResponseClassification = None
        self._otherResponseClassificationTier = None
        self._minimalResidualDiseaseAssessment = None
        self._minimalResidualDiseaseAssessmentTier = None
        self._methodOfResponseEvaluation = None
        self._methodOfResponseEvaluationTier = None
        self._responseCriteriaUsed = None
        self._responseCriteriaUsedTier = None
        self._summaryStage = None
        self._summaryStageTier = None
        self._sitesOfAnyProgressionOrRecurrence = None
        self._sitesOfAnyProgressionOrRecurrenceTier = None
        self._vitalStatus = None
        self._vitalStatusTier = None
        self._height = None
        self._heightTier = None
        self._weight = None
        self._weightTier = None
        self._heightUnits = None
        self._heightUnitsTier = None
        self._weightUnits = None
        self._weightUnitsTier = None
        self._performanceStatus = None
        self._performanceStatusTier = None
        self._overallSurvivalInMonths = None
        self._overallSurvivalInMonthsTier = None
        self._diseaseFreeSurvivalInMonths = None
        self._diseaseFreeSurvivalInMonthsTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "physicalExamId": self.getPhysicalExamId,
            "dateOfAssessment": self.getDateOfAssessment,
            "diseaseResponseOrStatus": self.getDiseaseResponseOrStatus,
            "otherResponseClassification": self.getOtherResponseClassification,
            "minimalResidualDiseaseAssessment": self.getMinimalResidualDiseaseAssessment,
            "methodOfResponseEvaluation": self.getMethodOfResponseEvaluation,
            "responseCriteriaUsed": self.getResponseCriteriaUsed,
            "summaryStage": self.getSummaryStage,
            "sitesOfAnyProgressionOrRecurrence": self.getSitesOfAnyProgressionOrRecurrence,
            "vitalStatus": self.getVitalStatus,
            "height": self.getHeight,
            "weight": self.getWeight,
            "heightUnits": self.getHeightUnits,
            "weightUnits": self.getWeightUnits,
            "performanceStatus": self.getPerformanceStatus,
            "overallSurvivalInMonths": self.getOverallSurvivalInMonths,
            "diseaseFreeSurvivalInMonths": self.getDiseaseFreeSurvivalInMonths
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        try:
            # Unique fields
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getPhysicalExamIdTier():
                record['physicalExamId'] = self.getPhysicalExamId()
            if tier >= self.getDateOfAssessmentTier():
                record['dateOfAssessment'] = self.getDateOfAssessment()
            if tier >= self.getDiseaseResponseOrStatusTier():
                record['diseaseResponseOrStatus'] = self.getDiseaseResponseOrStatus()
            if tier >= self.getOtherResponseClassificationTier():
                record['otherResponseClassification'] = self.getOtherResponseClassification()
            if tier >= self.getMinimalResidualDiseaseAssessmentTier():
                record['minimalResidualDiseaseAssessment'] = self.getMinimalResidualDiseaseAssessment()
            if tier >= self.getMethodOfResponseEvaluationTier():
                record['methodOfResponseEvaluation'] = self.getMethodOfResponseEvaluation()
            if tier >= self.getResponseCriteriaUsedTier():
                record['responseCriteriaUsed'] = self.getResponseCriteriaUsed()
            if tier >= self.getSummaryStageTier():
                record['summaryStage'] = self.getSummaryStage()
            if tier >= self.getSitesOfAnyProgressionOrRecurrenceTier():
                record['sitesOfAnyProgressionOrRecurrence'] = self.getSitesOfAnyProgressionOrRecurrence()
            if tier >= self.getVitalStatusTier():
                record['vitalStatus'] = self.getVitalStatus()
            if tier >= self.getHeightTier():
                record['height'] = self.getHeight()
            if tier >= self.getWeightTier():
                record['weight'] = self.getWeight()
            if tier >= self.getHeightUnitsTier():
                record['heightUnits'] = self.getHeightUnits()
            if tier >= self.getWeightUnitsTier():
                record['weightUnits'] = self.getWeightUnits()
            if tier >= self.getPerformanceStatusTier():
                record['performanceStatus'] = self.getPerformanceStatus()
            if tier >= self.getOverallSurvivalInMonthsTier():
                record['overallSurvivalInMonths'] = self.getOverallSurvivalInMonths()
            if tier >= self.getDiseaseFreeSurvivalInMonthsTier():
                record['diseaseFreeSurvivalInMonths'] = self.getDiseaseFreeSurvivalInMonths()
        except TypeError:
            pass

        Outcome = protocol.Outcome(**record)
        self.serializeMetadataAttributes(Outcome)

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
        self._patientIdTier = OutcomeRecord.patientIdTier
        self._physicalExamId = OutcomeRecord.physicalExamId
        self._physicalExamIdTier = OutcomeRecord.physicalExamIdTier
        self._dateOfAssessment = OutcomeRecord.dateOfAssessment
        self._dateOfAssessmentTier = OutcomeRecord.dateOfAssessmentTier
        self._diseaseResponseOrStatus = OutcomeRecord.diseaseResponseOrStatus
        self._diseaseResponseOrStatusTier = OutcomeRecord.diseaseResponseOrStatusTier
        self._otherResponseClassification = OutcomeRecord.otherResponseClassification
        self._otherResponseClassificationTier = OutcomeRecord.otherResponseClassificationTier
        self._minimalResidualDiseaseAssessment = OutcomeRecord.minimalResidualDiseaseAssessment
        self._minimalResidualDiseaseAssessmentTier = OutcomeRecord.minimalResidualDiseaseAssessmentTier
        self._methodOfResponseEvaluation = OutcomeRecord.methodOfResponseEvaluation
        self._methodOfResponseEvaluationTier = OutcomeRecord.methodOfResponseEvaluationTier
        self._responseCriteriaUsed = OutcomeRecord.responseCriteriaUsed
        self._responseCriteriaUsedTier = OutcomeRecord.responseCriteriaUsedTier
        self._summaryStage = OutcomeRecord.summaryStage
        self._summaryStageTier = OutcomeRecord.summaryStageTier
        self._sitesOfAnyProgressionOrRecurrence = OutcomeRecord.sitesOfAnyProgressionOrRecurrence
        self._sitesOfAnyProgressionOrRecurrenceTier = OutcomeRecord.sitesOfAnyProgressionOrRecurrenceTier
        self._vitalStatus = OutcomeRecord.vitalStatus
        self._vitalStatusTier = OutcomeRecord.vitalStatusTier
        self._height = OutcomeRecord.height
        self._heightTier = OutcomeRecord.heightTier
        self._weight = OutcomeRecord.weight
        self._weightTier = OutcomeRecord.weightTier
        self._heightUnits = OutcomeRecord.heightUnits
        self._heightUnitsTier = OutcomeRecord.heightUnitsTier
        self._weightUnits = OutcomeRecord.weightUnits
        self._weightUnitsTier = OutcomeRecord.weightUnitsTier
        self._performanceStatus = OutcomeRecord.performanceStatus
        self._performanceStatusTier = OutcomeRecord.performanceStatusTier
        self._overallSurvivalInMonths = OutcomeRecord.overallSurvivalInMonths
        self._overallSurvivalInMonthsTier = OutcomeRecord.overallSurvivalInMonthsTier
        self._diseaseFreeSurvivalInMonths = OutcomeRecord.diseaseFreeSurvivalInMonths
        self._diseaseFreeSurvivalInMonthsTier = OutcomeRecord.diseaseFreeSurvivalInMonthsTier

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
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._physicalExamId = parsed.physicalExamId
        self._physicalExamIdTier = parsed.physicalExamIdTier
        self._dateOfAssessment = parsed.dateOfAssessment
        self._dateOfAssessmentTier = parsed.dateOfAssessmentTier
        self._diseaseResponseOrStatus = parsed.diseaseResponseOrStatus
        self._diseaseResponseOrStatusTier = parsed.diseaseResponseOrStatusTier
        self._otherResponseClassification = parsed.otherResponseClassification
        self._otherResponseClassificationTier = parsed.otherResponseClassificationTier
        self._minimalResidualDiseaseAssessment = parsed.minimalResidualDiseaseAssessment
        self._minimalResidualDiseaseAssessmentTier = parsed.minimalResidualDiseaseAssessmentTier
        self._methodOfResponseEvaluation = parsed.methodOfResponseEvaluation
        self._methodOfResponseEvaluationTier = parsed.methodOfResponseEvaluationTier
        self._responseCriteriaUsed = parsed.responseCriteriaUsed
        self._responseCriteriaUsedTier = parsed.responseCriteriaUsedTier
        self._summaryStage = parsed.summaryStage
        self._summaryStageTier = parsed.summaryStageTier
        self._sitesOfAnyProgressionOrRecurrence = parsed.sitesOfAnyProgressionOrRecurrence
        self._sitesOfAnyProgressionOrRecurrenceTier = parsed.sitesOfAnyProgressionOrRecurrenceTier
        self._vitalStatus = parsed.vitalStatus
        self._vitalStatusTier = parsed.vitalStatusTier
        self._height = parsed.height
        self._heightTier = parsed.heightTier
        self._weight = parsed.weight
        self._weightTier = parsed.weightTier
        self._heightUnits = parsed.heightUnits
        self._heightUnitsTier = parsed.heightUnitsTier
        self._weightUnits = parsed.weightUnits
        self._weightUnitsTier = parsed.weightUnitsTier
        self._performanceStatus = parsed.performanceStatus
        self._performanceStatusTier = parsed.performanceStatusTier
        self._overallSurvivalInMonths = parsed.overallSurvivalInMonths
        self._overallSurvivalInMonthsTier = parsed.overallSurvivalInMonthsTier
        self._diseaseFreeSurvivalInMonths = parsed.diseaseFreeSurvivalInMonths
        self._diseaseFreeSurvivalInMonthsTier = parsed.diseaseFreeSurvivalInMonthsTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getPhysicalExamId(self):
        return self._physicalExamId

    def getPhysicalExamIdTier(self):
        return self._physicalExamIdTier

    def getDateOfAssessment(self):
        return self._dateOfAssessment

    def getDateOfAssessmentTier(self):
        return self._dateOfAssessmentTier

    def getDiseaseResponseOrStatus(self):
        return self._diseaseResponseOrStatus

    def getDiseaseResponseOrStatusTier(self):
        return self._diseaseResponseOrStatusTier

    def getOtherResponseClassification(self):
        return self._otherResponseClassification

    def getOtherResponseClassificationTier(self):
        return self._otherResponseClassificationTier

    def getMinimalResidualDiseaseAssessment(self):
        return self._minimalResidualDiseaseAssessment

    def getMinimalResidualDiseaseAssessmentTier(self):
        return self._minimalResidualDiseaseAssessmentTier

    def getMethodOfResponseEvaluation(self):
        return self._methodOfResponseEvaluation

    def getMethodOfResponseEvaluationTier(self):
        return self._methodOfResponseEvaluationTier

    def getResponseCriteriaUsed(self):
        return self._responseCriteriaUsed

    def getResponseCriteriaUsedTier(self):
        return self._responseCriteriaUsedTier

    def getSummaryStage(self):
        return self._summaryStage

    def getSummaryStageTier(self):
        return self._summaryStageTier

    def getSitesOfAnyProgressionOrRecurrence(self):
        return self._sitesOfAnyProgressionOrRecurrence

    def getSitesOfAnyProgressionOrRecurrenceTier(self):
        return self._sitesOfAnyProgressionOrRecurrenceTier

    def getVitalStatus(self):
        return self._vitalStatus

    def getVitalStatusTier(self):
        return self._vitalStatusTier

    def getHeight(self):
        return self._height

    def getHeightTier(self):
        return self._heightTier

    def getWeight(self):
        return self._weight

    def getWeightTier(self):
        return self._weightTier

    def getHeightUnits(self):
        return self._heightUnits

    def getHeightUnitsTier(self):
        return self._heightUnitsTier

    def getWeightUnits(self):
        return self._weightUnits

    def getWeightUnitsTier(self):
        return self._weightUnitsTier

    def getPerformanceStatus(self):
        return self._performanceStatus

    def getPerformanceStatusTier(self):
        return self._performanceStatusTier

    def getOverallSurvivalInMonths(self):
        return self._overallSurvivalInMonths

    def getOverallSurvivalInMonthsTier(self):
        return self._overallSurvivalInMonthsTier

    def getDiseaseFreeSurvivalInMonths(self):
        return self._diseaseFreeSurvivalInMonths

    def getDiseaseFreeSurvivalInMonthsTier(self):
        return self._diseaseFreeSurvivalInMonthsTier


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
        self._patientIdTier = None
        self._date = None
        self._dateTier = None
        self._lateComplicationOfTherapyDeveloped = None
        self._lateComplicationOfTherapyDevelopedTier = None
        self._lateToxicityDetail = None
        self._lateToxicityDetailTier = None
        self._suspectedTreatmentInducedNeoplasmDeveloped = None
        self._suspectedTreatmentInducedNeoplasmDevelopedTier = None
        self._treatmentInducedNeoplasmDetails = None
        self._treatmentInducedNeoplasmDetailsTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "date": self.getDate,
            "lateComplicationOfTherapyDeveloped": self.getLateComplicationOfTherapyDeveloped,
            "lateToxicityDetail": self.getLateToxicityDetail,
            "suspectedTreatmentInducedNeoplasmDeveloped": self.getSuspectedTreatmentInducedNeoplasmDeveloped,
            "treatmentInducedNeoplasmDetails": self.getTreatmentInducedNeoplasmDetails
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getDateTier():
                record['date'] = self.getDate()
            if tier >= self.getLateComplicationOfTherapyDevelopedTier():
                record['lateComplicationOfTherapyDeveloped'] = self.getLateComplicationOfTherapyDeveloped()
            if tier >= self.getLateToxicityDetailTier():
                record['lateToxicityDetail'] = self.getLateToxicityDetail()
            if tier >= self.getSuspectedTreatmentInducedNeoplasmDevelopedTier():
                record['suspectedTreatmentInducedNeoplasmDeveloped'] = self.getSuspectedTreatmentInducedNeoplasmDeveloped()
            if tier >= self.getTreatmentInducedNeoplasmDetailsTier():
                record['treatmentInducedNeoplasmDetails'] = self.getTreatmentInducedNeoplasmDetails()
        except TypeError:
            pass

        Complication = protocol.Complication(**record)
        self.serializeMetadataAttributes(Complication)

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
        self._patientIdTier = ComplicationRecord.patientIdTier
        self._date = ComplicationRecord.date
        self._dateTier = ComplicationRecord.dateTier
        self._lateComplicationOfTherapyDeveloped = ComplicationRecord.lateComplicationOfTherapyDeveloped
        self._lateComplicationOfTherapyDevelopedTier = ComplicationRecord.lateComplicationOfTherapyDevelopedTier
        self._lateToxicityDetail = ComplicationRecord.lateToxicityDetail
        self._lateToxicityDetailTier = ComplicationRecord.lateToxicityDetailTier
        self._suspectedTreatmentInducedNeoplasmDeveloped = ComplicationRecord.suspectedTreatmentInducedNeoplasmDeveloped
        self._suspectedTreatmentInducedNeoplasmDevelopedTier = ComplicationRecord.suspectedTreatmentInducedNeoplasmDevelopedTier
        self._treatmentInducedNeoplasmDetails = ComplicationRecord.treatmentInducedNeoplasmDetails
        self._treatmentInducedNeoplasmDetailsTier = ComplicationRecord.treatmentInducedNeoplasmDetailsTier

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
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._date = parsed.date
        self._dateTier = parsed.dateTier
        self._lateComplicationOfTherapyDeveloped = parsed.lateComplicationOfTherapyDeveloped
        self._lateComplicationOfTherapyDevelopedTier = parsed.lateComplicationOfTherapyDevelopedTier
        self._lateToxicityDetail = parsed.lateToxicityDetail
        self._lateToxicityDetailTier = parsed.lateToxicityDetailTier
        self._suspectedTreatmentInducedNeoplasmDeveloped = parsed.suspectedTreatmentInducedNeoplasmDeveloped
        self._suspectedTreatmentInducedNeoplasmDevelopedTier = parsed.suspectedTreatmentInducedNeoplasmDevelopedTier
        self._treatmentInducedNeoplasmDetails = parsed.treatmentInducedNeoplasmDetails
        self._treatmentInducedNeoplasmDetailsTier = parsed.treatmentInducedNeoplasmDetailsTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getDate(self):
        return self._date

    def getDateTier(self):
        return self._dateTier

    def getLateComplicationOfTherapyDeveloped(self):
        return self._lateComplicationOfTherapyDeveloped

    def getLateComplicationOfTherapyDevelopedTier(self):
        return self._lateComplicationOfTherapyDevelopedTier

    def getLateToxicityDetail(self):
        return self._lateToxicityDetail

    def getLateToxicityDetailTier(self):
        return self._lateToxicityDetailTier

    def getSuspectedTreatmentInducedNeoplasmDeveloped(self):
        return self._suspectedTreatmentInducedNeoplasmDeveloped

    def getSuspectedTreatmentInducedNeoplasmDevelopedTier(self):
        return self._suspectedTreatmentInducedNeoplasmDevelopedTier

    def getTreatmentInducedNeoplasmDetails(self):
        return self._treatmentInducedNeoplasmDetails

    def getTreatmentInducedNeoplasmDetailsTier(self):
        return self._treatmentInducedNeoplasmDetailsTier


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
        self._patientIdTier = None
        self._dateOfMolecularTumorBoard = None
        self._dateOfMolecularTumorBoardTier = None
        self._typeOfSampleAnalyzed = None
        self._typeOfSampleAnalyzedTier = None
        self._typeOfTumourSampleAnalyzed = None
        self._typeOfTumourSampleAnalyzedTier = None
        self._analysesDiscussed = None
        self._analysesDiscussedTier = None
        self._somaticSampleType = None
        self._somaticSampleTypeTier = None
        self._normalExpressionComparator = None
        self._normalExpressionComparatorTier = None
        self._diseaseExpressionComparator = None
        self._diseaseExpressionComparatorTier = None
        self._hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer = None
        self._hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancerTier = None
        self._actionableTargetFound = None
        self._actionableTargetFoundTier = None
        self._molecularTumorBoardRecommendation = None
        self._molecularTumorBoardRecommendationTier = None
        self._germlineDnaSampleId = None
        self._germlineDnaSampleIdTier = None
        self._tumorDnaSampleId = None
        self._tumorDnaSampleIdTier = None
        self._tumorRnaSampleId = None
        self._tumorRnaSampleIdTier = None
        self._germlineSnvDiscussed = None
        self._germlineSnvDiscussedTier = None
        self._somaticSnvDiscussed = None
        self._somaticSnvDiscussedTier = None
        self._cnvsDiscussed = None
        self._cnvsDiscussedTier = None
        self._structuralVariantDiscussed = None
        self._structuralVariantDiscussedTier = None
        self._classificationOfVariants = None
        self._classificationOfVariantsTier = None
        self._clinicalValidationProgress = None
        self._clinicalValidationProgressTier = None
        self._typeOfValidation = None
        self._typeOfValidationTier = None
        self._agentOrDrugClass = None
        self._agentOrDrugClassTier = None
        self._levelOfEvidenceForExpressionTargetAgentMatch = None
        self._levelOfEvidenceForExpressionTargetAgentMatchTier = None
        self._didTreatmentPlanChangeBasedOnProfilingResult = None
        self._didTreatmentPlanChangeBasedOnProfilingResultTier = None
        self._howTreatmentHasAlteredBasedOnProfiling = None
        self._howTreatmentHasAlteredBasedOnProfilingTier = None
        self._reasonTreatmentPlanDidNotChangeBasedOnProfiling = None
        self._reasonTreatmentPlanDidNotChangeBasedOnProfilingTier = None
        self._detailsOfTreatmentPlanImpact = None
        self._detailsOfTreatmentPlanImpactTier = None
        self._patientOrFamilyInformedOfGermlineVariant = None
        self._patientOrFamilyInformedOfGermlineVariantTier = None
        self._patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling = None
        self._patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfilingTier = None
        self._summaryReport = None
        self._summaryReportTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "dateOfMolecularTumorBoard": self.getDateOfMolecularTumorBoard,
            "typeOfSampleAnalyzed": self.getTypeOfSampleAnalyzed,
            "typeOfTumourSampleAnalyzed": self.getTypeOfTumourSampleAnalyzed,
            "analysesDiscussed": self.getAnalysesDiscussed,
            "somaticSampleType": self.getSomaticSampleType,
            "normalExpressionComparator": self.getNormalExpressionComparator,
            "diseaseExpressionComparator": self.getDiseaseExpressionComparator,
            "hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer": self.getHasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer,
            "actionableTargetFound": self.getActionableTargetFound,
            "molecularTumorBoardRecommendation": self.getMolecularTumorBoardRecommendation,
            "germlineDnaSampleId": self.getGermlineDnaSampleId,
            "tumorDnaSampleId": self.getTumorDnaSampleId,
            "tumorRnaSampleId": self.getTumorRnaSampleId,
            "germlineSnvDiscussed": self.getGermlineSnvDiscussed,
            "somaticSnvDiscussed": self.getSomaticSnvDiscussed,
            "cnvsDiscussed": self.getCnvsDiscussed,
            "structuralVariantDiscussed": self.getStructuralVariantDiscussed,
            "classificationOfVariants": self.getClassificationOfVariants,
            "clinicalValidationProgress": self.getClinicalValidationProgress,
            "typeOfValidation": self.getTypeOfValidation,
            "agentOrDrugClass": self.getAgentOrDrugClass,
            "levelOfEvidenceForExpressionTargetAgentMatch": self.getLevelOfEvidenceForExpressionTargetAgentMatch,
            "didTreatmentPlanChangeBasedOnProfilingResult": self.getDidTreatmentPlanChangeBasedOnProfilingResult,
            "howTreatmentHasAlteredBasedOnProfiling": self.getHowTreatmentHasAlteredBasedOnProfiling,
            "reasonTreatmentPlanDidNotChangeBasedOnProfiling": self.getReasonTreatmentPlanDidNotChangeBasedOnProfiling,
            "detailsOfTreatmentPlanImpact": self.getDetailsOfTreatmentPlanImpact,
            "patientOrFamilyInformedOfGermlineVariant": self.getPatientOrFamilyInformedOfGermlineVariant,
            "patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling": self.getPatientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling,
            "summaryReport": self.getSummaryReport
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getDateOfMolecularTumorBoardTier():
                record['dateOfMolecularTumorBoard'] = self.getDateOfMolecularTumorBoard()
            if tier >= self.getTypeOfSampleAnalyzedTier():
                record['typeOfSampleAnalyzed'] = self.getTypeOfSampleAnalyzed()
            if tier >= self.getTypeOfTumourSampleAnalyzedTier():
                record['typeOfTumourSampleAnalyzed'] = self.getTypeOfTumourSampleAnalyzed()
            if tier >= self.getAnalysesDiscussedTier():
                record['analysesDiscussed'] = self.getAnalysesDiscussed()
            if tier >= self.getSomaticSampleTypeTier():
                record['somaticSampleType'] = self.getSomaticSampleType()
            if tier >= self.getNormalExpressionComparatorTier():
                record['normalExpressionComparator'] = self.getNormalExpressionComparator()
            if tier >= self.getDiseaseExpressionComparatorTier():
                record['diseaseExpressionComparator'] = self.getDiseaseExpressionComparator()
            if tier >= self.getHasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancerTier():
                record['hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer'] = self.getHasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer()
            if tier >= self.getActionableTargetFoundTier():
                record['actionableTargetFound'] = self.getActionableTargetFound()
            if tier >= self.getMolecularTumorBoardRecommendationTier():
                record['molecularTumorBoardRecommendation'] = self.getMolecularTumorBoardRecommendation()
            if tier >= self.getGermlineDnaSampleIdTier():
                record['germlineDnaSampleId'] = self.getGermlineDnaSampleId()
            if tier >= self.getTumorDnaSampleIdTier():
                record['tumorDnaSampleId'] = self.getTumorDnaSampleId()
            if tier >= self.getTumorRnaSampleIdTier():
                record['tumorRnaSampleId'] = self.getTumorRnaSampleId()
            if tier >= self.getGermlineSnvDiscussedTier():
                record['germlineSnvDiscussed'] = self.getGermlineSnvDiscussed()
            if tier >= self.getSomaticSnvDiscussedTier():
                record['somaticSnvDiscussed'] = self.getSomaticSnvDiscussed()
            if tier >= self.getCnvsDiscussedTier():
                record['cnvsDiscussed'] = self.getCnvsDiscussed()
            if tier >= self.getStructuralVariantDiscussedTier():
                record['structuralVariantDiscussed'] = self.getStructuralVariantDiscussed()
            if tier >= self.getClassificationOfVariantsTier():
                record['classificationOfVariants'] = self.getClassificationOfVariants()
            if tier >= self.getClinicalValidationProgressTier():
                record['clinicalValidationProgress'] = self.getClinicalValidationProgress()
            if tier >= self.getTypeOfValidationTier():
                record['typeOfValidation'] = self.getTypeOfValidation()
            if tier >= self.getAgentOrDrugClassTier():
                record['agentOrDrugClass'] = self.getAgentOrDrugClass()
            if tier >= self.getLevelOfEvidenceForExpressionTargetAgentMatchTier():
                record['levelOfEvidenceForExpressionTargetAgentMatch'] = self.getLevelOfEvidenceForExpressionTargetAgentMatch()
            if tier >= self.getDidTreatmentPlanChangeBasedOnProfilingResultTier():
                record['didTreatmentPlanChangeBasedOnProfilingResult'] = self.getDidTreatmentPlanChangeBasedOnProfilingResult()
            if tier >= self.getHowTreatmentHasAlteredBasedOnProfilingTier():
                record['howTreatmentHasAlteredBasedOnProfiling'] = self.getHowTreatmentHasAlteredBasedOnProfiling()
            if tier >= self.getReasonTreatmentPlanDidNotChangeBasedOnProfilingTier():
                record['reasonTreatmentPlanDidNotChangeBasedOnProfiling'] = self.getReasonTreatmentPlanDidNotChangeBasedOnProfiling()
            if tier >= self.getDetailsOfTreatmentPlanImpactTier():
                record['detailsOfTreatmentPlanImpact'] = self.getDetailsOfTreatmentPlanImpact()
            if tier >= self.getPatientOrFamilyInformedOfGermlineVariantTier():
                record['patientOrFamilyInformedOfGermlineVariant'] = self.getPatientOrFamilyInformedOfGermlineVariant()
            if tier >= self.getPatientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfilingTier():
                record['patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling'] = self.getPatientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling()
            if tier >= self.getSummaryReportTier():
                record['summaryReport'] = self.getSummaryReport()
        except TypeError:
            pass

        Tumourboard = protocol.Tumourboard(**record)
        self.serializeMetadataAttributes(Tumourboard)
        
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
        self._patientIdTier = TumourboardRecord.patientIdTier
        self._dateOfMolecularTumorBoard = TumourboardRecord.dateOfMolecularTumorBoard
        self._dateOfMolecularTumorBoardTier = TumourboardRecord.dateOfMolecularTumorBoardTier
        self._typeOfSampleAnalyzed = TumourboardRecord.typeOfSampleAnalyzed
        self._typeOfSampleAnalyzedTier = TumourboardRecord.typeOfSampleAnalyzedTier
        self._typeOfTumourSampleAnalyzed = TumourboardRecord.typeOfTumourSampleAnalyzed
        self._typeOfTumourSampleAnalyzedTier = TumourboardRecord.typeOfTumourSampleAnalyzedTier
        self._analysesDiscussed = TumourboardRecord.analysesDiscussed
        self._analysesDiscussedTier = TumourboardRecord.analysesDiscussedTier
        self._somaticSampleType = TumourboardRecord.somaticSampleType
        self._somaticSampleTypeTier = TumourboardRecord.somaticSampleTypeTier
        self._normalExpressionComparator = TumourboardRecord.normalExpressionComparator
        self._normalExpressionComparatorTier = TumourboardRecord.normalExpressionComparatorTier
        self._diseaseExpressionComparator = TumourboardRecord.diseaseExpressionComparator
        self._diseaseExpressionComparatorTier = TumourboardRecord.diseaseExpressionComparatorTier
        self._hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer = TumourboardRecord.hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer
        self._hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancerTier = TumourboardRecord.hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancerTier
        self._actionableTargetFound = TumourboardRecord.actionableTargetFound
        self._actionableTargetFoundTier = TumourboardRecord.actionableTargetFoundTier
        self._molecularTumorBoardRecommendation = TumourboardRecord.molecularTumorBoardRecommendation
        self._molecularTumorBoardRecommendationTier = TumourboardRecord.molecularTumorBoardRecommendationTier
        self._germlineDnaSampleId = TumourboardRecord.germlineDnaSampleId
        self._germlineDnaSampleIdTier = TumourboardRecord.germlineDnaSampleIdTier
        self._tumorDnaSampleId = TumourboardRecord.tumorDnaSampleId
        self._tumorDnaSampleIdTier = TumourboardRecord.tumorDnaSampleIdTier
        self._tumorRnaSampleId = TumourboardRecord.tumorRnaSampleId
        self._tumorRnaSampleIdTier = TumourboardRecord.tumorRnaSampleIdTier
        self._germlineSnvDiscussed = TumourboardRecord.germlineSnvDiscussed
        self._germlineSnvDiscussedTier = TumourboardRecord.germlineSnvDiscussedTier
        self._somaticSnvDiscussed = TumourboardRecord.somaticSnvDiscussed
        self._somaticSnvDiscussedTier = TumourboardRecord.somaticSnvDiscussedTier
        self._cnvsDiscussed = TumourboardRecord.cnvsDiscussed
        self._cnvsDiscussedTier = TumourboardRecord.cnvsDiscussedTier
        self._structuralVariantDiscussed = TumourboardRecord.structuralVariantDiscussed
        self._structuralVariantDiscussedTier = TumourboardRecord.structuralVariantDiscussedTier
        self._classificationOfVariants = TumourboardRecord.classificationOfVariants
        self._classificationOfVariantsTier = TumourboardRecord.classificationOfVariantsTier
        self._clinicalValidationProgress = TumourboardRecord.clinicalValidationProgress
        self._clinicalValidationProgressTier = TumourboardRecord.clinicalValidationProgressTier
        self._typeOfValidation = TumourboardRecord.typeOfValidation
        self._typeOfValidationTier = TumourboardRecord.typeOfValidationTier
        self._agentOrDrugClass = TumourboardRecord.agentOrDrugClass
        self._agentOrDrugClassTier = TumourboardRecord.agentOrDrugClassTier
        self._levelOfEvidenceForExpressionTargetAgentMatch = TumourboardRecord.levelOfEvidenceForExpressionTargetAgentMatch
        self._levelOfEvidenceForExpressionTargetAgentMatchTier = TumourboardRecord.levelOfEvidenceForExpressionTargetAgentMatchTier
        self._didTreatmentPlanChangeBasedOnProfilingResult = TumourboardRecord.didTreatmentPlanChangeBasedOnProfilingResult
        self._didTreatmentPlanChangeBasedOnProfilingResultTier = TumourboardRecord.didTreatmentPlanChangeBasedOnProfilingResultTier
        self._howTreatmentHasAlteredBasedOnProfiling = TumourboardRecord.howTreatmentHasAlteredBasedOnProfiling
        self._howTreatmentHasAlteredBasedOnProfilingTier = TumourboardRecord.howTreatmentHasAlteredBasedOnProfilingTier
        self._reasonTreatmentPlanDidNotChangeBasedOnProfiling = TumourboardRecord.reasonTreatmentPlanDidNotChangeBasedOnProfiling
        self._reasonTreatmentPlanDidNotChangeBasedOnProfilingTier = TumourboardRecord.reasonTreatmentPlanDidNotChangeBasedOnProfilingTier
        self._detailsOfTreatmentPlanImpact = TumourboardRecord.detailsOfTreatmentPlanImpact
        self._detailsOfTreatmentPlanImpactTier = TumourboardRecord.detailsOfTreatmentPlanImpactTier
        self._patientOrFamilyInformedOfGermlineVariant = TumourboardRecord.patientOrFamilyInformedOfGermlineVariant
        self._patientOrFamilyInformedOfGermlineVariantTier = TumourboardRecord.patientOrFamilyInformedOfGermlineVariantTier
        self._patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling = TumourboardRecord.patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling
        self._patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfilingTier = TumourboardRecord.patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfilingTier
        self._summaryReport = TumourboardRecord.summaryReport
        self._summaryReportTier = TumourboardRecord.summaryReportTier

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
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._dateOfMolecularTumorBoard = parsed.dateOfMolecularTumorBoard
        self._dateOfMolecularTumorBoardTier = parsed.dateOfMolecularTumorBoardTier
        self._typeOfSampleAnalyzed = parsed.typeOfSampleAnalyzed
        self._typeOfSampleAnalyzedTier = parsed.typeOfSampleAnalyzedTier
        self._typeOfTumourSampleAnalyzed = parsed.typeOfTumourSampleAnalyzed
        self._typeOfTumourSampleAnalyzedTier = parsed.typeOfTumourSampleAnalyzedTier
        self._analysesDiscussed = parsed.analysesDiscussed
        self._analysesDiscussedTier = parsed.analysesDiscussedTier
        self._somaticSampleType = parsed.somaticSampleType
        self._somaticSampleTypeTier = parsed.somaticSampleTypeTier
        self._normalExpressionComparator = parsed.normalExpressionComparator
        self._normalExpressionComparatorTier = parsed.normalExpressionComparatorTier
        self._diseaseExpressionComparator = parsed.diseaseExpressionComparator
        self._diseaseExpressionComparatorTier = parsed.diseaseExpressionComparatorTier
        self._hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer = parsed.hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer
        self._hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancerTier = parsed.hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancerTier
        self._actionableTargetFound = parsed.actionableTargetFound
        self._actionableTargetFoundTier = parsed.actionableTargetFoundTier
        self._molecularTumorBoardRecommendation = parsed.molecularTumorBoardRecommendation
        self._molecularTumorBoardRecommendationTier = parsed.molecularTumorBoardRecommendationTier
        self._germlineDnaSampleId = parsed.germlineDnaSampleId
        self._germlineDnaSampleIdTier = parsed.germlineDnaSampleIdTier
        self._tumorDnaSampleId = parsed.tumorDnaSampleId
        self._tumorDnaSampleIdTier = parsed.tumorDnaSampleIdTier
        self._tumorRnaSampleId = parsed.tumorRnaSampleId
        self._tumorRnaSampleIdTier = parsed.tumorRnaSampleIdTier
        self._germlineSnvDiscussed = parsed.germlineSnvDiscussed
        self._germlineSnvDiscussedTier = parsed.germlineSnvDiscussedTier
        self._somaticSnvDiscussed = parsed.somaticSnvDiscussed
        self._somaticSnvDiscussedTier = parsed.somaticSnvDiscussedTier
        self._cnvsDiscussed = parsed.cnvsDiscussed
        self._cnvsDiscussedTier = parsed.cnvsDiscussedTier
        self._structuralVariantDiscussed = parsed.structuralVariantDiscussed
        self._structuralVariantDiscussedTier = parsed.structuralVariantDiscussedTier
        self._classificationOfVariants = parsed.classificationOfVariants
        self._classificationOfVariantsTier = parsed.classificationOfVariantsTier
        self._clinicalValidationProgress = parsed.clinicalValidationProgress
        self._clinicalValidationProgressTier = parsed.clinicalValidationProgressTier
        self._typeOfValidation = parsed.typeOfValidation
        self._typeOfValidationTier = parsed.typeOfValidationTier
        self._agentOrDrugClass = parsed.agentOrDrugClass
        self._agentOrDrugClassTier = parsed.agentOrDrugClassTier
        self._levelOfEvidenceForExpressionTargetAgentMatch = parsed.levelOfEvidenceForExpressionTargetAgentMatch
        self._levelOfEvidenceForExpressionTargetAgentMatchTier = parsed.levelOfEvidenceForExpressionTargetAgentMatchTier
        self._didTreatmentPlanChangeBasedOnProfilingResult = parsed.didTreatmentPlanChangeBasedOnProfilingResult
        self._didTreatmentPlanChangeBasedOnProfilingResultTier = parsed.didTreatmentPlanChangeBasedOnProfilingResultTier
        self._howTreatmentHasAlteredBasedOnProfiling = parsed.howTreatmentHasAlteredBasedOnProfiling
        self._howTreatmentHasAlteredBasedOnProfilingTier = parsed.howTreatmentHasAlteredBasedOnProfilingTier
        self._reasonTreatmentPlanDidNotChangeBasedOnProfiling = parsed.reasonTreatmentPlanDidNotChangeBasedOnProfiling
        self._reasonTreatmentPlanDidNotChangeBasedOnProfilingTier = parsed.reasonTreatmentPlanDidNotChangeBasedOnProfilingTier
        self._detailsOfTreatmentPlanImpact = parsed.detailsOfTreatmentPlanImpact
        self._detailsOfTreatmentPlanImpactTier = parsed.detailsOfTreatmentPlanImpactTier
        self._patientOrFamilyInformedOfGermlineVariant = parsed.patientOrFamilyInformedOfGermlineVariant
        self._patientOrFamilyInformedOfGermlineVariantTier = parsed.patientOrFamilyInformedOfGermlineVariantTier
        self._patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling = parsed.patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling
        self._patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfilingTier = parsed.patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfilingTier
        self._summaryReport = parsed.summaryReport
        self._summaryReportTier = parsed.summaryReportTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getDateOfMolecularTumorBoard(self):
        return self._dateOfMolecularTumorBoard

    def getDateOfMolecularTumorBoardTier(self):
        return self._dateOfMolecularTumorBoardTier

    def getTypeOfSampleAnalyzed(self):
        return self._typeOfSampleAnalyzed

    def getTypeOfSampleAnalyzedTier(self):
        return self._typeOfSampleAnalyzedTier

    def getTypeOfTumourSampleAnalyzed(self):
        return self._typeOfTumourSampleAnalyzed

    def getTypeOfTumourSampleAnalyzedTier(self):
        return self._typeOfTumourSampleAnalyzedTier

    def getAnalysesDiscussed(self):
        return self._analysesDiscussed

    def getAnalysesDiscussedTier(self):
        return self._analysesDiscussedTier

    def getSomaticSampleType(self):
        return self._somaticSampleType

    def getSomaticSampleTypeTier(self):
        return self._somaticSampleTypeTier

    def getNormalExpressionComparator(self):
        return self._normalExpressionComparator

    def getNormalExpressionComparatorTier(self):
        return self._normalExpressionComparatorTier

    def getDiseaseExpressionComparator(self):
        return self._diseaseExpressionComparator

    def getDiseaseExpressionComparatorTier(self):
        return self._diseaseExpressionComparatorTier

    def getHasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer(self):
        return self._hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer

    def getHasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancerTier(self):
        return self._hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancerTier

    def getActionableTargetFound(self):
        return self._actionableTargetFound

    def getActionableTargetFoundTier(self):
        return self._actionableTargetFoundTier

    def getMolecularTumorBoardRecommendation(self):
        return self._molecularTumorBoardRecommendation

    def getMolecularTumorBoardRecommendationTier(self):
        return self._molecularTumorBoardRecommendationTier

    def getGermlineDnaSampleId(self):
        return self._germlineDnaSampleId

    def getGermlineDnaSampleIdTier(self):
        return self._germlineDnaSampleIdTier

    def getTumorDnaSampleId(self):
        return self._tumorDnaSampleId

    def getTumorDnaSampleIdTier(self):
        return self._tumorDnaSampleIdTier

    def getTumorRnaSampleId(self):
        return self._tumorRnaSampleId

    def getTumorRnaSampleIdTier(self):
        return self._tumorRnaSampleIdTier

    def getGermlineSnvDiscussed(self):
        return self._germlineSnvDiscussed

    def getGermlineSnvDiscussedTier(self):
        return self._germlineSnvDiscussedTier

    def getSomaticSnvDiscussed(self):
        return self._somaticSnvDiscussed

    def getSomaticSnvDiscussedTier(self):
        return self._somaticSnvDiscussedTier

    def getCnvsDiscussed(self):
        return self._cnvsDiscussed

    def getCnvsDiscussedTier(self):
        return self._cnvsDiscussedTier

    def getStructuralVariantDiscussed(self):
        return self._structuralVariantDiscussed

    def getStructuralVariantDiscussedTier(self):
        return self._structuralVariantDiscussedTier

    def getClassificationOfVariants(self):
        return self._classificationOfVariants

    def getClassificationOfVariantsTier(self):
        return self._classificationOfVariantsTier

    def getClinicalValidationProgress(self):
        return self._clinicalValidationProgress

    def getClinicalValidationProgressTier(self):
        return self._clinicalValidationProgressTier

    def getTypeOfValidation(self):
        return self._typeOfValidation

    def getTypeOfValidationTier(self):
        return self._typeOfValidationTier

    def getAgentOrDrugClass(self):
        return self._agentOrDrugClass

    def getAgentOrDrugClassTier(self):
        return self._agentOrDrugClassTier

    def getLevelOfEvidenceForExpressionTargetAgentMatch(self):
        return self._levelOfEvidenceForExpressionTargetAgentMatch

    def getLevelOfEvidenceForExpressionTargetAgentMatchTier(self):
        return self._levelOfEvidenceForExpressionTargetAgentMatchTier

    def getDidTreatmentPlanChangeBasedOnProfilingResult(self):
        return self._didTreatmentPlanChangeBasedOnProfilingResult

    def getDidTreatmentPlanChangeBasedOnProfilingResultTier(self):
        return self._didTreatmentPlanChangeBasedOnProfilingResultTier

    def getHowTreatmentHasAlteredBasedOnProfiling(self):
        return self._howTreatmentHasAlteredBasedOnProfiling

    def getHowTreatmentHasAlteredBasedOnProfilingTier(self):
        return self._howTreatmentHasAlteredBasedOnProfilingTier

    def getReasonTreatmentPlanDidNotChangeBasedOnProfiling(self):
        return self._reasonTreatmentPlanDidNotChangeBasedOnProfiling

    def getReasonTreatmentPlanDidNotChangeBasedOnProfilingTier(self):
        return self._reasonTreatmentPlanDidNotChangeBasedOnProfilingTier

    def getDetailsOfTreatmentPlanImpact(self):
        return self._detailsOfTreatmentPlanImpact

    def getDetailsOfTreatmentPlanImpactTier(self):
        return self._detailsOfTreatmentPlanImpactTier

    def getPatientOrFamilyInformedOfGermlineVariant(self):
        return self._patientOrFamilyInformedOfGermlineVariant

    def getPatientOrFamilyInformedOfGermlineVariantTier(self):
        return self._patientOrFamilyInformedOfGermlineVariantTier

    def getPatientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling(self):
        return self._patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling

    def getPatientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfilingTier(self):
        return self._patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfilingTier

    def getSummaryReport(self):
        return self._summaryReport

    def getSummaryReportTier(self):
        return self._summaryReportTier


class Chemotherapy(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.ChemotherapyCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Chemotherapy, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._patientIdTier = None
        self._courseNumber = None
        self._courseNumberTier = None
        self._startDate = None
        self._startDateTier = None
        self._stopDate = None
        self._stopDateTier = None
        self._systematicTherapyAgentName = None
        self._systematicTherapyAgentNameTier = None
        self._route = None
        self._routeTier = None
        self._dose = None
        self._doseTier = None
        self._doseFrequency = None
        self._doseFrequencyTier = None
        self._doseUnit = None
        self._doseUnitTier = None
        self._daysPerCycle = None
        self._daysPerCycleTier = None
        self._numberOfCycle = None
        self._numberOfCycleTier = None
        self._treatmentIntent = None
        self._treatmentIntentTier = None
        self._treatingCentreName = None
        self._treatingCentreNameTier = None
        self._type = None
        self._typeTier = None
        self._protocolCode = None
        self._protocolCodeTier = None
        self._recordingDate = None
        self._recordingDateTier = None
        self._treatmentPlanId = None
        self._treatmentPlanIdTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "courseNumber": self.getCourseNumber,
            "startDate": self.getStartDate,
            "stopDate": self.getStopDate,
            "systematicTherapyAgentName": self.getSystematicTherapyAgentName,
            "route": self.getRoute,
            "dose": self.getDose,
            "doseFrequency": self.getDoseFrequency,
            "doseUnit": self.getDoseUnit,
            "daysPerCycle": self.getDaysPerCycle,
            "numberOfCycle": self.getNumberOfCycle,
            "treatmentIntent": self.getTreatmentIntent,
            "treatingCentreName": self.getTreatingCentreName,
            "type": self.getType,
            "protocolCode": self.getProtocolCode,
            "recordingDate": self.getRecordingDate,
            "treatmentPlanId": self.getTreatmentPlanId,
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        try:
            # Unique fields
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getCourseNumberTier():
                record['courseNumber'] = self.getCourseNumber()
            if tier >= self.getStartDateTier():
                record['startDate'] = self.getStartDate()
            if tier >= self.getStopDateTier():
                record['stopDate'] = self.getStopDate()
            if tier >= self.getSystematicTherapyAgentNameTier():
                record['systematicTherapyAgentName'] = self.getSystematicTherapyAgentName()
            if tier >= self.getRouteTier():
                record['route'] = self.getRoute()
            if tier >= self.getDoseTier():
                record['dose'] = self.getDose()
            if tier >= self.getDoseFrequencyTier():
                record['doseFrequency'] = self.getDoseFrequency()
            if tier >= self.getDoseUnitTier():
                record['doseUnit'] = self.getDoseUnit()
            if tier >= self.getDaysPerCycleTier():
                record['daysPerCycle'] = self.getDaysPerCycle()
            if tier >= self.getNumberOfCycleTier():
                record['numberOfCycle'] = self.getNumberOfCycle()
            if tier >= self.getTreatmentIntentTier():
                record['treatmentIntent'] = self.getTreatmentIntent()
            if tier >= self.getTreatingCentreNameTier():
                record['treatingCentreName'] = self.getTreatingCentreName()
            if tier >= self.getTypeTier():
                record['type'] = self.getType()
            if tier >= self.getProtocolCodeTier():
                record['protocolCode'] = self.getProtocolCode()
            if tier >= self.getRecordingDateTier():
                record['recordingDate'] = self.getRecordingDate()
            if tier >= self.getTreatmentPlanIdTier():
                record['treatmentPlanId'] = self.getTreatmentPlanId()
        except TypeError:
            pass

        Chemotherapy = protocol.Chemotherapy(**record)
        self.serializeMetadataAttributes(Chemotherapy, tier)

        return Chemotherapy

    def populateFromRow(self, ChemotherapyRecord):
        """
        """
        self._created = ChemotherapyRecord.created
        self._updated = ChemotherapyRecord.updated
        self._name = ChemotherapyRecord.name
        self._description = ChemotherapyRecord.description
        self.setAttributesJson(ChemotherapyRecord.attributes)

        # Unique fields
        self._patientId = ChemotherapyRecord.patientId
        self._patientIdTier = ChemotherapyRecord.patientIdTier
        self._courseNumber = ChemotherapyRecord.courseNumber
        self._courseNumberTier = ChemotherapyRecord.courseNumberTier
        self._startDate = ChemotherapyRecord.startDate
        self._startDateTier = ChemotherapyRecord.startDateTier
        self._stopDate = ChemotherapyRecord.stopDate
        self._stopDateTier = ChemotherapyRecord.stopDateTier
        self._systematicTherapyAgentName = ChemotherapyRecord.systematicTherapyAgentName
        self._systematicTherapyAgentNameTier = ChemotherapyRecord.systematicTherapyAgentNameTier
        self._route = ChemotherapyRecord.route
        self._routeTier = ChemotherapyRecord.routeTier
        self._dose = ChemotherapyRecord.dose
        self._doseTier = ChemotherapyRecord.doseTier
        self._doseFrequency = ChemotherapyRecord.doseFrequency
        self._doseFrequencyTier = ChemotherapyRecord.doseFrequencyTier
        self._doseUnit = ChemotherapyRecord.doseUnit
        self._doseUnitTier = ChemotherapyRecord.doseUnitTier
        self._daysPerCycle = ChemotherapyRecord.daysPerCycle
        self._daysPerCycleTier = ChemotherapyRecord.daysPerCycleTier
        self._numberOfCycle = ChemotherapyRecord.numberOfCycle
        self._numberOfCycleTier = ChemotherapyRecord.numberOfCycleTier
        self._treatmentIntent = ChemotherapyRecord.treatmentIntent
        self._treatmentIntentTier = ChemotherapyRecord.treatmentIntentTier
        self._treatingCentreName = ChemotherapyRecord.treatingCentreName
        self._treatingCentreNameTier = ChemotherapyRecord.treatingCentreNameTier
        self._type = ChemotherapyRecord.type
        self._typeTier = ChemotherapyRecord.typeTier
        self._protocolCode = ChemotherapyRecord.protocolCode
        self._protocolCodeTier = ChemotherapyRecord.protocolCodeTier
        self._recordingDate = ChemotherapyRecord.recordingDate
        self._recordingDateTier = ChemotherapyRecord.recordingDateTier
        self._treatmentPlanId = ChemotherapyRecord.treatmentPlanId
        self._treatmentPlanIdTier = ChemotherapyRecord.treatmentPlanIdTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Chemotherapy)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._courseNumber = parsed.courseNumber
        self._courseNumberTier = parsed.courseNumberTier
        self._startDate = parsed.startDate
        self._startDateTier = parsed.startDateTier
        self._stopDate = parsed.stopDate
        self._stopDateTier = parsed.stopDateTier
        self._systematicTherapyAgentName = parsed.systematicTherapyAgentName
        self._systematicTherapyAgentNameTier = parsed.systematicTherapyAgentNameTier
        self._route = parsed.route
        self._routeTier = parsed.routeTier
        self._dose = parsed.dose
        self._doseTier = parsed.doseTier
        self._doseFrequency = parsed.doseFrequency
        self._doseFrequencyTier = parsed.doseFrequencyTier
        self._doseUnit = parsed.doseUnit
        self._doseUnitTier = parsed.doseUnitTier
        self._daysPerCycle = parsed.daysPerCycle
        self._daysPerCycleTier = parsed.daysPerCycleTier
        self._numberOfCycle = parsed.numberOfCycle
        self._numberOfCycleTier = parsed.numberOfCycleTier
        self._treatmentIntent = parsed.treatmentIntent
        self._treatmentIntentTier = parsed.treatmentIntentTier
        self._treatingCentreName = parsed.treatingCentreName
        self._treatingCentreNameTier = parsed.treatingCentreNameTier
        self._type = parsed.type
        self._typeTier = parsed.typeTier
        self._protocolCode = parsed.protocolCode
        self._protocolCodeTier = parsed.protocolCodeTier
        self._recordingDate = parsed.recordingDate
        self._recordingDateTier = parsed.recordingDateTier
        self._treatmentPlanId = parsed.treatmentPlanId
        self._treatmentPlanIdTier = parsed.treatmentPlanIdTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getCourseNumber(self):
        return self._courseNumber

    def getCourseNumberTier(self):
        return self._courseNumberTier

    def getStartDate(self):
        return self._startDate

    def getStartDateTier(self):
        return self._startDateTier

    def getStopDate(self):
        return self._stopDate

    def getStopDateTier(self):
        return self._stopDateTier

    def getSystematicTherapyAgentName(self):
        return self._systematicTherapyAgentName

    def getSystematicTherapyAgentNameTier(self):
        return self._systematicTherapyAgentNameTier

    def getRoute(self):
        return self._route

    def getRouteTier(self):
        return self._routeTier

    def getDose(self):
        return self._dose

    def getDoseTier(self):
        return self._doseTier

    def getDoseFrequency(self):
        return self._doseFrequency

    def getDoseFrequencyTier(self):
        return self._doseFrequencyTier

    def getDoseUnit(self):
        return self._doseUnit

    def getDoseUnitTier(self):
        return self._doseUnitTier

    def getDaysPerCycle(self):
        return self._daysPerCycle

    def getDaysPerCycleTier(self):
        return self._daysPerCycleTier

    def getNumberOfCycle(self):
        return self._numberOfCycle

    def getNumberOfCycleTier(self):
        return self._numberOfCycleTier

    def getTreatmentIntent(self):
        return self._treatmentIntent

    def getTreatmentIntentTier(self):
        return self._treatmentIntentTier

    def getTreatingCentreName(self):
        return self._treatingCentreName

    def getTreatingCentreNameTier(self):
        return self._treatingCentreNameTier

    def getType(self):
        return self._type

    def getTypeTier(self):
        return self._typeTier

    def getProtocolCode(self):
        return self._protocolCode

    def getProtocolCodeTier(self):
        return self._protocolCodeTier

    def getRecordingDate(self):
        return self._recordingDate

    def getRecordingDateTier(self):
        return self._recordingDateTier

    def getTreatmentPlanId(self):
        return self._treatmentPlanId

    def getTreatmentPlanIdTier(self):
        return self._treatmentPlanIdTier


class Radiotherapy(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.RadiotherapyCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Radiotherapy, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._patientIdTier = None
        self._courseNumber = None
        self._courseNumberTier = None
        self._startDate = None
        self._startDateTier = None
        self._stopDate = None
        self._stopDateTier = None
        self._therapeuticModality = None
        self._therapeuticModalityTier = None
        self._baseline = None
        self._baselineTier = None
        self._testResult = None
        self._testResultTier = None
        self._testResultStd = None
        self._testResultStdTier = None
        self._treatingCentreName = None
        self._treatingCentreNameTier = None
        self._startIntervalRad = None
        self._startIntervalRadTier = None
        self._startIntervalRadRaw = None
        self._startIntervalRadRawTier = None
        self._recordingDate = None
        self._recordingDateTier = None
        self._adjacentFields = None
        self._adjacentFieldsTier = None
        self._adjacentFractions = None
        self._adjacentFractionsTier = None
        self._complete = None
        self._completeTier = None
        self._brachytherapyDose = None
        self._brachytherapyDoseTier = None
        self._radiotherapyDose = None
        self._radiotherapyDoseTier = None
        self._siteNumber = None
        self._siteNumberTier = None
        self._technique = None
        self._techniqueTier = None
        self._treatedRegion = None
        self._treatedRegionTier = None
        self._treatmentPlanId = None
        self._treatmentPlanIdTier = None
        self._radiationType = None
        self._radiationTypeTier = None
        self._radiationSite = None
        self._radiationSiteTier = None
        self._totalDose = None
        self._totalDoseTier = None
        self._boostSite = None
        self._boostSiteTier = None
        self._boostDose = None
        self._boostDoseTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "courseNumber": self.getCourseNumber,
            "startDate": self.getStartDate,
            "stopDate": self.getStopDate,
            "therapeuticModality": self.getTherapeuticModality,
            "baseline": self.getBaseline,
            "testResult": self.getTestResult,
            "testResultStd": self.getTestResultStd,
            "treatingCentreName": self.getTreatingCentreName,
            "startIntervalRad": self.getStartIntervalRad,
            "startIntervalRadRaw": self.getStartIntervalRadRaw,
            "recordingDate": self.getRecordingDate,
            "adjacentFields": self.getAdjacentFields,
            "adjacentFractions": self.getAdjacentFractions,
            "complete": self.getComplete,
            "brachytherapyDose": self.getBrachytherapyDose,
            "siteNumber": self.getSiteNumber,
            "technique": self.getTechnique,
            "treatedRegion": self.getTreatedRegion,
            "treatmentPlanId": self.getTreatmentPlanId,
            "radiationType": self.getRadiationType,
            "radiationSite": self.getRadiationSite,
            "totalDose": self.getTotalDose,
            "boostSite": self.getBoostSite,
            "boostDose": self.getBoostDose
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getCourseNumberTier():
                record['courseNumber'] = self.getCourseNumber()
            if tier >= self.getStartDateTier():
                record['startDate'] = self.getStartDate()
            if tier >= self.getStopDateTier():
                record['stopDate'] = self.getStopDate()
            if tier >= self.getTherapeuticModalityTier():
                record['therapeuticModality'] = self.getTherapeuticModality()
            if tier >= self.getBaselineTier():
                record['baseline'] = self.getBaseline()
            if tier >= self.getTestResultTier():
                record['testResult'] = self.getTestResult()
            if tier >= self.getTestResultStdTier():
                record['testResultStd'] = self.getTestResultStd()
            if tier >= self.getTreatingCentreNameTier():
                record['treatingCentreName'] = self.getTreatingCentreName()
            if tier >= self.getStartIntervalRadTier():
                record['startIntervalRad'] = self.getStartIntervalRad()
            if tier >= self.getStartIntervalRadRawTier():
                record['startIntervalRadRaw'] = self.getStartIntervalRadRaw()
            if tier >= self.getRecordingDateTier():
                record['recordingDate'] = self.getRecordingDate()
            if tier >= self.getAdjacentFieldsTier():
                record['adjacentFields'] = self.getAdjacentFields()
            if tier >= self.getAdjacentFractionsTier():
                record['adjacentFractions'] = self.getAdjacentFractions()
            if tier >= self.getCompleteTier():
                record['complete'] = self.getComplete()
            if tier >= self.getBrachytherapyDoseTier():
                record['brachytherapyDose'] = self.getBrachytherapyDose()
            if tier >= self.getRadiotherapyDoseTier():
                record['radiotherapyDose'] = self.getRadiotherapyDose()
            if tier >= self.getSiteNumberTier():
                record['siteNumber'] = self.getSiteNumber()
            if tier >= self.getTechniqueTier():
                record['technique'] = self.getTechnique()
            if tier >= self.getTreatedRegionTier():
                record['treatedRegion'] = self.getTreatedRegion()
            if tier >= self.getTreatmentPlanIdTier():
                record['treatmentPlanId'] = self.getTreatmentPlanId()
            if tier >= self.getRadiationTypeTier():
                record['radiationType'] = self.getRadiationType()
            if tier >= self.getRadiationSiteTier():
                record['radiationSite'] = self.getRadiationSite()
            if tier >= self.getTotalDoseTier():
                record['totalDose'] = self.getTotalDose()
            if tier >= self.getBoostSiteTier():
                record['boostSite'] = self.getBoostSite()
            if tier >= self.getBoostDoseTier():
                record['boostDose'] = self.getBoostDose()
        except TypeError:
            pass

        Radiotherapy = protocol.Radiotherapy(**record)
        self.serializeMetadataAttributes(Radiotherapy)

        return Radiotherapy

    def populateFromRow(self, RadiotherapyRecord):
        """
        """
        self._created = RadiotherapyRecord.created
        self._updated = RadiotherapyRecord.updated
        self._name = RadiotherapyRecord.name
        self._description = RadiotherapyRecord.description
        self.setAttributesJson(RadiotherapyRecord.attributes)

        # Unique fields
        self._patientId = RadiotherapyRecord.patientId
        self._patientIdTier = RadiotherapyRecord.patientIdTier
        self._courseNumber = RadiotherapyRecord.courseNumber
        self._courseNumberTier = RadiotherapyRecord.courseNumberTier
        self._startDate = RadiotherapyRecord.startDate
        self._startDateTier = RadiotherapyRecord.startDateTier
        self._stopDate = RadiotherapyRecord.stopDate
        self._stopDateTier = RadiotherapyRecord.stopDateTier
        self._therapeuticModality = RadiotherapyRecord.therapeuticModality
        self._therapeuticModalityTier = RadiotherapyRecord.therapeuticModalityTier
        self._baseline = RadiotherapyRecord.baseline
        self._baselineTier = RadiotherapyRecord.baselineTier
        self._testResult = RadiotherapyRecord.testResult
        self._testResultTier = RadiotherapyRecord.testResultTier
        self._testResultStd = RadiotherapyRecord.testResultStd
        self._testResultStdTier = RadiotherapyRecord.testResultStdTier
        self._treatingCentreName = RadiotherapyRecord.treatingCentreName
        self._treatingCentreNameTier = RadiotherapyRecord.treatingCentreNameTier
        self._startIntervalRad = RadiotherapyRecord.startIntervalRad
        self._startIntervalRadTier = RadiotherapyRecord.startIntervalRadTier
        self._startIntervalRadRaw = RadiotherapyRecord.startIntervalRadRaw
        self._startIntervalRadRawTier = RadiotherapyRecord.startIntervalRadRawTier
        self._recordingDate = RadiotherapyRecord.recordingDate
        self._recordingDateTier = RadiotherapyRecord.recordingDateTier
        self._adjacentFields = RadiotherapyRecord.adjacentFields
        self._adjacentFieldsTier = RadiotherapyRecord.adjacentFieldsTier
        self._adjacentFractions = RadiotherapyRecord.adjacentFractions
        self._adjacentFractionsTier = RadiotherapyRecord.adjacentFractionsTier
        self._complete = RadiotherapyRecord.complete
        self._completeTier = RadiotherapyRecord.completeTier
        self._brachytherapyDose = RadiotherapyRecord.brachytherapyDose
        self._brachytherapyDoseTier = RadiotherapyRecord.brachytherapyDoseTier
        self._radiotherapyDose = RadiotherapyRecord.radiotherapyDose
        self._radiotherapyDoseTier = RadiotherapyRecord.radiotherapyDoseTier
        self._siteNumber = RadiotherapyRecord.siteNumber
        self._siteNumberTier = RadiotherapyRecord.siteNumberTier
        self._technique = RadiotherapyRecord.technique
        self._techniqueTier = RadiotherapyRecord.techniqueTier
        self._treatedRegion = RadiotherapyRecord.treatedRegion
        self._treatedRegionTier = RadiotherapyRecord.treatedRegionTier
        self._treatmentPlanId = RadiotherapyRecord.treatmentPlanId
        self._treatmentPlanIdTier = RadiotherapyRecord.treatmentPlanIdTier
        self._radiationType = RadiotherapyRecord.radiationType
        self._radiationTypeTier = RadiotherapyRecord.radiationTypeTier
        self._radiationSite = RadiotherapyRecord.radiationSite
        self._radiationSiteTier = RadiotherapyRecord.radiationSiteTier
        self._totalDose = RadiotherapyRecord.totalDose
        self._totalDoseTier = RadiotherapyRecord.totalDoseTier
        self._boostSite = RadiotherapyRecord.boostSite
        self._boostSiteTier = RadiotherapyRecord.boostSiteTier
        self._boostDose = RadiotherapyRecord.boostDose
        self._boostDoseTier = RadiotherapyRecord.boostDoseTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Radiotherapy)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._courseNumber = parsed.courseNumber
        self._courseNumberTier = parsed.courseNumberTier
        self._startDate = parsed.startDate
        self._startDateTier = parsed.startDateTier
        self._stopDate = parsed.stopDate
        self._stopDateTier = parsed.stopDateTier
        self._therapeuticModality = parsed.therapeuticModality
        self._therapeuticModalityTier = parsed.therapeuticModalityTier
        self._baseline = parsed.baseline
        self._baselineTier = parsed.baselineTier
        self._testResult = parsed.testResult
        self._testResultTier = parsed.testResultTier
        self._testResultStd = parsed.testResultStd
        self._testResultStdTier = parsed.testResultStdTier
        self._treatingCentreName = parsed.treatingCentreName
        self._treatingCentreNameTier = parsed.treatingCentreNameTier
        self._startIntervalRad = parsed.startIntervalRad
        self._startIntervalRadTier = parsed.startIntervalRadTier
        self._startIntervalRadRaw = parsed.startIntervalRadRaw
        self._startIntervalRadRawTier = parsed.startIntervalRadRawTier
        self._recordingDate = parsed.recordingDate
        self._recordingDateTier = parsed.recordingDateTier
        self._adjacentFields = parsed.adjacentFields
        self._adjacentFieldsTier = parsed.adjacentFieldsTier
        self._adjacentFractions = parsed.adjacentFractions
        self._adjacentFractionsTier = parsed.adjacentFractionsTier
        self._complete = parsed.complete
        self._completeTier = parsed.completeTier
        self._brachytherapyDose = parsed.brachytherapyDose
        self._brachytherapyDoseTier = parsed.brachytherapyDoseTier
        self._radiotherapyDose = parsed.radiotherapyDose
        self._radiotherapyDoseTier = parsed.radiotherapyDoseTier
        self._siteNumber = parsed.siteNumber
        self._siteNumberTier = parsed.siteNumberTier
        self._technique = parsed.technique
        self._techniqueTier = parsed.techniqueTier
        self._treatedRegion = parsed.treatedRegion
        self._treatedRegionTier = parsed.treatedRegionTier
        self._treatmentPlanId = parsed.treatmentPlanId
        self._treatmentPlanIdTier = parsed.treatmentPlanIdTier
        self._radiationType = parsed.radiationType
        self._radiationTypeTier = parsed.radiationTypeTier
        self._radiationSite = parsed.radiationSite
        self._radiationSiteTier = parsed.radiationSiteTier
        self._totalDose = parsed.totalDose
        self._totalDoseTier = parsed.totalDoseTier
        self._boostSite = parsed.boostSite
        self._boostSiteTier = parsed.boostSiteTier
        self._boostDose = parsed.boostDose
        self._boostDoseTier = parsed.boostDoseTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getCourseNumber(self):
        return self._courseNumber

    def getCourseNumberTier(self):
        return self._courseNumberTier

    def getStartDate(self):
        return self._startDate

    def getStartDateTier(self):
        return self._startDateTier

    def getStopDate(self):
        return self._stopDate

    def getStopDateTier(self):
        return self._stopDateTier

    def getTherapeuticModality(self):
        return self._therapeuticModality

    def getTherapeuticModalityTier(self):
        return self._therapeuticModalityTier

    def getBaseline(self):
        return self._baseline

    def getBaselineTier(self):
        return self._baselineTier

    def getTestResult(self):
        return self._testResult

    def getTestResultTier(self):
        return self._testResultTier

    def getTestResultStd(self):
        return self._testResultStd

    def getTestResultStdTier(self):
        return self._testResultStdTier

    def getTreatingCentreName(self):
        return self._treatingCentreName

    def getTreatingCentreNameTier(self):
        return self._treatingCentreNameTier

    def getStartIntervalRad(self):
        return self._startIntervalRad

    def getStartIntervalRadTier(self):
        return self._startIntervalRadTier

    def getStartIntervalRadRaw(self):
        return self._startIntervalRadRaw

    def getStartIntervalRadRawTier(self):
        return self._startIntervalRadRawTier

    def getRecordingDate(self):
        return self._recordingDate

    def getRecordingDateTier(self):
        return self._recordingDateTier

    def getAdjacentFields(self):
        return self._adjacentFields

    def getAdjacentFieldsTier(self):
        return self._adjacentFieldsTier

    def getAdjacentFractions(self):
        return self._adjacentFractions

    def getAdjacentFractionsTier(self):
        return self._adjacentFractionsTier

    def getComplete(self):
        return self._complete

    def getCompleteTier(self):
        return self._completeTier

    def getBrachytherapyDose(self):
        return self._brachytherapyDose

    def getBrachytherapyDoseTier(self):
        return self._brachytherapyDoseTier

    def getRadiotherapyDose(self):
        return self._radiotherapyDose

    def getRadiotherapyDoseTier(self):
        return self._radiotherapyDoseTier

    def getSiteNumber(self):
        return self._siteNumber

    def getSiteNumberTier(self):
        return self._siteNumberTier

    def getTechnique(self):
        return self._technique

    def getTechniqueTier(self):
        return self._techniqueTier

    def getTreatedRegion(self):
        return self._treatedRegion

    def getTreatedRegionTier(self):
        return self._treatedRegionTier

    def getTreatmentPlanId(self):
        return self._treatmentPlanId

    def getTreatmentPlanIdTier(self):
        return self._treatmentPlanIdTier

    def getRadiationType(self):
        return self._radiationType

    def getRadiationTypeTier(self):
        return self._radiationTypeTier

    def getRadiationSite(self):
        return self._radiationSite

    def getRadiationSiteTier(self):
        return self._radiationSiteTier

    def getTotalDose(self):
        return self._totalDose

    def getTotalDoseTier(self):
        return self._totalDoseTier

    def getBoostSite(self):
        return self._boostSite

    def getBoostSiteTier(self):
        return self._boostSiteTier

    def getBoostDose(self):
        return self._boostDose

    def getBoostDoseTier(self):
        return self._boostDoseTier


class Surgery(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.SurgeryCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Surgery, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._patientIdTier = None
        self._startDate = None
        self._startDateTier = None
        self._stopDate = None
        self._stopDateTier = None
        self._sampleId = None
        self._sampleIdTier = None
        self._collectionTimePoint = None
        self._collectionTimePointTier = None
        self._diagnosisDate = None
        self._diagnosisDateTier = None
        self._site = None
        self._siteTier = None
        self._type = None
        self._typeTier = None
        self._recordingDate = None
        self._recordingDateTier = None
        self._treatmentPlanId = None
        self._treatmentPlanIdTier = None
        self._courseNumber = None
        self._courseNumberTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "startDate": self.getStartDate,
            "stopDate": self.getStopDate,
            "sampleId": self.getSampleId,
            "collectionTimePoint": self.getCollectionTimePoint,
            "diagnosisDate": self.getDiagnosisDate,
            "site": self.getSite,
            "type": self.getType,
            "recordingDate": self.getRecordingDate,
            "treatmentPlanId": self.getTreatmentPlanId,
            "courseNumber": self.getCourseNumber
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getStartDateTier():
                record['startDate'] = self.getStartDate()
            if tier >= self.getStopDateTier():
                record['stopDate'] = self.getStopDate()
            if tier >= self.getSampleIdTier():
                record['sampleId'] = self.getSampleId()
            if tier >= self.getCollectionTimePointTier():
                record['collectionTimePoint'] = self.getCollectionTimePoint()
            if tier >= self.getDiagnosisDateTier():
                record['diagnosisDate'] = self.getDiagnosisDate()
            if tier >= self.getSiteTier():
                record['site'] = self.getSite()
            if tier >= self.getTypeTier():
                record['type'] = self.getType()
            if tier >= self.getRecordingDateTier():
                record['recordingDate'] = self.getRecordingDate()
            if tier >= self.getTreatmentPlanIdTier():
                record['treatmentPlanId'] = self.getTreatmentPlanId()
            if tier >= self.getCourseNumberTier():
                record['courseNumber'] = self.getCourseNumber()
        except TypeError:
            pass

        Surgery = protocol.Surgery(**record)
        self.serializeMetadataAttributes(Surgery)

        return Surgery

    def populateFromRow(self, SurgeryRecord):
        """
        """
        self._created = SurgeryRecord.created
        self._updated = SurgeryRecord.updated
        self._name = SurgeryRecord.name
        self._description = SurgeryRecord.description
        self.setAttributesJson(SurgeryRecord.attributes)

        # Unique fields
        self._patientId = SurgeryRecord.patientId
        self._patientIdTier = SurgeryRecord.patientIdTier
        self._startDate = SurgeryRecord.startDate
        self._startDateTier = SurgeryRecord.startDateTier
        self._stopDate = SurgeryRecord.stopDate
        self._stopDateTier = SurgeryRecord.stopDateTier
        self._sampleId = SurgeryRecord.sampleId
        self._sampleIdTier = SurgeryRecord.sampleIdTier
        self._collectionTimePoint = SurgeryRecord.collectionTimePoint
        self._collectionTimePointTier = SurgeryRecord.collectionTimePointTier
        self._diagnosisDate = SurgeryRecord.diagnosisDate
        self._diagnosisDateTier = SurgeryRecord.diagnosisDateTier
        self._site = SurgeryRecord.site
        self._siteTier = SurgeryRecord.siteTier
        self._type = SurgeryRecord.type
        self._typeTier = SurgeryRecord.typeTier
        self._recordingDate = SurgeryRecord.recordingDate
        self._recordingDateTier = SurgeryRecord.recordingDateTier
        self._treatmentPlanId = SurgeryRecord.treatmentPlanId
        self._treatmentPlanIdTier = SurgeryRecord.treatmentPlanIdTier
        self._courseNumber = SurgeryRecord.courseNumber
        self._courseNumberTier = SurgeryRecord.courseNumberTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Surgery)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._startDate = parsed.startDate
        self._startDateTier = parsed.startDateTier
        self._stopDate = parsed.stopDate
        self._stopDateTier = parsed.stopDateTier
        self._sampleId = parsed.sampleId
        self._sampleIdTier = parsed.sampleIdTier
        self._collectionTimePoint = parsed.collectionTimePoint
        self._collectionTimePointTier = parsed.collectionTimePointTier
        self._diagnosisDate = parsed.diagnosisDate
        self._diagnosisDateTier = parsed.diagnosisDateTier
        self._site = parsed.site
        self._siteTier = parsed.siteTier
        self._type = parsed.type
        self._typeTier = parsed.typeTier
        self._recordingDate = parsed.recordingDate
        self._recordingDateTier = parsed.recordingDateTier
        self._treatmentPlanId = parsed.treatmentPlanId
        self._treatmentPlanIdTier = parsed.treatmentPlanIdTier
        self._courseNumber = parsed.courseNumber
        self._courseNumberTier = parsed.courseNumberTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getStartDate(self):
        return self._startDate

    def getStartDateTier(self):
        return self._startDateTier

    def getStopDate(self):
        return self._stopDate

    def getStopDateTier(self):
        return self._stopDateTier

    def getSampleId(self):
        return self._sampleId

    def getSampleIdTier(self):
        return self._sampleIdTier

    def getCollectionTimePoint(self):
        return self._collectionTimePoint

    def getCollectionTimePointTier(self):
        return self._collectionTimePointTier

    def getDiagnosisDate(self):
        return self._diagnosisDate

    def getDiagnosisDateTier(self):
        return self._diagnosisDateTier

    def getSite(self):
        return self._site

    def getSiteTier(self):
        return self._siteTier

    def getType(self):
        return self._type

    def getTypeTier(self):
        return self._typeTier

    def getRecordingDate(self):
        return self._recordingDate

    def getRecordingDateTier(self):
        return self._recordingDateTier

    def getTreatmentPlanId(self):
        return self._treatmentPlanId

    def getTreatmentPlanIdTier(self):
        return self._treatmentPlanIdTier

    def getCourseNumber(self):
        return self._courseNumber

    def getCourseNumberTier(self):
        return self._courseNumberTier


class Immunotherapy(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.ImmunotherapyCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Immunotherapy, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._patientIdTier = None
        self._startDate = None
        self._startDateTier = None
        self._immunotherapyType = None
        self._immunotherapyTypeTier = None
        self._immunotherapyTarget = None
        self._immunotherapyTargetTier = None
        self._immunotherapyDetail = None
        self._immunotherapyDetailTier = None
        self._treatmentPlanId = None
        self._treatmentPlanIdTier = None
        self._courseNumber = None
        self._courseNumberTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "startDate": self.getStartDate,
            "immunotherapyType": self.getImmunotherapyType,
            "immunotherapyTarget": self.getImmunotherapyTarget,
            "immunotherapyDetail": self.getImmunotherapyDetail,
            "treatmentPlanId": self.getTreatmentPlanId,
            "courseNumber": self.getCourseNumber
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getStartDateTier():
                record['startDate'] = self.getStartDate()
            if tier >= self.getImmunotherapyTypeTier():
                record['immunotherapyType'] = self.getImmunotherapyType()
            if tier >= self.getImmunotherapyTargetTier():
                record['immunotherapyTarget'] = self.getImmunotherapyTarget()
            if tier >= self.getImmunotherapyDetailTier():
                record['immunotherapyDetail'] = self.getImmunotherapyDetail()
            if tier >= self.getTreatmentPlanIdTier():
                record['treatmentPlanId'] = self.getTreatmentPlanId()
            if tier >= self.getCourseNumberTier():
                record['courseNumber'] = self.getCourseNumber()
        except TypeError:
            pass

        Immunotherapy = protocol.Immunotherapy(**record)
        self.serializeMetadataAttributes(Immunotherapy)

        return Immunotherapy

    def populateFromRow(self, ImmunotherapyRecord):
        """
        """
        self._created = ImmunotherapyRecord.created
        self._updated = ImmunotherapyRecord.updated
        self._name = ImmunotherapyRecord.name
        self._description = ImmunotherapyRecord.description
        self.setAttributesJson(ImmunotherapyRecord.attributes)

        # Unique fields
        self._patientId = ImmunotherapyRecord.patientId
        self._patientIdTier = ImmunotherapyRecord.patientIdTier
        self._startDate = ImmunotherapyRecord.startDate
        self._startDateTier = ImmunotherapyRecord.startDateTier
        self._immunotherapyType = ImmunotherapyRecord.immunotherapyType
        self._immunotherapyTypeTier = ImmunotherapyRecord.immunotherapyTypeTier
        self._immunotherapyTarget = ImmunotherapyRecord.immunotherapyTarget
        self._immunotherapyTargetTier = ImmunotherapyRecord.immunotherapyTargetTier
        self._immunotherapyDetail = ImmunotherapyRecord.immunotherapyDetail
        self._immunotherapyDetailTier = ImmunotherapyRecord.immunotherapyDetailTier
        self._treatmentPlanId = ImmunotherapyRecord.treatmentPlanId
        self._treatmentPlanIdTier = ImmunotherapyRecord.treatmentPlanIdTier
        self._courseNumber = ImmunotherapyRecord.courseNumber
        self._courseNumberTier = ImmunotherapyRecord.courseNumberTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Immunotherapy)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._startDate = parsed.startDate
        self._startDateTier = parsed.startDateTier
        self._immunotherapyType = parsed.immunotherapyType
        self._immunotherapyTypeTier = parsed.immunotherapyTypeTier
        self._immunotherapyTarget = parsed.immunotherapyTarget
        self._immunotherapyTargetTier = parsed.immunotherapyTargetTier
        self._immunotherapyDetail = parsed.immunotherapyDetail
        self._immunotherapyDetailTier = parsed.immunotherapyDetailTier
        self._treatmentPlanId = parsed.treatmentPlanId
        self._treatmentPlanIdTier = parsed.treatmentPlanIdTier
        self._courseNumber = parsed.courseNumber
        self._courseNumberTier = parsed.courseNumberTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getStartDate(self):
        return self._startDate

    def getStartDateTier(self):
        return self._startDateTier

    def getImmunotherapyType(self):
        return self._immunotherapyType

    def getImmunotherapyTypeTier(self):
        return self._immunotherapyTypeTier

    def getImmunotherapyTarget(self):
        return self._immunotherapyTarget

    def getImmunotherapyTargetTier(self):
        return self._immunotherapyTargetTier

    def getImmunotherapyDetail(self):
        return self._immunotherapyDetail

    def getImmunotherapyDetailTier(self):
        return self._immunotherapyDetailTier

    def getTreatmentPlanId(self):
        return self._treatmentPlanId

    def getTreatmentPlanIdTier(self):
        return self._treatmentPlanIdTier

    def getCourseNumber(self):
        return self._courseNumber

    def getCourseNumberTier(self):
        return self._courseNumberTier


class Celltransplant(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.CelltransplantCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Celltransplant, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._patientIdTier = None
        self._startDate = None
        self._startDateTier = None
        self._cellSource = None
        self._cellSourceTier = None
        self._donorType = None
        self._donorTypeTier = None
        self._treatmentPlanId = None
        self._treatmentPlanIdTier = None
        self._courseNumber = None
        self._courseNumberTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "startDate": self.getStartDate,
            "cellSource": self.getCellSource,
            "donorType": self.getDonorType,
            "treatmentPlanId": self.getTreatmentPlanId,
            "courseNumber": self.getCourseNumber
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getStartDateTier():
                record['startDate'] = self.getStartDate()
            if tier >= self.getCellSourceTier():
                record['cellSource'] = self.getCellSource()
            if tier >= self.getDonorTypeTier():
                record['donorType'] = self.getDonorType()
            if tier >= self.getTreatmentPlanIdTier():
                record['treatmentPlanId'] = self.getTreatmentPlanId()
            if tier >= self.getCourseNumberTier():
                record['courseNumber'] = self.getCourseNumber()
        except TypeError:
            pass

        Celltransplant = protocol.Celltransplant(**record)
        self.serializeMetadataAttributes(Celltransplant)

        return Celltransplant

    def populateFromRow(self, CelltransplantRecord):
        """
        """
        self._created = CelltransplantRecord.created
        self._updated = CelltransplantRecord.updated
        self._name = CelltransplantRecord.name
        self._description = CelltransplantRecord.description
        self.setAttributesJson(CelltransplantRecord.attributes)

        # Unique fields
        self._patientId = CelltransplantRecord.patientId
        self._patientIdTier = CelltransplantRecord.patientIdTier
        self._startDate = CelltransplantRecord.startDate
        self._startDateTier = CelltransplantRecord.startDateTier
        self._cellSource = CelltransplantRecord.cellSource
        self._cellSourceTier = CelltransplantRecord.cellSourceTier
        self._donorType = CelltransplantRecord.donorType
        self._donorTypeTier = CelltransplantRecord.donorTypeTier
        self._treatmentPlanId = CelltransplantRecord.treatmentPlanId
        self._treatmentPlanIdTier = CelltransplantRecord.treatmentPlanIdTier
        self._courseNumber = CelltransplantRecord.courseNumber
        self._courseNumberTier = CelltransplantRecord.courseNumberTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Celltransplant)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._startDate = parsed.startDate
        self._startDateTier = parsed.startDateTier
        self._cellSource = parsed.cellSource
        self._cellSourceTier = parsed.cellSourceTier
        self._donorType = parsed.donorType
        self._donorTypeTier = parsed.donorTypeTier
        self._treatmentPlanId = parsed.treatmentPlanId
        self._treatmentPlanIdTier = parsed.treatmentPlanIdTier
        self._courseNumber = parsed.courseNumber
        self._courseNumberTier = parsed.courseNumberTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getStartDate(self):
        return self._startDate

    def getStartDateTier(self):
        return self._startDateTier

    def getCellSource(self):
        return self._cellSource

    def getCellSourceTier(self):
        return self._cellSourceTier

    def getDonorType(self):
        return self._donorType

    def getDonorTypeTier(self):
        return self._donorTypeTier

    def getTreatmentPlanId(self):
        return self._treatmentPlanId

    def getTreatmentPlanIdTier(self):
        return self._treatmentPlanIdTier

    def getCourseNumber(self):
        return self._courseNumber

    def getCourseNumberTier(self):
        return self._courseNumberTier


class Slide(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.SlideCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Slide, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._patientIdTier = None
        self._sampleId = None
        self._sampleIdTier = None
        self._slideId = None
        self._slideIdTier = None
        self._slideOtherId = None
        self._slideOtherIdTier = None
        self._lymphocyteInfiltrationPercent = None
        self._lymphocyteInfiltrationPercentTier = None
        self._tumorNucleiPercent = None
        self._tumorNucleiPercentTier = None
        self._monocyteInfiltrationPercent = None
        self._monocyteInfiltrationPercentTier = None
        self._normalCellsPercent = None
        self._normalCellsPercentTier = None
        self._tumorCellsPercent = None
        self._tumorCellsPercentTier = None
        self._stromalCellsPercent = None
        self._stromalCellsPercentTier = None
        self._eosinophilInfiltrationPercent = None
        self._eosinophilInfiltrationPercentTier = None
        self._neutrophilInfiltrationPercent = None
        self._neutrophilInfiltrationPercentTier = None
        self._granulocyteInfiltrationPercent = None
        self._granulocyteInfiltrationPercentTier = None
        self._necrosisPercent = None
        self._necrosisPercentTier = None
        self._inflammatoryInfiltrationPercent = None
        self._inflammatoryInfiltrationPercentTier = None
        self._proliferatingCellsNumber = None
        self._proliferatingCellsNumberTier = None
        self._sectionLocation = None
        self._sectionLocationTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "sampleId": self.getSampleId,
            "slideId": self.getSlideId,
            "slideOtherId": self.getSlideOtherId,
            "lymphocyteInfiltrationPercent": self.getLymphocyteInfiltrationPercent,
            "tumorNucleiPercent": self.getTumorNucleiPercent,
            "monocyteInfiltrationPercent": self.getMonocyteInfiltrationPercent,
            "normalCellsPercent": self.getNormalCellsPercent,
            "tumorCellsPercent": self.getTumorCellsPercent,
            "stromalCellsPercent": self.getStromalCellsPercent,
            "eosinophilInfiltrationPercent": self.getEosinophilInfiltrationPercent,
            "neutrophilInfiltrationPercent": self.getNeutrophilInfiltrationPercent,
            "granulocyteInfiltrationPercent": self.getGranulocyteInfiltrationPercent,
            "necrosisPercent": self.getNecrosisPercent,
            "inflammatoryInfiltrationPercent": self.getInflammatoryInfiltrationPercent,
            "proliferatingCellsNumber": self.getProliferatingCellsNumber,
            "sectionLocation": self.getSectionLocation,
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getSampleIdTier():
                record['sampleId'] = self.getSampleId()
            if tier >= self.getSlideIdTier():
                record['slideId'] = self.getSlideId()
            if tier >= self.getSlideOtherIdTier():
                record['slideOtherId'] = self.getSlideOtherId()
            if tier >= self.getLymphocyteInfiltrationPercentTier():
                record['lymphocyteInfiltrationPercent'] = self.getLymphocyteInfiltrationPercent()
            if tier >= self.getTumorNucleiPercentTier():
                record['tumorNucleiPercent'] = self.getTumorNucleiPercent()
            if tier >= self.getMonocyteInfiltrationPercentTier():
                record['monocyteInfiltrationPercent'] = self.getMonocyteInfiltrationPercent()
            if tier >= self.getNormalCellsPercentTier():
                record['normalCellsPercent'] = self.getNormalCellsPercent()
            if tier >= self.getTumorCellsPercentTier():
                record['tumorCellsPercent'] = self.getTumorCellsPercent()
            if tier >= self.getStromalCellsPercentTier():
                record['stromalCellsPercent'] = self.getStromalCellsPercent()
            if tier >= self.getEosinophilInfiltrationPercentTier():
                record['eosinophilInfiltrationPercent'] = self.getEosinophilInfiltrationPercent()
            if tier >= self.getNeutrophilInfiltrationPercentTier():
                record['neutrophilInfiltrationPercent'] = self.getNeutrophilInfiltrationPercent()
            if tier >= self.getGranulocyteInfiltrationPercentTier():
                record['granulocyteInfiltrationPercent'] = self.getGranulocyteInfiltrationPercent()
            if tier >= self.getNecrosisPercentTier():
                record['necrosisPercent'] = self.getNecrosisPercent()
            if tier >= self.getInflammatoryInfiltrationPercentTier():
                record['inflammatoryInfiltrationPercent'] = self.getInflammatoryInfiltrationPercent()
            if tier >= self.getProliferatingCellsNumberTier():
                record['proliferatingCellsNumber'] = self.getProliferatingCellsNumber()
            if tier >= self.getSectionLocationTier():
                record['sectionLocation'] = self.getSectionLocation()
        except TypeError:
            pass

        Slide = protocol.Slide(**record)
        self.serializeMetadataAttributes(Slide)

        return Slide

    def populateFromRow(self, SlideRecord):
        """
        """
        self._created = SlideRecord.created
        self._updated = SlideRecord.updated
        self._name = SlideRecord.name
        self._description = SlideRecord.description
        self.setAttributesJson(SlideRecord.attributes)

        # Unique fields
        self._patientId = SlideRecord.patientId
        self._patientIdTier = SlideRecord.patientIdTier
        self._sampleId = SlideRecord.sampleId
        self._sampleIdTier = SlideRecord.sampleIdTier
        self._slideId = SlideRecord.slideId
        self._slideIdTier = SlideRecord.slideIdTier
        self._slideOtherId = SlideRecord.slideOtherId
        self._slideOtherIdTier = SlideRecord.slideOtherIdTier
        self._lymphocyteInfiltrationPercent = SlideRecord.lymphocyteInfiltrationPercent
        self._lymphocyteInfiltrationPercentTier = SlideRecord.lymphocyteInfiltrationPercentTier
        self._tumorNucleiPercent = SlideRecord.tumorNucleiPercent
        self._tumorNucleiPercentTier = SlideRecord.tumorNucleiPercentTier
        self._monocyteInfiltrationPercent = SlideRecord.monocyteInfiltrationPercent
        self._monocyteInfiltrationPercentTier = SlideRecord.monocyteInfiltrationPercentTier
        self._normalCellsPercent = SlideRecord.normalCellsPercent
        self._normalCellsPercentTier = SlideRecord.normalCellsPercentTier
        self._tumorCellsPercent = SlideRecord.tumorCellsPercent
        self._tumorCellsPercentTier = SlideRecord.tumorCellsPercentTier
        self._stromalCellsPercent = SlideRecord.stromalCellsPercent
        self._stromalCellsPercentTier = SlideRecord.stromalCellsPercentTier
        self._eosinophilInfiltrationPercent = SlideRecord.eosinophilInfiltrationPercent
        self._eosinophilInfiltrationPercentTier = SlideRecord.eosinophilInfiltrationPercentTier
        self._neutrophilInfiltrationPercent = SlideRecord.neutrophilInfiltrationPercent
        self._neutrophilInfiltrationPercentTier = SlideRecord.neutrophilInfiltrationPercentTier
        self._granulocyteInfiltrationPercent = SlideRecord.granulocyteInfiltrationPercent
        self._granulocyteInfiltrationPercentTier = SlideRecord.granulocyteInfiltrationPercentTier
        self._necrosisPercent = SlideRecord.necrosisPercent
        self._necrosisPercentTier = SlideRecord.necrosisPercentTier
        self._inflammatoryInfiltrationPercent = SlideRecord.inflammatoryInfiltrationPercent
        self._inflammatoryInfiltrationPercentTier = SlideRecord.inflammatoryInfiltrationPercentTier
        self._proliferatingCellsNumber = SlideRecord.proliferatingCellsNumber
        self._proliferatingCellsNumberTier = SlideRecord.proliferatingCellsNumberTier
        self._sectionLocation = SlideRecord.sectionLocation
        self._sectionLocationTier = SlideRecord.sectionLocationTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Slide)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._sampleId = parsed.sampleId
        self._sampleIdTier = parsed.sampleIdTier
        self._slideId = parsed.slideId
        self._slideIdTier = parsed.slideIdTier
        self._slideOtherId = parsed.slideOtherId
        self._slideOtherIdTier = parsed.slideOtherIdTier
        self._lymphocyteInfiltrationPercent = parsed.lymphocyteInfiltrationPercent
        self._lymphocyteInfiltrationPercentTier = parsed.lymphocyteInfiltrationPercentTier
        self._tumorNucleiPercent = parsed.tumorNucleiPercent
        self._tumorNucleiPercentTier = parsed.tumorNucleiPercentTier
        self._monocyteInfiltrationPercent = parsed.monocyteInfiltrationPercent
        self._monocyteInfiltrationPercentTier = parsed.monocyteInfiltrationPercentTier
        self._normalCellsPercent = parsed.normalCellsPercent
        self._normalCellsPercentTier = parsed.normalCellsPercentTier
        self._tumorCellsPercent = parsed.tumorCellsPercent
        self._tumorCellsPercentTier = parsed.tumorCellsPercentTier
        self._stromalCellsPercent = parsed.stromalCellsPercent
        self._stromalCellsPercentTier = parsed.stromalCellsPercentTier
        self._eosinophilInfiltrationPercent = parsed.eosinophilInfiltrationPercent
        self._eosinophilInfiltrationPercentTier = parsed.eosinophilInfiltrationPercentTier
        self._neutrophilInfiltrationPercent = parsed.neutrophilInfiltrationPercent
        self._neutrophilInfiltrationPercentTier = parsed.neutrophilInfiltrationPercentTier
        self._granulocyteInfiltrationPercent = parsed.granulocyteInfiltrationPercent
        self._granulocyteInfiltrationPercentTier = parsed.granulocyteInfiltrationPercentTier
        self._necrosisPercent = parsed.necrosisPercent
        self._necrosisPercentTier = parsed.necrosisPercentTier
        self._inflammatoryInfiltrationPercent = parsed.inflammatoryInfiltrationPercent
        self._inflammatoryInfiltrationPercentTier = parsed.inflammatoryInfiltrationPercentTier
        self._proliferatingCellsNumber = parsed.proliferatingCellsNumber
        self._proliferatingCellsNumberTier = parsed.proliferatingCellsNumberTier
        self._sectionLocation = parsed.sectionLocation
        self._sectionLocationTier = parsed.sectionLocationTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getSampleId(self):
        return self._sampleId

    def getSampleIdTier(self):
        return self._sampleIdTier

    def getSlideId(self):
        return self._slideId

    def getSlideIdTier(self):
        return self._slideIdTier

    def getSlideOtherId(self):
        return self._slideOtherId

    def getSlideOtherIdTier(self):
        return self._slideOtherIdTier

    def getLymphocyteInfiltrationPercent(self):
        return self._lymphocyteInfiltrationPercent

    def getLymphocyteInfiltrationPercentTier(self):
        return self._lymphocyteInfiltrationPercentTier

    def getTumorNucleiPercent(self):
        return self._tumorNucleiPercent

    def getTumorNucleiPercentTier(self):
        return self._tumorNucleiPercentTier

    def getMonocyteInfiltrationPercent(self):
        return self._monocyteInfiltrationPercent

    def getMonocyteInfiltrationPercentTier(self):
        return self._monocyteInfiltrationPercentTier

    def getNormalCellsPercent(self):
        return self._normalCellsPercent

    def getNormalCellsPercentTier(self):
        return self._normalCellsPercentTier

    def getTumorCellsPercent(self):
        return self._tumorCellsPercent

    def getTumorCellsPercentTier(self):
        return self._tumorCellsPercentTier

    def getStromalCellsPercent(self):
        return self._stromalCellsPercent

    def getStromalCellsPercentTier(self):
        return self._stromalCellsPercentTier

    def getEosinophilInfiltrationPercent(self):
        return self._eosinophilInfiltrationPercent

    def getEosinophilInfiltrationPercentTier(self):
        return self._eosinophilInfiltrationPercentTier

    def getNeutrophilInfiltrationPercent(self):
        return self._neutrophilInfiltrationPercent

    def getNeutrophilInfiltrationPercentTier(self):
        return self._neutrophilInfiltrationPercentTier

    def getGranulocyteInfiltrationPercent(self):
        return self._granulocyteInfiltrationPercent

    def getGranulocyteInfiltrationPercentTier(self):
        return self._granulocyteInfiltrationPercentTier

    def getNecrosisPercent(self):
        return self._necrosisPercent

    def getNecrosisPercentTier(self):
        return self._necrosisPercentTier

    def getInflammatoryInfiltrationPercent(self):
        return self._inflammatoryInfiltrationPercent

    def getInflammatoryInfiltrationPercentTier(self):
        return self._inflammatoryInfiltrationPercentTier

    def getProliferatingCellsNumber(self):
        return self._proliferatingCellsNumber

    def getProliferatingCellsNumberTier(self):
        return self._proliferatingCellsNumberTier

    def getSectionLocation(self):
        return self._sectionLocation

    def getSectionLocationTier(self):
        return self._sectionLocationTier


class Study(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.StudyCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Study, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._patientIdTier = None
        self._startDate = None
        self._startDateTier = None
        self._endDate = None
        self._endDateTier = None
        self._status = None
        self._statusTier = None
        self._recordingDate = None
        self._recordingDateTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "startDate": self.getStartDate,
            "endDate": self.getEndDate,
            "status": self.getStatus,
            "recordingDate": self.getRecordingDate,
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getStartDateTier():
                record['startDate'] = self.getStartDate()
            if tier >= self.getEndDateTier():
                record['endDate'] = self.getEndDate()
            if tier >= self.getStatusTier():
                record['status'] = self.getStatus()
            if tier >= self.getRecordingDateTier():
                record['recordingDate'] = self.getRecordingDate()
        except TypeError:
            pass

        Study = protocol.Study(**record)
        self.serializeMetadataAttributes(Study)

        return Study

    def populateFromRow(self, StudyRecord):
        """
        """
        self._created = StudyRecord.created
        self._updated = StudyRecord.updated
        self._name = StudyRecord.name
        self._description = StudyRecord.description
        self.setAttributesJson(StudyRecord.attributes)

        # Unique fields
        self._patientId = StudyRecord.patientId
        self._patientIdTier = StudyRecord.patientIdTier
        self._startDate = StudyRecord.startDate
        self._startDateTier = StudyRecord.startDateTier
        self._endDate = StudyRecord.endDate
        self._endDateTier = StudyRecord.endDateTier
        self._status = StudyRecord.status
        self._statusTier = StudyRecord.statusTier
        self._recordingDate = StudyRecord.recordingDate
        self._recordingDateTier = StudyRecord.recordingDateTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Study)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._startDate = parsed.startDate
        self._startDateTier = parsed.startDateTier
        self._endDate = parsed.endDate
        self._endDateTier = parsed.endDateTier
        self._status = parsed.status
        self._statusTier = parsed.statusTier
        self._recordingDate = parsed.recordingDate
        self._recordingDateTier = parsed.recordingDateTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getStartDate(self):
        return self._startDate

    def getStartDateTier(self):
        return self._startDateTier

    def getEndDate(self):
        return self._endDate

    def getEndDateTier(self):
        return self._endDateTier

    def getStatus(self):
        return self._status

    def getStatusTier(self):
        return self._statusTier

    def getRecordingDate(self):
        return self._recordingDate

    def getRecordingDateTier(self):
        return self._recordingDateTier


class Labtest(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.LabtestCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Labtest, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._patientId = None
        self._patientIdTier = None
        self._startDate = None
        self._startDateTier = None
        self._collectionDate = None
        self._collectionDateTier = None
        self._endDate = None
        self._endDateTier = None
        self._eventType = None
        self._eventTypeTier = None
        self._testResults = None
        self._testResultsTier = None
        self._timePoint = None
        self._timePointTier = None
        self._recordingDate = None
        self._recordingDateTier = None

        self._objectAttr = {
            "patientId": self.getPatientId,
            "startDate": self.getStartDate,
            "endDate": self.getEndDate,
            "collectionDate": self.getCollectionDate,
            "eventType": self.getEventType,
            "testResults": self.getTestResults,
            "timePoint": self.getTimePoint,
            "recordingDate": self.getRecordingDate,
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getPatientIdTier():
                record['patientId'] = self.getPatientId()
            if tier >= self.getStartDateTier():
                record['startDate'] = self.getStartDate()
            if tier >= self.getEndDateTier():
                record['endDate'] = self.getEndDate()
            if tier >= self.getCollectionDateTier():
                record['collectionDate'] = self.getCollectionDate()
            if tier >= self.getEventTypeTier():
                record['eventType'] = self.getEventType()
            if tier >= self.getTestResultsTier():
                record['testResults'] = self.getTestResults()
            if tier >= self.getTimePointTier():
                record['timePoint'] = self.getTimePoint()
            if tier >= self.getRecordingDateTier():
                record['recordingDate'] = self.getRecordingDate()
        except TypeError:
            pass

        Labtest = protocol.Labtest(**record)
        self.serializeMetadataAttributes(Labtest)

        return Labtest

    def populateFromRow(self, LabtestRecord):
        """
        """
        self._created = LabtestRecord.created
        self._updated = LabtestRecord.updated
        self._name = LabtestRecord.name
        self._description = LabtestRecord.description
        self.setAttributesJson(LabtestRecord.attributes)

        # Unique fields
        self._patientId = LabtestRecord.patientId
        self._patientIdTier = LabtestRecord.patientIdTier
        self._startDate = LabtestRecord.startDate
        self._startDateTier = LabtestRecord.startDateTier
        self._collectionDate = LabtestRecord.collectionDate
        self._collectionDateTier = LabtestRecord.collectionDateTier
        self._endDate = LabtestRecord.endDate
        self._endDateTier = LabtestRecord.endDateTier
        self._eventType = LabtestRecord.eventType
        self._eventTypeTier = LabtestRecord.eventTypeTier
        self._testResults = LabtestRecord.testResults
        self._testResultsTier = LabtestRecord.testResultsTier
        self._timePoint = LabtestRecord.timePoint
        self._timePointTier = LabtestRecord.timePointTier
        self._recordingDate = LabtestRecord.recordingDate
        self._recordingDateTier = LabtestRecord.recordingDateTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Labtest)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._patientId = parsed.patientId
        self._patientIdTier = parsed.patientIdTier
        self._startDate = parsed.startDate
        self._startDateTier = parsed.startDateTier
        self._collectionDate = parsed.collectionDate
        self._collectionDateTier = parsed.collectionDateTier
        self._endDate = parsed.endDate
        self._endDateTier = parsed.endDateTier
        self._eventType = parsed.eventType
        self._eventTypeTier = parsed.eventTypeTier
        self._testResults = parsed.testResults
        self._testResultsTier = parsed.testResultsTier
        self._timePoint = parsed.timePoint
        self._timePointTier = parsed.timePointTier
        self._recordingDate = parsed.recordingDate
        self._recordingDateTier = parsed.recordingDateTier

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

    def getPatientIdTier(self):
        return self._patientIdTier

    def getStartDate(self):
        return self._startDate

    def getStartDateTier(self):
        return self._startDateTier

    def getCollectionDate(self):
        return self._collectionDate

    def getCollectionDateTier(self):
        return self._collectionDateTier

    def getEndDate(self):
        return self._endDate

    def getEndDateTier(self):
        return self._endDateTier

    def getEventType(self):
        return self._eventType

    def getEventTypeTier(self):
        return self._eventTypeTier

    def getTestResults(self):
        return self._testResults

    def getTestResultsTier(self):
        return self._testResultsTier

    def getTimePoint(self):
        return self._timePoint

    def getTimePointTier(self):
        return self._timePointTier

    def getRecordingDate(self):
        return self._recordingDate

    def getRecordingDateTier(self):
        return self._recordingDateTier
