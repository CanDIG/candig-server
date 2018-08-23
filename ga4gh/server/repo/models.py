"""
peewee is a lightweight ORM with SQLite, postgresql,
and MySQL support. This file presents models for the
registry database.

Partially auto-generated using pwiz.

    python -m pwiz -e sqlite ga4gh-example-data/registry.db > models.py

For more on the peewee model API see:

https://peewee.readthedocs.io/en/latest/peewee/models.html

"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import peewee as pw
import datetime
# The databaseProxy is used to dynamically changed the
# backing database and needs to be set to an actual
# database instance to use these models.
databaseProxy = pw.Proxy()


class SqliteDatabase(pw.SqliteDatabase):
    def __init__(self, *_, **__):
        super(SqliteDatabase, self).__init__(*_, **__)


class BaseModel(pw.Model):
    attributes = pw.TextField(null=True)

    class Meta:
        database = databaseProxy


class Peer(BaseModel):
    url = pw.TextField(primary_key=True, null=False, unique=True)


class Announcement(BaseModel):
    # Provides the storage layer for AnnouncePeerRequest
    # Primary key for the record autoincrement
    id = pw.PrimaryKeyField()
    # URL submitted as a possible peer
    url = pw.TextField(null=False)
    # Other information about the request stored as JSON.
    remote_addr = pw.TextField(null=True)
    user_agent = pw.TextField(null=True)
    # The time at which this record was created.
    created = pw.DateTimeField()

    def save(self, *args, **kwargs):
        self.created = datetime.datetime.now()
        return super(Announcement, self).save(*args, **kwargs)


class Dataset(BaseModel):
    description = pw.TextField(null=True)
    id = pw.TextField(primary_key=True)
    info = pw.TextField(null=True)
    name = pw.TextField(unique=True)


class Biosample(BaseModel):
    created = pw.TextField(null=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    description = pw.TextField(null=True)
    disease = pw.TextField(null=True)
    id = pw.TextField(primary_key=True)
    individualid = pw.TextField(db_column='individualId', null=True)
    info = pw.TextField(null=True)
    name = pw.TextField()
    updated = pw.TextField(null=True)
    individualAgeAtCollection = pw.TextField(null=True)
    estimated_tumor_content = pw.TextField(null=True)
    normal_sample_source = pw.TextField(null=True)
    biopsy_data = pw.TextField(null=True)
    tumor_biopsy_anatomical_site = pw.TextField(null=True)
    biopsy_type = pw.TextField(null=True)
    sample_shipment_date = pw.TextField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Experiment(BaseModel):
    name = pw.TextField()
    id = pw.TextField(primary_key=True)
    description = pw.TextField(null=True)
    created = pw.TextField(null=True)
    updated = pw.TextField(null=True)
    runTime = pw.TextField(null=True)
    molecule = pw.TextField(null=True)
    strategy = pw.TextField(null=True)
    selection = pw.TextField(null=True)
    library = pw.TextField(null=True)
    libraryLayout = pw.TextField(null=True)
    instrumentModel = pw.TextField(null=True)
    instrumentDataFile = pw.TextField(null=True)
    sequencingCenter = pw.TextField(null=True)
    platformUnit = pw.TextField(null=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    biosample_id = pw.TextField(db_column='biosampleId', null=True)
    dna_library_construction_method = pw.TextField(null=True)
    wgs_sequencing_completion_date = pw.TextField(null=True)
    rna_library_construction_method = pw.TextField(null=True)
    rna_sequencing_completion_date = pw.TextField(null=True)
    panel_completion_date = pw.TextField(null=True)

    class Meta:
        indexes = (
            (('name'), True),
        )


class Analysis(BaseModel):
    name = pw.TextField()
    id = pw.TextField(primary_key=True)
    description = pw.TextField(null=True)
    created = pw.TextField(null=True)
    updated = pw.TextField(null=True)
    analysistype = pw.TextField(null=True)
    software = pw.TextField(null=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    experiment_id = pw.TextField(db_column='experimentId', null=True)
    other_analysis_descriptor = pw.TextField(null=True)
    other_analysis_completition_date = pw.TextField(null=True)

    class Meta:
        indexes = (
            (('name'), True),
        )


class Referenceset(BaseModel):
    assemblyid = pw.TextField(db_column='assemblyId', null=True)
    dataurl = pw.TextField(db_column='dataUrl')
    description = pw.TextField(null=True)
    id = pw.TextField(primary_key=True)
    isderived = pw.IntegerField(db_column='isDerived', null=True)
    md5checksum = pw.TextField(null=True)
    name = pw.TextField(unique=True)
    species = pw.TextField(db_column='species', null=True)
    sourceaccessions = pw.TextField(db_column='sourceAccessions', null=True)
    sourceuri = pw.TextField(db_column='sourceUri', null=True)


class Variantset(BaseModel):
    created = pw.TextField(null=True)
    dataurlindexmap = pw.TextField(db_column='dataUrlIndexMap')
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    id = pw.TextField(primary_key=True)
    metadata = pw.TextField(null=True)
    name = pw.TextField()
    referencesetid = pw.ForeignKeyField(
        db_column='referenceSetId', rel_model=Referenceset, to_field='id')
    updated = pw.TextField(null=True)
    patientId = pw.TextField(db_column='patientId', null=False)
    sampleId = pw.TextField(db_column='sampleId', null=False)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Callset(BaseModel):
    biosampleid = pw.TextField(db_column='biosampleId', null=True)
    id = pw.TextField(primary_key=True)
    name = pw.TextField()
    variantsetid = pw.ForeignKeyField(
        db_column='variantSetId', rel_model=Variantset, to_field='id')

    class Meta:
        indexes = (
            (('variantsetid', 'name'), True),
        )


class Ontology(BaseModel):
    dataurl = pw.TextField(db_column='dataUrl')
    id = pw.TextField(primary_key=True)
    name = pw.TextField(unique=True)
    ontologyprefix = pw.TextField(db_column='ontologyPrefix')


class Featureset(BaseModel):
    dataurl = pw.TextField(db_column='dataUrl')
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    id = pw.TextField(primary_key=True)
    info = pw.TextField(null=True)
    name = pw.TextField()
    ontologyid = pw.ForeignKeyField(
        db_column='ontologyId', rel_model=Ontology, to_field='id')
    referencesetid = pw.ForeignKeyField(
        db_column='referenceSetId', rel_model=Referenceset, to_field='id')
    sourceuri = pw.TextField(
        db_column='sourceUri', null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class ContinuousSet(BaseModel):
    dataurl = pw.TextField(db_column='dataUrl')
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    id = pw.TextField(primary_key=True)
    info = pw.TextField(null=True)
    name = pw.TextField()
    referencesetid = pw.ForeignKeyField(
        db_column='referenceSetId', rel_model=Referenceset, to_field='id')
    sourceuri = pw.TextField(
        db_column='sourceUri', null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Patient(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    patientId = pw.TextField(null=True)
    patientIdTier = pw.IntegerField(null=True)
    otherIds = pw.TextField(null=True)
    otherIdsTier = pw.IntegerField(null=True)
    dateOfBirth = pw.TextField(null=True)
    dateOfBirthTier = pw.IntegerField(null=True)
    gender = pw.TextField(null=True)
    genderTier = pw.IntegerField(null=True)
    ethnicity = pw.TextField(null=True)
    ethnicityTier = pw.IntegerField(null=True)
    race = pw.TextField(null=True)
    raceTier = pw.IntegerField(null=True)
    provinceOfResidence = pw.TextField(null=True)
    provinceOfResidenceTier = pw.IntegerField(null=True)
    dateOfDeath = pw.TextField(null=True)
    dateOfDeathTier = pw.IntegerField(null=True)
    causeOfDeath = pw.TextField(null=True)
    causeOfDeathTier = pw.IntegerField(null=True)
    autopsyTissueForResearch = pw.TextField(null=True)
    autopsyTissueForResearchTier = pw.IntegerField(null=True)
    priorMalignancy = pw.TextField(null=True)
    priorMalignancyTier = pw.IntegerField(null=True)
    dateOfPriorMalignancy = pw.TextField(null=True)
    dateOfPriorMalignancyTier = pw.IntegerField(null=True)
    familyHistoryAndRiskFactors = pw.TextField(null=True)
    familyHistoryAndRiskFactorsTier = pw.IntegerField(null=True)
    familyHistoryOfPredispositionSyndrome = pw.TextField(null=True)
    familyHistoryOfPredispositionSyndromeTier = pw.IntegerField(null=True)
    detailsOfPredispositionSyndrome = pw.TextField(null=True)
    detailsOfPredispositionSyndromeTier = pw.IntegerField(null=True)
    geneticCancerSyndrome = pw.TextField(null=True)
    geneticCancerSyndromeTier = pw.IntegerField(null=True)
    otherGeneticConditionOrSignificantComorbidity = pw.TextField(null=True)
    otherGeneticConditionOrSignificantComorbidityTier = pw.IntegerField(null=True)
    occupationalOrEnvironmentalExposure = pw.TextField(null=True)
    occupationalOrEnvironmentalExposureTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Enrollment(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    patientId = pw.TextField(null=True)
    patientIdTier = pw.IntegerField(null=True)
    enrollmentInstitution = pw.TextField(null=True)
    enrollmentInstitutionTier = pw.IntegerField(null=True)
    enrollmentApprovalDate = pw.TextField(null=True)
    enrollmentApprovalDateTier = pw.IntegerField(null=True)
    crossEnrollment = pw.TextField(null=True)
    crossEnrollmentTier = pw.IntegerField(null=True)
    otherPersonalizedMedicineStudyName = pw.TextField(null=True)
    otherPersonalizedMedicineStudyNameTier = pw.IntegerField(null=True)
    otherPersonalizedMedicineStudyId = pw.TextField(null=True)
    otherPersonalizedMedicineStudyIdTier = pw.IntegerField(null=True)
    ageAtEnrollment = pw.TextField(null=True)
    ageAtEnrollmentTier = pw.IntegerField(null=True)
    eligibilityCategory = pw.TextField(null=True)
    eligibilityCategoryTier = pw.IntegerField(null=True)
    statusAtEnrollment = pw.TextField(null=True)
    statusAtEnrollmentTier = pw.IntegerField(null=True)
    primaryOncologistName = pw.TextField(null=True)
    primaryOncologistNameTier = pw.IntegerField(null=True)
    primaryOncologistContact = pw.TextField(null=True)
    primaryOncologistContactTier = pw.IntegerField(null=True)
    referringPhysicianName = pw.TextField(null=True)
    referringPhysicianNameTier = pw.IntegerField(null=True)
    referringPhysicianContact = pw.TextField(null=True)
    referringPhysicianContactTier = pw.IntegerField(null=True)
    summaryOfIdRequest = pw.TextField(null=True)
    summaryOfIdRequestTier = pw.IntegerField(null=True)
    treatingCentreName = pw.TextField(null=True)
    treatingCentreNameTier = pw.IntegerField(null=True)
    treatingCentreProvince = pw.TextField(null=True)
    treatingCentreProvinceTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Consent(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    patientId = pw.TextField(null=True)
    patientIdTier = pw.IntegerField(null=True)
    consentId = pw.TextField(null=True)
    consentIdTier = pw.IntegerField(null=True)
    consentDate = pw.TextField(null=True)
    consentDateTier = pw.IntegerField(null=True)
    consentVersion = pw.TextField(null=True)
    consentVersionTier = pw.IntegerField(null=True)
    patientConsentedTo = pw.TextField(null=True)
    patientConsentedToTier = pw.IntegerField(null=True)
    reasonForRejection = pw.TextField(null=True)
    reasonForRejectionTier = pw.IntegerField(null=True)
    wasAssentObtained = pw.TextField(null=True)
    wasAssentObtainedTier = pw.IntegerField(null=True)
    dateOfAssent = pw.TextField(null=True)
    dateOfAssentTier = pw.IntegerField(null=True)
    assentFormVersion = pw.TextField(null=True)
    assentFormVersionTier = pw.IntegerField(null=True)
    ifAssentNotObtainedWhyNot = pw.TextField(null=True)
    ifAssentNotObtainedWhyNotTier = pw.IntegerField(null=True)
    reconsentDate = pw.TextField(null=True)
    reconsentDateTier = pw.IntegerField(null=True)
    reconsentVersion = pw.TextField(null=True)
    reconsentVersionTier = pw.IntegerField(null=True)
    consentingCoordinatorName = pw.TextField(null=True)
    consentingCoordinatorNameTier = pw.IntegerField(null=True)
    previouslyConsented = pw.TextField(null=True)
    previouslyConsentedTier = pw.IntegerField(null=True)
    nameOfOtherBiobank = pw.TextField(null=True)
    nameOfOtherBiobankTier = pw.IntegerField(null=True)
    hasConsentBeenWithdrawn = pw.TextField(null=True)
    hasConsentBeenWithdrawnTier = pw.IntegerField(null=True)
    dateOfConsentWithdrawal = pw.TextField(null=True)
    dateOfConsentWithdrawalTier = pw.IntegerField(null=True)
    typeOfConsentWithdrawal = pw.TextField(null=True)
    typeOfConsentWithdrawalTier = pw.IntegerField(null=True)
    reasonForConsentWithdrawal = pw.TextField(null=True)
    reasonForConsentWithdrawalTier = pw.IntegerField(null=True)
    consentFormComplete = pw.TextField(null=True)
    consentFormCompleteTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Diagnosis(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    patientId = pw.TextField(null=True)
    patientIdTier = pw.IntegerField(null=True)
    diagnosisId = pw.TextField(null=True)
    diagnosisIdTier = pw.IntegerField(null=True)
    diagnosisDate = pw.TextField(null=True)
    diagnosisDateTier = pw.IntegerField(null=True)
    ageAtDiagnosis = pw.TextField(null=True)
    ageAtDiagnosisTier = pw.IntegerField(null=True)
    cancerType = pw.TextField(null=True)
    cancerTypeTier = pw.IntegerField(null=True)
    classification = pw.TextField(null=True)
    classificationTier = pw.IntegerField(null=True)
    cancerSite = pw.TextField(null=True)
    cancerSiteTier = pw.IntegerField(null=True)
    histology = pw.TextField(null=True)
    histologyTier = pw.IntegerField(null=True)
    methodOfDefinitiveDiagnosis = pw.TextField(null=True)
    methodOfDefinitiveDiagnosisTier = pw.IntegerField(null=True)
    sampleType = pw.TextField(null=True)
    sampleTypeTier = pw.IntegerField(null=True)
    sampleSite = pw.TextField(null=True)
    sampleSiteTier = pw.IntegerField(null=True)
    tumorGrade = pw.TextField(null=True)
    tumorGradeTier = pw.IntegerField(null=True)
    gradingSystemUsed = pw.TextField(null=True)
    gradingSystemUsedTier = pw.IntegerField(null=True)
    sitesOfMetastases = pw.TextField(null=True)
    sitesOfMetastasesTier = pw.IntegerField(null=True)
    stagingSystem = pw.TextField(null=True)
    stagingSystemTier = pw.IntegerField(null=True)
    versionOrEditionOfTheStagingSystem = pw.TextField(null=True)
    versionOrEditionOfTheStagingSystemTier = pw.IntegerField(null=True)
    specificTumorStageAtDiagnosis = pw.TextField(null=True)
    specificTumorStageAtDiagnosisTier = pw.IntegerField(null=True)
    prognosticBiomarkers = pw.TextField(null=True)
    prognosticBiomarkersTier = pw.IntegerField(null=True)
    biomarkerQuantification = pw.TextField(null=True)
    biomarkerQuantificationTier = pw.IntegerField(null=True)
    additionalMolecularTesting = pw.TextField(null=True)
    additionalMolecularTestingTier = pw.IntegerField(null=True)
    additionalTestType = pw.TextField(null=True)
    additionalTestTypeTier = pw.IntegerField(null=True)
    laboratoryName = pw.TextField(null=True)
    laboratoryNameTier = pw.IntegerField(null=True)
    laboratoryAddress = pw.TextField(null=True)
    laboratoryAddressTier = pw.IntegerField(null=True)
    siteOfMetastases = pw.TextField(null=True)
    siteOfMetastasesTier = pw.IntegerField(null=True)
    stagingSystemVersion = pw.TextField(null=True)
    stagingSystemVersionTier = pw.IntegerField(null=True)
    specificStage = pw.TextField(null=True)
    specificStageTier = pw.IntegerField(null=True)
    cancerSpecificBiomarkers = pw.TextField(null=True)
    cancerSpecificBiomarkersTier = pw.IntegerField(null=True)
    additionalMolecularDiagnosticTestingPerformed = pw.TextField(null=True)
    additionalMolecularDiagnosticTestingPerformedTier = pw.IntegerField(null=True)
    additionalTest = pw.TextField(null=True)
    additionalTestTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Sample(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    patientId = pw.TextField(null=True)
    patientIdTier = pw.IntegerField(null=True)
    sampleId = pw.TextField(null=True)
    sampleIdTier = pw.IntegerField(null=True)
    diagnosisId = pw.TextField(null=True)
    diagnosisIdTier = pw.IntegerField(null=True)
    localBiobankId = pw.TextField(null=True)
    localBiobankIdTier = pw.IntegerField(null=True)
    collectionDate = pw.TextField(null=True)
    collectionDateTier = pw.IntegerField(null=True)
    collectionHospital = pw.TextField(null=True)
    collectionHospitalTier = pw.IntegerField(null=True)
    sampleType = pw.TextField(null=True)
    sampleTypeTier = pw.IntegerField(null=True)
    tissueDiseaseState = pw.TextField(null=True)
    tissueDiseaseStateTier = pw.IntegerField(null=True)
    anatomicSiteTheSampleObtainedFrom = pw.TextField(null=True)
    anatomicSiteTheSampleObtainedFromTier = pw.IntegerField(null=True)
    cancerType = pw.TextField(null=True)
    cancerTypeTier = pw.IntegerField(null=True)
    cancerSubtype = pw.TextField(null=True)
    cancerSubtypeTier = pw.IntegerField(null=True)
    pathologyReportId = pw.TextField(null=True)
    pathologyReportIdTier = pw.IntegerField(null=True)
    morphologicalCode = pw.TextField(null=True)
    morphologicalCodeTier = pw.IntegerField(null=True)
    topologicalCode = pw.TextField(null=True)
    topologicalCodeTier = pw.IntegerField(null=True)
    shippingDate = pw.TextField(null=True)
    shippingDateTier = pw.IntegerField(null=True)
    receivedDate = pw.TextField(null=True)
    receivedDateTier = pw.IntegerField(null=True)
    qualityControlPerformed = pw.TextField(null=True)
    qualityControlPerformedTier = pw.IntegerField(null=True)
    estimatedTumorContent = pw.TextField(null=True)
    estimatedTumorContentTier = pw.IntegerField(null=True)
    quantity = pw.TextField(null=True)
    quantityTier = pw.IntegerField(null=True)
    units = pw.TextField(null=True)
    unitsTier = pw.IntegerField(null=True)
    associatedBiobank = pw.TextField(null=True)
    associatedBiobankTier = pw.IntegerField(null=True)
    otherBiobank = pw.TextField(null=True)
    otherBiobankTier = pw.IntegerField(null=True)
    sopFollowed = pw.TextField(null=True)
    sopFollowedTier = pw.IntegerField(null=True)
    ifNotExplainAnyDeviation = pw.TextField(null=True)
    ifNotExplainAnyDeviationTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Treatment(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    patientId = pw.TextField(null=True)
    patientIdTier = pw.IntegerField(null=True)
    courseNumber = pw.TextField(null=True)
    courseNumberTier = pw.IntegerField(null=True)
    therapeuticModality = pw.TextField(null=True)
    therapeuticModalityTier = pw.IntegerField(null=True)
    systematicTherapyAgentName = pw.TextField(null=True)
    systematicTherapyAgentNameTier = pw.IntegerField(null=True)
    treatmentPlanType = pw.TextField(null=True)
    treatmentPlanTypeTier = pw.IntegerField(null=True)
    treatmentIntent = pw.TextField(null=True)
    treatmentIntentTier = pw.IntegerField(null=True)
    startDate = pw.TextField(null=True)
    startDateTier = pw.IntegerField(null=True)
    stopDate = pw.TextField(null=True)
    stopDateTier = pw.IntegerField(null=True)
    reasonForEndingTheTreatment = pw.TextField(null=True)
    reasonForEndingTheTreatmentTier = pw.IntegerField(null=True)
    protocolNumberOrCode = pw.TextField(null=True)
    protocolNumberOrCodeTier = pw.IntegerField(null=True)
    surgeryDetails = pw.TextField(null=True)
    surgeryDetailsTier = pw.IntegerField(null=True)
    radiotherapyDetails = pw.TextField(null=True)
    radiotherapyDetailsTier = pw.IntegerField(null=True)
    chemotherapyDetails = pw.TextField(null=True)
    chemotherapyDetailsTier = pw.IntegerField(null=True)
    hematopoieticCellTransplant = pw.TextField(null=True)
    hematopoieticCellTransplantTier = pw.IntegerField(null=True)
    immunotherapyDetails = pw.TextField(null=True)
    immunotherapyDetailsTier = pw.IntegerField(null=True)
    responseToTreatment = pw.TextField(null=True)
    responseToTreatmentTier = pw.IntegerField(null=True)
    responseCriteriaUsed = pw.TextField(null=True)
    responseCriteriaUsedTier = pw.IntegerField(null=True)
    dateOfRecurrenceOrProgressionAfterThisTreatment = pw.TextField(null=True)
    dateOfRecurrenceOrProgressionAfterThisTreatmentTier = pw.IntegerField(null=True)
    unexpectedOrUnusualToxicityDuringTreatment = pw.TextField(null=True)
    unexpectedOrUnusualToxicityDuringTreatmentTier = pw.IntegerField(null=True)
    drugListOrAgent = pw.TextField(null=True)
    drugListOrAgentTier = pw.IntegerField(null=True)
    drugIdNumbers = pw.TextField(null=True)
    drugIdNumbersTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Outcome(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    patientId = pw.TextField(null=True)
    patientIdTier = pw.IntegerField(null=True)
    physicalExamId = pw.TextField(null=True)
    physicalExamIdTier = pw.IntegerField(null=True)
    dateOfAssessment = pw.TextField(null=True)
    dateOfAssessmentTier = pw.IntegerField(null=True)
    diseaseResponseOrStatus = pw.TextField(null=True)
    diseaseResponseOrStatusTier = pw.IntegerField(null=True)
    otherResponseClassification = pw.TextField(null=True)
    otherResponseClassificationTier = pw.IntegerField(null=True)
    minimalResidualDiseaseAssessment = pw.TextField(null=True)
    minimalResidualDiseaseAssessmentTier = pw.IntegerField(null=True)
    methodOfResponseEvaluation = pw.TextField(null=True)
    methodOfResponseEvaluationTier = pw.IntegerField(null=True)
    responseCriteriaUsed = pw.TextField(null=True)
    responseCriteriaUsedTier = pw.IntegerField(null=True)
    summaryStage = pw.TextField(null=True)
    summaryStageTier = pw.IntegerField(null=True)
    sitesOfAnyProgressionOrRecurrence = pw.TextField(null=True)
    sitesOfAnyProgressionOrRecurrenceTier = pw.IntegerField(null=True)
    vitalStatus = pw.TextField(null=True)
    vitalStatusTier = pw.IntegerField(null=True)
    height = pw.TextField(null=True)
    heightTier = pw.IntegerField(null=True)
    weight = pw.TextField(null=True)
    weightTier = pw.IntegerField(null=True)
    heightUnits = pw.TextField(null=True)
    heightUnitsTier = pw.IntegerField(null=True)
    weightUnits = pw.TextField(null=True)
    weightUnitsTier = pw.IntegerField(null=True)
    performanceStatus = pw.TextField(null=True)
    performanceStatusTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Complication(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    patientId = pw.TextField(null=True)
    patientIdTier = pw.IntegerField(null=True)
    date = pw.TextField(null=True)
    dateTier = pw.IntegerField(null=True)
    lateComplicationOfTherapyDeveloped = pw.TextField(null=True)
    lateComplicationOfTherapyDevelopedTier = pw.IntegerField(null=True)
    lateToxicityDetail = pw.TextField(null=True)
    lateToxicityDetailTier = pw.IntegerField(null=True)
    suspectedTreatmentInducedNeoplasmDeveloped = pw.TextField(null=True)
    suspectedTreatmentInducedNeoplasmDevelopedTier = pw.IntegerField(null=True)
    treatmentInducedNeoplasmDetails = pw.TextField(null=True)
    treatmentInducedNeoplasmDetailsTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Tumourboard(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    patientId = pw.TextField(null=True)
    patientIdTier = pw.IntegerField(null=True)
    dateOfMolecularTumorBoard = pw.TextField(null=True)
    dateOfMolecularTumorBoardTier = pw.IntegerField(null=True)
    typeOfSampleAnalyzed = pw.TextField(null=True)
    typeOfSampleAnalyzedTier = pw.IntegerField(null=True)
    typeOfTumourSampleAnalyzed = pw.TextField(null=True)
    typeOfTumourSampleAnalyzedTier = pw.IntegerField(null=True)
    analysesDiscussed = pw.TextField(null=True)
    analysesDiscussedTier = pw.IntegerField(null=True)
    somaticSampleType = pw.TextField(null=True)
    somaticSampleTypeTier = pw.IntegerField(null=True)
    normalExpressionComparator = pw.TextField(null=True)
    normalExpressionComparatorTier = pw.IntegerField(null=True)
    diseaseExpressionComparator = pw.TextField(null=True)
    diseaseExpressionComparatorTier = pw.IntegerField(null=True)
    hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer = pw.TextField(null=True)
    hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancerTier = pw.IntegerField(null=True)
    actionableTargetFound = pw.TextField(null=True)
    actionableTargetFoundTier = pw.IntegerField(null=True)
    molecularTumorBoardRecommendation = pw.TextField(null=True)
    molecularTumorBoardRecommendationTier = pw.IntegerField(null=True)
    germlineDnaSampleId = pw.TextField(null=True)
    germlineDnaSampleIdTier = pw.IntegerField(null=True)
    tumorDnaSampleId = pw.TextField(null=True)
    tumorDnaSampleIdTier = pw.IntegerField(null=True)
    tumorRnaSampleId = pw.TextField(null=True)
    tumorRnaSampleIdTier = pw.IntegerField(null=True)
    germlineSnvDiscussed = pw.TextField(null=True)
    germlineSnvDiscussedTier = pw.IntegerField(null=True)
    somaticSnvDiscussed = pw.TextField(null=True)
    somaticSnvDiscussedTier = pw.IntegerField(null=True)
    cnvsDiscussed = pw.TextField(null=True)
    cnvsDiscussedTier = pw.IntegerField(null=True)
    structuralVariantDiscussed = pw.TextField(null=True)
    structuralVariantDiscussedTier = pw.IntegerField(null=True)
    classificationOfVariants = pw.TextField(null=True)
    classificationOfVariantsTier = pw.IntegerField(null=True)
    clinicalValidationProgress = pw.TextField(null=True)
    clinicalValidationProgressTier = pw.IntegerField(null=True)
    typeOfValidation = pw.TextField(null=True)
    typeOfValidationTier = pw.IntegerField(null=True)
    agentOrDrugClass = pw.TextField(null=True)
    agentOrDrugClassTier = pw.IntegerField(null=True)
    levelOfEvidenceForExpressionTargetAgentMatch = pw.TextField(null=True)
    levelOfEvidenceForExpressionTargetAgentMatchTier = pw.IntegerField(null=True)
    didTreatmentPlanChangeBasedOnProfilingResult = pw.TextField(null=True)
    didTreatmentPlanChangeBasedOnProfilingResultTier = pw.IntegerField(null=True)
    howTreatmentHasAlteredBasedOnProfiling = pw.TextField(null=True)
    howTreatmentHasAlteredBasedOnProfilingTier = pw.IntegerField(null=True)
    reasonTreatmentPlanDidNotChangeBasedOnProfiling = pw.TextField(null=True)
    reasonTreatmentPlanDidNotChangeBasedOnProfilingTier = pw.IntegerField(null=True)
    detailsOfTreatmentPlanImpact = pw.TextField(null=True)
    detailsOfTreatmentPlanImpactTier = pw.IntegerField(null=True)
    patientOrFamilyInformedOfGermlineVariant = pw.TextField(null=True)
    patientOrFamilyInformedOfGermlineVariantTier = pw.IntegerField(null=True)
    patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling = pw.TextField(null=True)
    patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfilingTier = pw.IntegerField(null=True)
    summaryReport = pw.TextField(null=True)
    summaryReportTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Individual(BaseModel):
    created = pw.TextField()
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    description = pw.TextField(null=True)
    id = pw.TextField(primary_key=True)
    info = pw.TextField(null=True)
    name = pw.TextField(null=True)
    sex = pw.TextField(null=True)
    species = pw.TextField(null=True)
    updated = pw.TextField(null=True)
    patient_id = pw.TextField(null=True)
    regional_profiling_centre = pw.TextField(null=True)
    diagnosis = pw.TextField(null=True)
    pathology_type = pw.TextField(null=True)
    enrollment_approval_date = pw.TextField(null=True)
    enrollment_approval_initials = pw.TextField(null=True)
    date_of_upload_to_sFTP = pw.TextField(null=True)
    tumor_board_presentation_date_and_analyses = pw.TextField(null=True)
    comments = pw.TextField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Phenotypeassociationset(BaseModel):
    dataurl = pw.TextField(db_column='dataUrl')
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    id = pw.TextField(primary_key=True)
    name = pw.TextField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Readgroupset(BaseModel):
    dataurl = pw.TextField(db_column='dataUrl')
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    id = pw.TextField(primary_key=True)
    indexfile = pw.TextField(db_column='indexFile')
    name = pw.TextField()
    programs = pw.TextField(null=True)
    referencesetid = pw.ForeignKeyField(
        db_column='referenceSetId', rel_model=Referenceset, to_field='id')
    stats = pw.TextField()
    patientId = pw.TextField(db_column='patientId', null=False)
    sampleId = pw.TextField(db_column='sampleId', null=False)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Readgroup(BaseModel):
    biosampleid = pw.TextField(db_column='biosampleId', null=True)
    created = pw.TextField(null=True)
    description = pw.TextField(null=True)
    experiment = pw.TextField(null=True)
    id = pw.TextField(primary_key=True)
    name = pw.TextField()
    predictedinsertsize = pw.IntegerField(
        db_column='predictedInsertSize', null=True)
    readgroupsetid = pw.ForeignKeyField(
        db_column='readGroupSetId', rel_model=Readgroupset, to_field='id')
    samplename = pw.TextField(db_column='sampleName', null=True)
    stats = pw.TextField()
    updated = pw.TextField(null=True)

    class Meta:
        indexes = (
            (('readgroupsetid', 'name'), True),
        )


class Reference(BaseModel):
    id = pw.TextField(null=True, primary_key=True)
    isderived = pw.IntegerField(db_column='isDerived', null=True)
    length = pw.IntegerField(null=True)
    md5checksum = pw.TextField(null=True)
    name = pw.TextField()
    species = pw.TextField(db_column='species', null=True)
    referencesetid = pw.ForeignKeyField(
        db_column='referenceSetId', rel_model=Referenceset, to_field='id')
    sourceaccessions = pw.TextField(db_column='sourceAccessions', null=True)
    sourcedivergence = pw.FloatField(db_column='sourceDivergence', null=True)
    sourceuri = pw.TextField(db_column='sourceUri', null=True)

    class Meta:
        indexes = (
            (('referencesetid', 'name'), True),
        )


class Rnaquantificationset(BaseModel):
    dataurl = pw.TextField(db_column='dataUrl')
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    id = pw.TextField(primary_key=True)
    info = pw.TextField(null=True)
    name = pw.TextField()
    referencesetid = pw.ForeignKeyField(
        db_column='referenceSetId', rel_model=Referenceset, to_field='id')

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class System(BaseModel):
    key = pw.TextField(primary_key=True)
    value = pw.TextField()


class Variantannotationset(BaseModel):
    analysis = pw.TextField(null=True)
    annotationtype = pw.TextField(db_column='annotationType', null=True)
    created = pw.TextField(null=True)
    id = pw.TextField(primary_key=True)
    name = pw.TextField()
    ontologyid = pw.ForeignKeyField(
        db_column='ontologyId', rel_model=Ontology, to_field='id')
    updated = pw.TextField(null=True)
    variantsetid = pw.ForeignKeyField(
        db_column='variantSetId', rel_model=Variantset, to_field='id')

    class Meta:
        indexes = (
            (('variantsetid', 'name'), True),
        )
