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

    def toProtocolElement(self, tier=0):
        """
        """
        record = {      
            str('id') : str(self.getId()),
            str('dataset_id') : str(self._datasetId),
            str('created') : str(self.getCreated()),
            str('updated') : str(self.getUpdated()),
            str('name') : str(self.getName()),
            str('description') : str(self.getDescription()),
            }
            
        # Unique fields
        if tier >= self.getPatientIdTier():
           record[str('patientId')] = str(self.getPatientId())
        if tier >= self.getOtherIdsTier():
           record[str('otherIds')] = str(self.getOtherIds())
        if tier >= self.getDateOfBirthTier():
           record[str('dateOfBirth')] = str(self.getDateOfBirth())
        if tier >= self.getGenderTier():
           record[str('gender')] = str(self.getGender())
        if tier >= self.getEthnicityTier():
           record[str('ethnicity')] = str(self.getEthnicity())
        if tier >= self.getRaceTier():
           record[str('race')] = str(self.getRace())
        if tier >= self.getProvinceOfResidenceTier():
           record[str('provinceOfResidence')] = str(self.getProvinceOfResidence())
        if tier >= self.getDateOfDeathTier():
           record[str('dateOfDeath')] = str(self.getDateOfDeath())
        if tier >= self.getCauseOfDeathTier():
           record[str('causeOfDeath')] = str(self.getCauseOfDeath())
        if tier >= self.getAutopsyTissueForResearchTier():
           record[str('autopsyTissueForResearch')] = str(self.getAutopsyTissueForResearch())
        if tier >= self.getPriorMalignancyTier():
           record[str('priorMalignancy')] = str(self.getPriorMalignancy())
        if tier >= self.getDateOfPriorMalignancyTier():
           record[str('dateOfPriorMalignancy')] = str(self.getDateOfPriorMalignancy())
        if tier >= self.getFamilyHistoryAndRiskFactorsTier():
           record[str('familyHistoryAndRiskFactors')] = str(self.getFamilyHistoryAndRiskFactors())
        if tier >= self.getFamilyHistoryOfPredispositionSyndromeTier():
           record[str('familyHistoryOfPredispositionSyndrome')] = str(self.getFamilyHistoryOfPredispositionSyndrome())
        if tier >= self.getDetailsOfPredispositionSyndromeTier():
           record[str('detailsOfPredispositionSyndrome')] = str(self.getDetailsOfPredispositionSyndrome())
        if tier >= self.getGeneticCancerSyndromeTier():
           record[str('geneticCancerSyndrome')] = str(self.getGeneticCancerSyndrome())
        if tier >= self.getOtherGeneticConditionOrSignificantComorbidityTier():
           record[str('otherGeneticConditionOrSignificantComorbidity')] = str(self.getOtherGeneticConditionOrSignificantComorbidity())
        if tier >= self.getOccupationalOrEnvironmentalExposureTier():
           record[str('occupationalOrEnvironmentalExposure')] = str(self.getOccupationalOrEnvironmentalExposure())

        Patient = protocol.Patient(**record)
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
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
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

    def toProtocolElement(self, tier=0):
        """
        """
        record = {      
            str('id') : str(self.getId()),
            str('dataset_id') : str(self._datasetId),
            str('created') : str(self.getCreated()),
            str('updated') : str(self.getUpdated()),
            str('name') : str(self.getName()),
            str('description') : str(self.getDescription()),
            }
            
        # Unique fields
        if tier >= self.getPatientIdTier():
           record[str('patientId')] = str(self.getPatientId())
        if tier >= self.getEnrollmentInstitutionTier():
           record[str('enrollmentInstitution')] = str(self.getEnrollmentInstitution())
        if tier >= self.getEnrollmentApprovalDateTier():
           record[str('enrollmentApprovalDate')] = str(self.getEnrollmentApprovalDate())
        if tier >= self.getCrossEnrollmentTier():
           record[str('crossEnrollment')] = str(self.getCrossEnrollment())
        if tier >= self.getOtherPersonalizedMedicineStudyNameTier():
           record[str('otherPersonalizedMedicineStudyName')] = str(self.getOtherPersonalizedMedicineStudyName())
        if tier >= self.getOtherPersonalizedMedicineStudyIdTier():
           record[str('otherPersonalizedMedicineStudyId')] = str(self.getOtherPersonalizedMedicineStudyId())
        if tier >= self.getAgeAtEnrollmentTier():
           record[str('ageAtEnrollment')] = str(self.getAgeAtEnrollment())
        if tier >= self.getEligibilityCategoryTier():
           record[str('eligibilityCategory')] = str(self.getEligibilityCategory())
        if tier >= self.getStatusAtEnrollmentTier():
           record[str('statusAtEnrollment')] = str(self.getStatusAtEnrollment())
        if tier >= self.getPrimaryOncologistNameTier():
           record[str('primaryOncologistName')] = str(self.getPrimaryOncologistName())
        if tier >= self.getPrimaryOncologistContactTier():
           record[str('primaryOncologistContact')] = str(self.getPrimaryOncologistContact())
        if tier >= self.getReferringPhysicianNameTier():
           record[str('referringPhysicianName')] = str(self.getReferringPhysicianName())
        if tier >= self.getReferringPhysicianContactTier():
           record[str('referringPhysicianContact')] = str(self.getReferringPhysicianContact())
        if tier >= self.getSummaryOfIdRequestTier():
           record[str('summaryOfIdRequest')] = str(self.getSummaryOfIdRequest())
        if tier >= self.getTreatingCentreNameTier():
           record[str('treatingCentreName')] = str(self.getTreatingCentreName())
        if tier >= self.getTreatingCentreProvinceTier():
           record[str('treatingCentreProvince')] = str(self.getTreatingCentreProvince())
           
        Enrollment = protocol.Enrollment(**record)
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
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
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

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            str('id') : str(self.getId()),
            str('dataset_id') : str(self._datasetId),
            str('created') : str(self.getCreated()),
            str('updated') : str(self.getUpdated()),
            str('name') : str(self.getName()),
            str('description') : str(self.getDescription()),
            }

        # Unique fields
        if tier >= self.getPatientIdTier():
           record[str('patientId')] = str(self.getPatientId())
        if tier >= self.getConsentIdTier():
           record[str('consentId')] = str(self.getConsentId())
        if tier >= self.getConsentDateTier():
           record[str('consentDate')] = str(self.getConsentDate())
        if tier >= self.getConsentVersionTier():
           record[str('consentVersion')] = str(self.getConsentVersion())
        if tier >= self.getPatientConsentedToTier():
           record[str('patientConsentedTo')] = str(self.getPatientConsentedTo())
        if tier >= self.getReasonForRejectionTier():
           record[str('reasonForRejection')] = str(self.getReasonForRejection())
        if tier >= self.getWasAssentObtainedTier():
           record[str('wasAssentObtained')] = str(self.getWasAssentObtained())
        if tier >= self.getDateOfAssentTier():
           record[str('dateOfAssent')] = str(self.getDateOfAssent())
        if tier >= self.getAssentFormVersionTier():
           record[str('assentFormVersion')] = str(self.getAssentFormVersion())
        if tier >= self.getIfAssentNotObtainedWhyNotTier():
           record[str('ifAssentNotObtainedWhyNot')] = str(self.getIfAssentNotObtainedWhyNot())
        if tier >= self.getReconsentDateTier():
           record[str('reconsentDate')] = str(self.getReconsentDate())
        if tier >= self.getReconsentVersionTier():
           record[str('reconsentVersion')] = str(self.getReconsentVersion())
        if tier >= self.getConsentingCoordinatorNameTier():
           record[str('consentingCoordinatorName')] = str(self.getConsentingCoordinatorName())
        if tier >= self.getPreviouslyConsentedTier():
           record[str('previouslyConsented')] = str(self.getPreviouslyConsented())
        if tier >= self.getNameOfOtherBiobankTier():
           record[str('nameOfOtherBiobank')] = str(self.getNameOfOtherBiobank())
        if tier >= self.getHasConsentBeenWithdrawnTier():
           record[str('hasConsentBeenWithdrawn')] = str(self.getHasConsentBeenWithdrawn())
        if tier >= self.getDateOfConsentWithdrawalTier():
           record[str('dateOfConsentWithdrawal')] = str(self.getDateOfConsentWithdrawal())
        if tier >= self.getTypeOfConsentWithdrawalTier():
           record[str('typeOfConsentWithdrawal')] = str(self.getTypeOfConsentWithdrawal())
        if tier >= self.getReasonForConsentWithdrawalTier():
           record[str('reasonForConsentWithdrawal')] = str(self.getReasonForConsentWithdrawal())
        if tier >= self.getConsentFormCompleteTier():
           record[str('consentFormComplete')] = str(self.getConsentFormComplete())

        Consent = protocol.Consent(**record)
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
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
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

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            str('id') : str(self.getId()),
            str('dataset_id') : str(self._datasetId),
            str('created') : str(self.getCreated()),
            str('updated') : str(self.getUpdated()),
            str('name') : str(self.getName()),
            str('description') : str(self.getDescription()),
            }

        # Unique fields
        if tier >= self.getPatientIdTier():
           record[str('patientId')] = str(self.getPatientId())
        if tier >= self.getDiagnosisIdTier():
           record[str('diagnosisId')] = str(self.getDiagnosisId())
        if tier >= self.getDiagnosisDateTier():
           record[str('diagnosisDate')] = str(self.getDiagnosisDate())
        if tier >= self.getAgeAtDiagnosisTier():
           record[str('ageAtDiagnosis')] = str(self.getAgeAtDiagnosis())
        if tier >= self.getCancerTypeTier():
           record[str('cancerType')] = str(self.getCancerType())
        if tier >= self.getClassificationTier():
           record[str('classification')] = str(self.getClassification())
        if tier >= self.getCancerSiteTier():
           record[str('cancerSite')] = str(self.getCancerSite())
        if tier >= self.getHistologyTier():
           record[str('histology')] = str(self.getHistology())
        if tier >= self.getMethodOfDefinitiveDiagnosisTier():
           record[str('methodOfDefinitiveDiagnosis')] = str(self.getMethodOfDefinitiveDiagnosis())
        if tier >= self.getSampleTypeTier():
           record[str('sampleType')] = str(self.getSampleType())
        if tier >= self.getSampleSiteTier():
           record[str('sampleSite')] = str(self.getSampleSite())
        if tier >= self.getTumorGradeTier():
           record[str('tumorGrade')] = str(self.getTumorGrade())
        if tier >= self.getGradingSystemUsedTier():
           record[str('gradingSystemUsed')] = str(self.getGradingSystemUsed())
        if tier >= self.getSitesOfMetastasesTier():
           record[str('sitesOfMetastases')] = str(self.getSitesOfMetastases())
        if tier >= self.getStagingSystemTier():
           record[str('stagingSystem')] = str(self.getStagingSystem())
        if tier >= self.getVersionOrEditionOfTheStagingSystemTier():
           record[str('versionOrEditionOfTheStagingSystem')] = str(self.getVersionOrEditionOfTheStagingSystem())
        if tier >= self.getSpecificTumorStageAtDiagnosisTier():
           record[str('specificTumorStageAtDiagnosis')] = str(self.getSpecificTumorStageAtDiagnosis())
        if tier >= self.getPrognosticBiomarkersTier():
           record[str('prognosticBiomarkers')] = str(self.getPrognosticBiomarkers())
        if tier >= self.getBiomarkerQuantificationTier():
           record[str('biomarkerQuantification')] = str(self.getBiomarkerQuantification())
        if tier >= self.getAdditionalMolecularTestingTier():
           record[str('additionalMolecularTesting')] = str(self.getAdditionalMolecularTesting())
        if tier >= self.getAdditionalTestTypeTier():
           record[str('additionalTestType')] = str(self.getAdditionalTestType())
        if tier >= self.getLaboratoryNameTier():
           record[str('laboratoryName')] = str(self.getLaboratoryName())
        if tier >= self.getLaboratoryAddressTier():
           record[str('laboratoryAddress')] = str(self.getLaboratoryAddress())
        if tier >= self.getSiteOfMetastasesTier():
           record[str('siteOfMetastases')] = str(self.getSiteOfMetastases())
        if tier >= self.getStagingSystemVersionTier():
           record[str('stagingSystemVersion')] = str(self.getStagingSystemVersion())
        if tier >= self.getSpecificStageTier():
           record[str('specificStage')] = str(self.getSpecificStage())
        if tier >= self.getCancerSpecificBiomarkersTier():
           record[str('cancerSpecificBiomarkers')] = str(self.getCancerSpecificBiomarkers())
        if tier >= self.getAdditionalMolecularDiagnosticTestingPerformedTier():
           record[str('additionalMolecularDiagnosticTestingPerformed')] = str(self.getAdditionalMolecularDiagnosticTestingPerformed())
        if tier >= self.getAdditionalTestTier():
           record[str('additionalTest')] = str(self.getAdditionalTest())

        Diagnosis = protocol.Diagnosis(**record)
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
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
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

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            str('id') : str(self.getId()),
            str('dataset_id') : str(self._datasetId),
            str('created') : str(self.getCreated()),
            str('updated') : str(self.getUpdated()),
            str('name') : str(self.getName()),
            str('description') : str(self.getDescription()),
            }

        # Unique fields
        if tier >= self.getPatientIdTier():
           record[str('patientId')] = str(self.getPatientId())
        if tier >= self.getSampleIdTier():
           record[str('sampleId')] = str(self.getSampleId())
        if tier >= self.getDiagnosisIdTier():
           record[str('diagnosisId')] = str(self.getDiagnosisId())
        if tier >= self.getLocalBiobankIdTier():
           record[str('localBiobankId')] = str(self.getLocalBiobankId())
        if tier >= self.getCollectionDateTier():
           record[str('collectionDate')] = str(self.getCollectionDate())
        if tier >= self.getCollectionHospitalTier():
           record[str('collectionHospital')] = str(self.getCollectionHospital())
        if tier >= self.getSampleTypeTier():
           record[str('sampleType')] = str(self.getSampleType())
        if tier >= self.getTissueDiseaseStateTier():
           record[str('tissueDiseaseState')] = str(self.getTissueDiseaseState())
        if tier >= self.getAnatomicSiteTheSampleObtainedFromTier():
           record[str('anatomicSiteTheSampleObtainedFrom')] = str(self.getAnatomicSiteTheSampleObtainedFrom())
        if tier >= self.getCancerTypeTier():
           record[str('cancerType')] = str(self.getCancerType())
        if tier >= self.getCancerSubtypeTier():
           record[str('cancerSubtype')] = str(self.getCancerSubtype())
        if tier >= self.getPathologyReportIdTier():
           record[str('pathologyReportId')] = str(self.getPathologyReportId())
        if tier >= self.getMorphologicalCodeTier():
           record[str('morphologicalCode')] = str(self.getMorphologicalCode())
        if tier >= self.getTopologicalCodeTier():
           record[str('topologicalCode')] = str(self.getTopologicalCode())
        if tier >= self.getShippingDateTier():
           record[str('shippingDate')] = str(self.getShippingDate())
        if tier >= self.getReceivedDateTier():
           record[str('receivedDate')] = str(self.getReceivedDate())
        if tier >= self.getQualityControlPerformedTier():
           record[str('qualityControlPerformed')] = str(self.getQualityControlPerformed())
        if tier >= self.getEstimatedTumorContentTier():
           record[str('estimatedTumorContent')] = str(self.getEstimatedTumorContent())
        if tier >= self.getQuantityTier():
           record[str('quantity')] = str(self.getQuantity())
        if tier >= self.getUnitsTier():
           record[str('units')] = str(self.getUnits())
        if tier >= self.getAssociatedBiobankTier():
           record[str('associatedBiobank')] = str(self.getAssociatedBiobank())
        if tier >= self.getOtherBiobankTier():
           record[str('otherBiobank')] = str(self.getOtherBiobank())
        if tier >= self.getSopFollowedTier():
           record[str('sopFollowed')] = str(self.getSopFollowed())
        if tier >= self.getIfNotExplainAnyDeviationTier():
           record[str('ifNotExplainAnyDeviation')] = str(self.getIfNotExplainAnyDeviation())

        Sample = protocol.Sample(**record)
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
        self._systematicTherapyAgentName = None
        self._systematicTherapyAgentNameTier = None
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
        self._protocolNumberOrCode = None
        self._protocolNumberOrCodeTier = None
        self._surgeryDetails = None
        self._surgeryDetailsTier = None
        self._radiotherapyDetails = None
        self._radiotherapyDetailsTier = None
        self._chemotherapyDetails = None
        self._chemotherapyDetailsTier = None
        self._hematopoieticCellTransplant = None
        self._hematopoieticCellTransplantTier = None
        self._immunotherapyDetails = None
        self._immunotherapyDetailsTier = None
        self._responseToTreatment = None
        self._responseToTreatmentTier = None
        self._responseCriteriaUsed = None
        self._responseCriteriaUsedTier = None
        self._dateOfRecurrenceOrProgressionAfterThisTreatment = None
        self._dateOfRecurrenceOrProgressionAfterThisTreatmentTier = None
        self._unexpectedOrUnusualToxicityDuringTreatment = None
        self._unexpectedOrUnusualToxicityDuringTreatmentTier = None
        self._drugListOrAgent = None
        self._drugListOrAgentTier = None
        self._drugIdNumbers = None
        self._drugIdNumbersTier = None

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            str('id') : str(self.getId()),
            str('dataset_id') : str(self._datasetId),
            str('created') : str(self.getCreated()),
            str('updated') : str(self.getUpdated()),
            str('name') : str(self.getName()),
            str('description') : str(self.getDescription()),
            }

        # Unique fields
        if tier >= self.getPatientIdTier():
           record[str('patientId')] = str(self.getPatientId())
        if tier >= self.getCourseNumberTier():
           record[str('courseNumber')] = str(self.getCourseNumber())
        if tier >= self.getTherapeuticModalityTier():
           record[str('therapeuticModality')] = str(self.getTherapeuticModality())
        if tier >= self.getSystematicTherapyAgentNameTier():
           record[str('systematicTherapyAgentName')] = str(self.getSystematicTherapyAgentName())
        if tier >= self.getTreatmentPlanTypeTier():
           record[str('treatmentPlanType')] = str(self.getTreatmentPlanType())
        if tier >= self.getTreatmentIntentTier():
           record[str('treatmentIntent')] = str(self.getTreatmentIntent())
        if tier >= self.getStartDateTier():
           record[str('startDate')] = str(self.getStartDate())
        if tier >= self.getStopDateTier():
           record[str('stopDate')] = str(self.getStopDate())
        if tier >= self.getReasonForEndingTheTreatmentTier():
           record[str('reasonForEndingTheTreatment')] = str(self.getReasonForEndingTheTreatment())
        if tier >= self.getProtocolNumberOrCodeTier():
           record[str('protocolNumberOrCode')] = str(self.getProtocolNumberOrCode())
        if tier >= self.getSurgeryDetailsTier():
           record[str('surgeryDetails')] = str(self.getSurgeryDetails())
        if tier >= self.getRadiotherapyDetailsTier():
           record[str('radiotherapyDetails')] = str(self.getRadiotherapyDetails())
        if tier >= self.getChemotherapyDetailsTier():
           record[str('chemotherapyDetails')] = str(self.getChemotherapyDetails())
        if tier >= self.getHematopoieticCellTransplantTier():
           record[str('hematopoieticCellTransplant')] = str(self.getHematopoieticCellTransplant())
        if tier >= self.getImmunotherapyDetailsTier():
           record[str('immunotherapyDetails')] = str(self.getImmunotherapyDetails())
        if tier >= self.getResponseToTreatmentTier():
           record[str('responseToTreatment')] = str(self.getResponseToTreatment())
        if tier >= self.getResponseCriteriaUsedTier():
           record[str('responseCriteriaUsed')] = str(self.getResponseCriteriaUsed())
        if tier >= self.getDateOfRecurrenceOrProgressionAfterThisTreatmentTier():
           record[str('dateOfRecurrenceOrProgressionAfterThisTreatment')] = str(self.getDateOfRecurrenceOrProgressionAfterThisTreatment())
        if tier >= self.getUnexpectedOrUnusualToxicityDuringTreatmentTier():
           record[str('unexpectedOrUnusualToxicityDuringTreatment')] = str(self.getUnexpectedOrUnusualToxicityDuringTreatment())
        if tier >= self.getDrugListOrAgentTier():
           record[str('drugListOrAgent')] = str(self.getDrugListOrAgent())
        if tier >= self.getDrugIdNumbersTier():
           record[str('drugIdNumbers')] = str(self.getDrugIdNumbers())

        Treatment = protocol.Treatment(**record)
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
        self._patientIdTier = TreatmentRecord.patientIdTier
        self._courseNumber = TreatmentRecord.courseNumber
        self._courseNumberTier = TreatmentRecord.courseNumberTier
        self._therapeuticModality = TreatmentRecord.therapeuticModality
        self._therapeuticModalityTier = TreatmentRecord.therapeuticModalityTier
        self._systematicTherapyAgentName = TreatmentRecord.systematicTherapyAgentName
        self._systematicTherapyAgentNameTier = TreatmentRecord.systematicTherapyAgentNameTier
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
        self._protocolNumberOrCode = TreatmentRecord.protocolNumberOrCode
        self._protocolNumberOrCodeTier = TreatmentRecord.protocolNumberOrCodeTier
        self._surgeryDetails = TreatmentRecord.surgeryDetails
        self._surgeryDetailsTier = TreatmentRecord.surgeryDetailsTier
        self._radiotherapyDetails = TreatmentRecord.radiotherapyDetails
        self._radiotherapyDetailsTier = TreatmentRecord.radiotherapyDetailsTier
        self._chemotherapyDetails = TreatmentRecord.chemotherapyDetails
        self._chemotherapyDetailsTier = TreatmentRecord.chemotherapyDetailsTier
        self._hematopoieticCellTransplant = TreatmentRecord.hematopoieticCellTransplant
        self._hematopoieticCellTransplantTier = TreatmentRecord.hematopoieticCellTransplantTier
        self._immunotherapyDetails = TreatmentRecord.immunotherapyDetails
        self._immunotherapyDetailsTier = TreatmentRecord.immunotherapyDetailsTier
        self._responseToTreatment = TreatmentRecord.responseToTreatment
        self._responseToTreatmentTier = TreatmentRecord.responseToTreatmentTier
        self._responseCriteriaUsed = TreatmentRecord.responseCriteriaUsed
        self._responseCriteriaUsedTier = TreatmentRecord.responseCriteriaUsedTier
        self._dateOfRecurrenceOrProgressionAfterThisTreatment = TreatmentRecord.dateOfRecurrenceOrProgressionAfterThisTreatment
        self._dateOfRecurrenceOrProgressionAfterThisTreatmentTier = TreatmentRecord.dateOfRecurrenceOrProgressionAfterThisTreatmentTier
        self._unexpectedOrUnusualToxicityDuringTreatment = TreatmentRecord.unexpectedOrUnusualToxicityDuringTreatment
        self._unexpectedOrUnusualToxicityDuringTreatmentTier = TreatmentRecord.unexpectedOrUnusualToxicityDuringTreatmentTier
        self._drugListOrAgent = TreatmentRecord.drugListOrAgent
        self._drugListOrAgentTier = TreatmentRecord.drugListOrAgentTier
        self._drugIdNumbers = TreatmentRecord.drugIdNumbers
        self._drugIdNumbersTier = TreatmentRecord.drugIdNumbersTier

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
        self._patientIdTier = parsed.patientIdTier
        self._courseNumber = parsed.courseNumber
        self._courseNumberTier = parsed.courseNumberTier
        self._therapeuticModality = parsed.therapeuticModality
        self._therapeuticModalityTier = parsed.therapeuticModalityTier
        self._systematicTherapyAgentName = parsed.systematicTherapyAgentName
        self._systematicTherapyAgentNameTier = parsed.systematicTherapyAgentNameTier
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
        self._protocolNumberOrCode = parsed.protocolNumberOrCode
        self._protocolNumberOrCodeTier = parsed.protocolNumberOrCodeTier
        self._surgeryDetails = parsed.surgeryDetails
        self._surgeryDetailsTier = parsed.surgeryDetailsTier
        self._radiotherapyDetails = parsed.radiotherapyDetails
        self._radiotherapyDetailsTier = parsed.radiotherapyDetailsTier
        self._chemotherapyDetails = parsed.chemotherapyDetails
        self._chemotherapyDetailsTier = parsed.chemotherapyDetailsTier
        self._hematopoieticCellTransplant = parsed.hematopoieticCellTransplant
        self._hematopoieticCellTransplantTier = parsed.hematopoieticCellTransplantTier
        self._immunotherapyDetails = parsed.immunotherapyDetails
        self._immunotherapyDetailsTier = parsed.immunotherapyDetailsTier
        self._responseToTreatment = parsed.responseToTreatment
        self._responseToTreatmentTier = parsed.responseToTreatmentTier
        self._responseCriteriaUsed = parsed.responseCriteriaUsed
        self._responseCriteriaUsedTier = parsed.responseCriteriaUsedTier
        self._dateOfRecurrenceOrProgressionAfterThisTreatment = parsed.dateOfRecurrenceOrProgressionAfterThisTreatment
        self._dateOfRecurrenceOrProgressionAfterThisTreatmentTier = parsed.dateOfRecurrenceOrProgressionAfterThisTreatmentTier
        self._unexpectedOrUnusualToxicityDuringTreatment = parsed.unexpectedOrUnusualToxicityDuringTreatment
        self._unexpectedOrUnusualToxicityDuringTreatmentTier = parsed.unexpectedOrUnusualToxicityDuringTreatmentTier
        self._drugListOrAgent = parsed.drugListOrAgent
        self._drugListOrAgentTier = parsed.drugListOrAgentTier
        self._drugIdNumbers = parsed.drugIdNumbers
        self._drugIdNumbersTier = parsed.drugIdNumbersTier

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

    def getSystematicTherapyAgentName(self):
        return self._systematicTherapyAgentName

    def getSystematicTherapyAgentNameTier(self):
        return self._systematicTherapyAgentNameTier

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

    def getProtocolNumberOrCode(self):
        return self._protocolNumberOrCode

    def getProtocolNumberOrCodeTier(self):
        return self._protocolNumberOrCodeTier

    def getSurgeryDetails(self):
        return self._surgeryDetails

    def getSurgeryDetailsTier(self):
        return self._surgeryDetailsTier

    def getRadiotherapyDetails(self):
        return self._radiotherapyDetails

    def getRadiotherapyDetailsTier(self):
        return self._radiotherapyDetailsTier

    def getChemotherapyDetails(self):
        return self._chemotherapyDetails

    def getChemotherapyDetailsTier(self):
        return self._chemotherapyDetailsTier

    def getHematopoieticCellTransplant(self):
        return self._hematopoieticCellTransplant

    def getHematopoieticCellTransplantTier(self):
        return self._hematopoieticCellTransplantTier

    def getImmunotherapyDetails(self):
        return self._immunotherapyDetails

    def getImmunotherapyDetailsTier(self):
        return self._immunotherapyDetailsTier

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

    def getDrugListOrAgent(self):
        return self._drugListOrAgent

    def getDrugListOrAgentTier(self):
        return self._drugListOrAgentTier

    def getDrugIdNumbers(self):
        return self._drugIdNumbers

    def getDrugIdNumbersTier(self):
        return self._drugIdNumbersTier


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

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            str('id') : str(self.getId()),
            str('dataset_id') : str(self._datasetId),
            str('created') : str(self.getCreated()),
            str('updated') : str(self.getUpdated()),
            str('name') : str(self.getName()),
            str('description') : str(self.getDescription()),
            }

        # Unique fields
        if tier >= self.getPatientIdTier():
           record[str('patientId')] = str(self.getPatientId())
        if tier >= self.getPhysicalExamIdTier():
           record[str('physicalExamId')] = str(self.getPhysicalExamId())
        if tier >= self.getDateOfAssessmentTier():
           record[str('dateOfAssessment')] = str(self.getDateOfAssessment())
        if tier >= self.getDiseaseResponseOrStatusTier():
           record[str('diseaseResponseOrStatus')] = str(self.getDiseaseResponseOrStatus())
        if tier >= self.getOtherResponseClassificationTier():
           record[str('otherResponseClassification')] = str(self.getOtherResponseClassification())
        if tier >= self.getMinimalResidualDiseaseAssessmentTier():
           record[str('minimalResidualDiseaseAssessment')] = str(self.getMinimalResidualDiseaseAssessment())
        if tier >= self.getMethodOfResponseEvaluationTier():
           record[str('methodOfResponseEvaluation')] = str(self.getMethodOfResponseEvaluation())
        if tier >= self.getResponseCriteriaUsedTier():
           record[str('responseCriteriaUsed')] = str(self.getResponseCriteriaUsed())
        if tier >= self.getSummaryStageTier():
           record[str('summaryStage')] = str(self.getSummaryStage())
        if tier >= self.getSitesOfAnyProgressionOrRecurrenceTier():
           record[str('sitesOfAnyProgressionOrRecurrence')] = str(self.getSitesOfAnyProgressionOrRecurrence())
        if tier >= self.getVitalStatusTier():
           record[str('vitalStatus')] = str(self.getVitalStatus())
        if tier >= self.getHeightTier():
           record[str('height')] = str(self.getHeight())
        if tier >= self.getWeightTier():
           record[str('weight')] = str(self.getWeight())
        if tier >= self.getHeightUnitsTier():
           record[str('heightUnits')] = str(self.getHeightUnits())
        if tier >= self.getWeightUnitsTier():
           record[str('weightUnits')] = str(self.getWeightUnits())
        if tier >= self.getPerformanceStatusTier():
           record[str('performanceStatus')] = str(self.getPerformanceStatus())

        Outcome = protocol.Outcome(**record)
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

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            str('id') : str(self.getId()),
            str('dataset_id') : str(self._datasetId),
            str('created') : str(self.getCreated()),
            str('updated') : str(self.getUpdated()),
            str('name') : str(self.getName()),
            str('description') : str(self.getDescription()),
            }

        # Unique fields
        if tier >= self.getPatientIdTier():
           record[str('patientId')] = str(self.getPatientId())
        if tier >= self.getDateTier():
           record[str('date')] = str(self.getDate())
        if tier >= self.getLateComplicationOfTherapyDevelopedTier():
           record[str('lateComplicationOfTherapyDeveloped')] = str(self.getLateComplicationOfTherapyDeveloped())
        if tier >= self.getLateToxicityDetailTier():
           record[str('lateToxicityDetail')] = str(self.getLateToxicityDetail())
        if tier >= self.getSuspectedTreatmentInducedNeoplasmDevelopedTier():
           record[str('suspectedTreatmentInducedNeoplasmDeveloped')] = str(self.getSuspectedTreatmentInducedNeoplasmDeveloped())
        if tier >= self.getTreatmentInducedNeoplasmDetailsTier():
           record[str('treatmentInducedNeoplasmDetails')] = str(self.getTreatmentInducedNeoplasmDetails())

        Complication = protocol.Complication(**record)
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
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
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

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            str('id') : str(self.getId()),
            str('dataset_id') : str(self._datasetId),
            str('created') : str(self.getCreated()),
            str('updated') : str(self.getUpdated()),
            str('name') : str(self.getName()),
            str('description') : str(self.getDescription()),
            }

        # Unique fields
        if tier >= self.getPatientIdTier():
           record[str('patientId')] = str(self.getPatientId())
        if tier >= self.getDateOfMolecularTumorBoardTier():
           record[str('dateOfMolecularTumorBoard')] = str(self.getDateOfMolecularTumorBoard())
        if tier >= self.getTypeOfSampleAnalyzedTier():
           record[str('typeOfSampleAnalyzed')] = str(self.getTypeOfSampleAnalyzed())
        if tier >= self.getTypeOfTumourSampleAnalyzedTier():
           record[str('typeOfTumourSampleAnalyzed')] = str(self.getTypeOfTumourSampleAnalyzed())
        if tier >= self.getAnalysesDiscussedTier():
           record[str('analysesDiscussed')] = str(self.getAnalysesDiscussed())
        if tier >= self.getSomaticSampleTypeTier():
           record[str('somaticSampleType')] = str(self.getSomaticSampleType())
        if tier >= self.getNormalExpressionComparatorTier():
           record[str('normalExpressionComparator')] = str(self.getNormalExpressionComparator())
        if tier >= self.getDiseaseExpressionComparatorTier():
           record[str('diseaseExpressionComparator')] = str(self.getDiseaseExpressionComparator())
        if tier >= self.getHasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancerTier():
           record[str('hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer')] = str(self.getHasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer())
        if tier >= self.getActionableTargetFoundTier():
           record[str('actionableTargetFound')] = str(self.getActionableTargetFound())
        if tier >= self.getMolecularTumorBoardRecommendationTier():
           record[str('molecularTumorBoardRecommendation')] = str(self.getMolecularTumorBoardRecommendation())
        if tier >= self.getGermlineDnaSampleIdTier():
           record[str('germlineDnaSampleId')] = str(self.getGermlineDnaSampleId())
        if tier >= self.getTumorDnaSampleIdTier():
           record[str('tumorDnaSampleId')] = str(self.getTumorDnaSampleId())
        if tier >= self.getTumorRnaSampleIdTier():
           record[str('tumorRnaSampleId')] = str(self.getTumorRnaSampleId())
        if tier >= self.getGermlineSnvDiscussedTier():
           record[str('germlineSnvDiscussed')] = str(self.getGermlineSnvDiscussed())
        if tier >= self.getSomaticSnvDiscussedTier():
           record[str('somaticSnvDiscussed')] = str(self.getSomaticSnvDiscussed())
        if tier >= self.getCnvsDiscussedTier():
           record[str('cnvsDiscussed')] = str(self.getCnvsDiscussed())
        if tier >= self.getStructuralVariantDiscussedTier():
           record[str('structuralVariantDiscussed')] = str(self.getStructuralVariantDiscussed())
        if tier >= self.getClassificationOfVariantsTier():
           record[str('classificationOfVariants')] = str(self.getClassificationOfVariants())
        if tier >= self.getClinicalValidationProgressTier():
           record[str('clinicalValidationProgress')] = str(self.getClinicalValidationProgress())
        if tier >= self.getTypeOfValidationTier():
           record[str('typeOfValidation')] = str(self.getTypeOfValidation())
        if tier >= self.getAgentOrDrugClassTier():
           record[str('agentOrDrugClass')] = str(self.getAgentOrDrugClass())
        if tier >= self.getLevelOfEvidenceForExpressionTargetAgentMatchTier():
           record[str('levelOfEvidenceForExpressionTargetAgentMatch')] = str(self.getLevelOfEvidenceForExpressionTargetAgentMatch())
        if tier >= self.getDidTreatmentPlanChangeBasedOnProfilingResultTier():
           record[str('didTreatmentPlanChangeBasedOnProfilingResult')] = str(self.getDidTreatmentPlanChangeBasedOnProfilingResult())
        if tier >= self.getHowTreatmentHasAlteredBasedOnProfilingTier():
           record[str('howTreatmentHasAlteredBasedOnProfiling')] = str(self.getHowTreatmentHasAlteredBasedOnProfiling())
        if tier >= self.getReasonTreatmentPlanDidNotChangeBasedOnProfilingTier():
           record[str('reasonTreatmentPlanDidNotChangeBasedOnProfiling')] = str(self.getReasonTreatmentPlanDidNotChangeBasedOnProfiling())
        if tier >= self.getDetailsOfTreatmentPlanImpactTier():
           record[str('detailsOfTreatmentPlanImpact')] = str(self.getDetailsOfTreatmentPlanImpact())
        if tier >= self.getPatientOrFamilyInformedOfGermlineVariantTier():
           record[str('patientOrFamilyInformedOfGermlineVariant')] = str(self.getPatientOrFamilyInformedOfGermlineVariant())
        if tier >= self.getPatientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfilingTier():
           record[str('patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling')] = str(self.getPatientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling())
        if tier >= self.getSummaryReportTier():
           record[str('summaryReport')] = str(self.getSummaryReport())

        Tumourboard = protocol.Tumourboard(**record)
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
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
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