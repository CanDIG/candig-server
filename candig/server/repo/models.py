"""
peewee is a lightweight ORM with SQLite, postgresql,
and MySQL support. This file presents models for the
registry database.

Partially auto-generated using pwiz.

    python -m pwiz -e sqlite ga4gh-example-data/registry.db > models.py

For more on the peewee model API see:

https://peewee.readthedocs.io/en/latest/peewee/models.html

"""

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
    recordingDate = pw.TextField(null=True)
    recordingDateTier = pw.IntegerField(null=True)
    startInterval = pw.TextField(null=True)
    startIntervalTier = pw.IntegerField(null=True)

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
    responseToTreatment = pw.TextField(null=True)
    responseToTreatmentTier = pw.IntegerField(null=True)
    responseCriteriaUsed = pw.TextField(null=True)
    responseCriteriaUsedTier = pw.IntegerField(null=True)
    dateOfRecurrenceOrProgressionAfterThisTreatment = pw.TextField(null=True)
    dateOfRecurrenceOrProgressionAfterThisTreatmentTier = pw.IntegerField(null=True)
    unexpectedOrUnusualToxicityDuringTreatment = pw.TextField(null=True)
    unexpectedOrUnusualToxicityDuringTreatmentTier = pw.IntegerField(null=True)
    drugIdNumbers = pw.TextField(null=True)
    drugIdNumbersTier = pw.IntegerField(null=True)
    diagnosisId = pw.TextField(null=True)
    diagnosisIdTier = pw.IntegerField(null=True)
    treatmentPlanId = pw.TextField(null=True)
    treatmentPlanIdTier = pw.IntegerField(null=True)

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
    overallSurvivalInMonths = pw.TextField(null=True)
    overallSurvivalInMonthsTier = pw.IntegerField(null=True)
    diseaseFreeSurvivalInMonths = pw.TextField(null=True)
    diseaseFreeSurvivalInMonthsTier = pw.IntegerField(null=True)

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


class Extraction(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    extractionId = pw.TextField(null=True)
    extractionIdTier = pw.IntegerField(null=True)
    sampleId = pw.TextField(null=True)
    sampleIdTier = pw.IntegerField(null=True)
    rnaBlood = pw.TextField(null=True)
    rnaBloodTier = pw.IntegerField(null=True)
    dnaBlood = pw.TextField(null=True)
    dnaBloodTier = pw.IntegerField(null=True)
    rnaTissue = pw.TextField(null=True)
    rnaTissueTier = pw.IntegerField(null=True)
    dnaTissue = pw.TextField(null=True)
    dnaTissueTier = pw.IntegerField(null=True)
    site = pw.TextField(null=True)
    siteTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Sequencing(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    sequencingId = pw.TextField(null=True)
    sequencingIdTier = pw.IntegerField(null=True)
    sampleId = pw.TextField(null=True)
    sampleIdTier = pw.IntegerField(null=True)
    dnaLibraryKit = pw.TextField(null=True)
    dnaLibraryKitTier = pw.IntegerField(null=True)
    dnaSeqPlatform = pw.TextField(null=True)
    dnaSeqPlatformTier = pw.IntegerField(null=True)
    dnaReadLength = pw.TextField(null=True)
    dnaReadLengthTier = pw.IntegerField(null=True)
    rnaLibraryKit = pw.TextField(null=True)
    rnaLibraryKitTier = pw.IntegerField(null=True)
    rnaSeqPlatform = pw.TextField(null=True)
    rnaSeqPlatformTier = pw.IntegerField(null=True)
    rnaReadLength = pw.TextField(null=True)
    rnaReadLengthTier = pw.IntegerField(null=True)
    pcrCycles = pw.TextField(null=True)
    pcrCyclesTier = pw.IntegerField(null=True)
    extractionId = pw.TextField(null=True)
    extractionIdTier = pw.IntegerField(null=True)
    site = pw.TextField(null=True)
    siteTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Alignment(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    alignmentId = pw.TextField(null=True)
    alignmentIdTier = pw.IntegerField(null=True)
    sampleId = pw.TextField(null=True)
    sampleIdTier = pw.IntegerField(null=True)
    inHousePipeline = pw.TextField(null=True)
    inHousePipelineTier = pw.IntegerField(null=True)
    alignmentTool = pw.TextField(null=True)
    alignmentToolTier = pw.IntegerField(null=True)
    mergeTool = pw.TextField(null=True)
    mergeToolTier = pw.IntegerField(null=True)
    markDuplicates = pw.TextField(null=True)
    markDuplicatesTier = pw.IntegerField(null=True)
    realignerTarget = pw.TextField(null=True)
    realignerTargetTier = pw.IntegerField(null=True)
    indelRealigner = pw.TextField(null=True)
    indelRealignerTier = pw.IntegerField(null=True)
    baseRecalibrator = pw.TextField(null=True)
    baseRecalibratorTier = pw.IntegerField(null=True)
    printReads = pw.TextField(null=True)
    printReadsTier = pw.IntegerField(null=True)
    idxStats = pw.TextField(null=True)
    idxStatsTier = pw.IntegerField(null=True)
    flagStat = pw.TextField(null=True)
    flagStatTier = pw.IntegerField(null=True)
    coverage = pw.TextField(null=True)
    coverageTier = pw.IntegerField(null=True)
    insertSizeMetrics = pw.TextField(null=True)
    insertSizeMetricsTier = pw.IntegerField(null=True)
    fastqc = pw.TextField(null=True)
    fastqcTier = pw.IntegerField(null=True)
    reference = pw.TextField(null=True)
    referenceTier = pw.IntegerField(null=True)
    sequencingId = pw.TextField(null=True)
    sequencingIdTier = pw.IntegerField(null=True)
    site = pw.TextField(null=True)
    siteTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class VariantCalling(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    variantCallingId = pw.TextField(null=True)
    variantCallingIdTier = pw.IntegerField(null=True)
    sampleId = pw.TextField(null=True)
    sampleIdTier = pw.IntegerField(null=True)
    inHousePipeline = pw.TextField(null=True)
    inHousePipelineTier = pw.IntegerField(null=True)
    variantCaller = pw.TextField(null=True)
    variantCallerTier = pw.IntegerField(null=True)
    tabulate = pw.TextField(null=True)
    tabulateTier = pw.IntegerField(null=True)
    annotation = pw.TextField(null=True)
    annotationTier = pw.IntegerField(null=True)
    mergeTool = pw.TextField(null=True)
    mergeToolTier = pw.IntegerField(null=True)
    rdaToTab = pw.TextField(null=True)
    rdaToTabTier = pw.IntegerField(null=True)
    delly = pw.TextField(null=True)
    dellyTier = pw.IntegerField(null=True)
    postFilter = pw.TextField(null=True)
    postFilterTier = pw.IntegerField(null=True)
    clipFilter = pw.TextField(null=True)
    clipFilterTier = pw.IntegerField(null=True)
    cosmic = pw.TextField(null=True)
    cosmicTier = pw.IntegerField(null=True)
    dbSnp = pw.TextField(null=True)
    dbSnpTier = pw.IntegerField(null=True)
    alignmentId = pw.TextField(null=True)
    alignmentIdTier = pw.IntegerField(null=True)
    site = pw.TextField(null=True)
    siteTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class FusionDetection(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    fusionDetectionId = pw.TextField(null=True)
    fusionDetectionIdTier = pw.IntegerField(null=True)
    sampleId = pw.TextField(null=True)
    sampleIdTier = pw.IntegerField(null=True)
    inHousePipeline = pw.TextField(null=True)
    inHousePipelineTier = pw.IntegerField(null=True)
    svDetection = pw.TextField(null=True)
    svDetectionTier = pw.IntegerField(null=True)
    fusionDetection = pw.TextField(null=True)
    fusionDetectionTier = pw.IntegerField(null=True)
    realignment = pw.TextField(null=True)
    realignmentTier = pw.IntegerField(null=True)
    annotation = pw.TextField(null=True)
    annotationTier = pw.IntegerField(null=True)
    genomeReference = pw.TextField(null=True)
    genomeReferenceTier = pw.IntegerField(null=True)
    geneModels = pw.TextField(null=True)
    geneModelsTier = pw.IntegerField(null=True)
    alignmentId = pw.TextField(null=True)
    alignmentIdTier = pw.IntegerField(null=True)
    site = pw.TextField(null=True)
    siteTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class ExpressionAnalysis(BaseModel):
    # Common fields
    id = pw.TextField(primary_key=True)
    datasetid = pw.ForeignKeyField(
        db_column='datasetId', rel_model=Dataset, to_field='id')
    created = pw.TextField()
    updated = pw.TextField(null=True)
    name = pw.TextField(null=True)
    description = pw.TextField(null=True)
    # Unique fields
    expressionAnalysisId = pw.TextField(null=True)
    expressionAnalysisIdTier = pw.IntegerField(null=True)
    sampleId = pw.TextField(null=True)
    sampleIdTier = pw.IntegerField(null=True)
    readLength = pw.TextField(null=True)
    readLengthTier = pw.IntegerField(null=True)
    reference = pw.TextField(null=True)
    referenceTier = pw.IntegerField(null=True)
    alignmentTool = pw.TextField(null=True)
    alignmentToolTier = pw.IntegerField(null=True)
    bamHandling = pw.TextField(null=True)
    bamHandlingTier = pw.IntegerField(null=True)
    expressionEstimation = pw.TextField(null=True)
    expressionEstimationTier = pw.IntegerField(null=True)
    sequencingId = pw.TextField(null=True)
    sequencingIdTier = pw.IntegerField(null=True)
    site = pw.TextField(null=True)
    siteTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Chemotherapy(BaseModel):
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
    startDate = pw.TextField(null=True)
    startDateTier = pw.IntegerField(null=True)
    stopDate = pw.TextField(null=True)
    stopDateTier = pw.IntegerField(null=True)
    systematicTherapyAgentName = pw.TextField(null=True)
    systematicTherapyAgentNameTier = pw.IntegerField(null=True)
    route = pw.TextField(null=True)
    routeTier = pw.IntegerField(null=True)
    dose = pw.TextField(null=True)
    doseTier = pw.IntegerField(null=True)
    doseFrequency = pw.TextField(null=True)
    doseFrequencyTier = pw.IntegerField(null=True)
    doseUnit = pw.TextField(null=True)
    doseUnitTier = pw.IntegerField(null=True)
    daysPerCycle = pw.TextField(null=True)
    daysPerCycleTier = pw.IntegerField(null=True)
    numberOfCycle = pw.TextField(null=True)
    numberOfCycleTier = pw.IntegerField(null=True)
    treatmentIntent = pw.TextField(null=True)
    treatmentIntentTier = pw.IntegerField(null=True)
    treatingCentreName = pw.TextField(null=True)
    treatingCentreNameTier = pw.IntegerField(null=True)
    type = pw.TextField(null=True)
    typeTier = pw.IntegerField(null=True)
    protocolCode = pw.TextField(null=True)
    protocolCodeTier = pw.IntegerField(null=True)
    recordingDate = pw.TextField(null=True)
    recordingDateTier = pw.IntegerField(null=True)
    treatmentPlanId = pw.TextField(null=True)
    treatmentPlanIdTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Radiotherapy(BaseModel):
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
    startDate = pw.TextField(null=True)
    startDateTier = pw.IntegerField(null=True)
    stopDate = pw.TextField(null=True)
    stopDateTier = pw.IntegerField(null=True)
    therapeuticModality = pw.TextField(null=True)
    therapeuticModalityTier = pw.IntegerField(null=True)
    baseline = pw.TextField(null=True)
    baselineTier = pw.IntegerField(null=True)
    testResult = pw.TextField(null=True)
    testResultTier = pw.IntegerField(null=True)
    testResultStd = pw.TextField(null=True)
    testResultStdTier = pw.IntegerField(null=True)
    treatingCentreName = pw.TextField(null=True)
    treatingCentreNameTier = pw.IntegerField(null=True)
    startIntervalRad = pw.TextField(null=True)
    startIntervalRadTier = pw.IntegerField(null=True)
    startIntervalRadRaw = pw.TextField(null=True)
    startIntervalRadRawTier = pw.IntegerField(null=True)
    recordingDate = pw.TextField(null=True)
    recordingDateTier = pw.IntegerField(null=True)
    adjacentFields = pw.TextField(null=True)
    adjacentFieldsTier = pw.IntegerField(null=True)
    adjacentFractions = pw.TextField(null=True)
    adjacentFractionsTier = pw.IntegerField(null=True)
    complete = pw.TextField(null=True)
    completeTier = pw.IntegerField(null=True)
    brachytherapyDose = pw.TextField(null=True)
    brachytherapyDoseTier = pw.IntegerField(null=True)
    radiotherapyDose = pw.TextField(null=True)
    radiotherapyDoseTier = pw.IntegerField(null=True)
    siteNumber = pw.TextField(null=True)
    siteNumberTier = pw.IntegerField(null=True)
    technique = pw.TextField(null=True)
    techniqueTier = pw.IntegerField(null=True)
    treatedRegion = pw.TextField(null=True)
    treatedRegionTier = pw.IntegerField(null=True)
    treatmentPlanId = pw.TextField(null=True)
    treatmentPlanIdTier = pw.IntegerField(null=True)
    radiationType = pw.TextField(null=True)
    radiationTypeTier = pw.IntegerField(null=True)
    radiationSite = pw.TextField(null=True)
    radiationSiteTier = pw.IntegerField(null=True)
    totalDose = pw.TextField(null=True)
    totalDoseTier = pw.IntegerField(null=True)
    boostSite = pw.TextField(null=True)
    boostSiteTier = pw.IntegerField(null=True)
    boostDose = pw.TextField(null=True)
    boostDoseTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Surgery(BaseModel):
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
    startDate = pw.TextField(null=True)
    startDateTier = pw.IntegerField(null=True)
    stopDate = pw.TextField(null=True)
    stopDateTier = pw.IntegerField(null=True)
    sampleId = pw.TextField(null=True)
    sampleIdTier = pw.IntegerField(null=True)
    collectionTimePoint = pw.TextField(null=True)
    collectionTimePointTier = pw.IntegerField(null=True)
    diagnosisDate = pw.TextField(null=True)
    diagnosisDateTier = pw.IntegerField(null=True)
    site = pw.TextField(null=True)
    siteTier = pw.IntegerField(null=True)
    type = pw.TextField(null=True)
    typeTier = pw.IntegerField(null=True)
    recordingDate = pw.TextField(null=True)
    recordingDateTier = pw.IntegerField(null=True)
    treatmentPlanId = pw.TextField(null=True)
    treatmentPlanIdTier = pw.IntegerField(null=True)
    courseNumber = pw.TextField(null=True)
    courseNumberTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Immunotherapy(BaseModel):
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
    startDate = pw.TextField(null=True)
    startDateTier = pw.IntegerField(null=True)
    immunotherapyType = pw.TextField(null=True)
    immunotherapyTypeTier = pw.IntegerField(null=True)
    immunotherapyTarget = pw.TextField(null=True)
    immunotherapyTargetTier = pw.IntegerField(null=True)
    immunotherapyDetail = pw.TextField(null=True)
    immunotherapyDetailTier = pw.IntegerField(null=True)
    treatmentPlanId = pw.TextField(null=True)
    treatmentPlanIdTier = pw.IntegerField(null=True)
    courseNumber = pw.TextField(null=True)
    courseNumberTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Celltransplant(BaseModel):
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
    startDate = pw.TextField(null=True)
    startDateTier = pw.IntegerField(null=True)
    cellSource = pw.TextField(null=True)
    cellSourceTier = pw.IntegerField(null=True)
    donorType = pw.TextField(null=True)
    donorTypeTier = pw.IntegerField(null=True)
    treatmentPlanId = pw.TextField(null=True)
    treatmentPlanIdTier = pw.IntegerField(null=True)
    courseNumber = pw.TextField(null=True)
    courseNumberTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Slide(BaseModel):
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
    slideId = pw.TextField(null=True)
    slideIdTier = pw.IntegerField(null=True)
    slideOtherId = pw.TextField(null=True)
    slideOtherIdTier = pw.IntegerField(null=True)
    lymphocyteInfiltrationPercent = pw.TextField(null=True)
    lymphocyteInfiltrationPercentTier = pw.IntegerField(null=True)
    tumorNucleiPercent = pw.TextField(null=True)
    tumorNucleiPercentTier = pw.IntegerField(null=True)
    monocyteInfiltrationPercent = pw.TextField(null=True)
    monocyteInfiltrationPercentTier = pw.IntegerField(null=True)
    normalCellsPercent = pw.TextField(null=True)
    normalCellsPercentTier = pw.IntegerField(null=True)
    tumorCellsPercent = pw.TextField(null=True)
    tumorCellsPercentTier = pw.IntegerField(null=True)
    stromalCellsPercent = pw.TextField(null=True)
    stromalCellsPercentTier = pw.IntegerField(null=True)
    eosinophilInfiltrationPercent = pw.TextField(null=True)
    eosinophilInfiltrationPercentTier = pw.IntegerField(null=True)
    neutrophilInfiltrationPercent = pw.TextField(null=True)
    neutrophilInfiltrationPercentTier = pw.IntegerField(null=True)
    granulocyteInfiltrationPercent = pw.TextField(null=True)
    granulocyteInfiltrationPercentTier = pw.IntegerField(null=True)
    necrosisPercent = pw.TextField(null=True)
    necrosisPercentTier = pw.IntegerField(null=True)
    inflammatoryInfiltrationPercent = pw.TextField(null=True)
    inflammatoryInfiltrationPercentTier = pw.IntegerField(null=True)
    proliferatingCellsNumber = pw.TextField(null=True)
    proliferatingCellsNumberTier = pw.IntegerField(null=True)
    sectionLocation = pw.TextField(null=True)
    sectionLocationTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Study(BaseModel):
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
    startDate = pw.TextField(null=True)
    startDateTier = pw.IntegerField(null=True)
    endDate = pw.TextField(null=True)
    endDateTier = pw.IntegerField(null=True)
    status = pw.TextField(null=True)
    statusTier = pw.IntegerField(null=True)
    recordingDate = pw.TextField(null=True)
    recordingDateTier = pw.IntegerField(null=True)

    class Meta:
        indexes = (
            (('datasetid', 'name'), True),
        )


class Labtest(BaseModel):
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
    startDate = pw.TextField(null=True)
    startDateTier = pw.IntegerField(null=True)
    collectionDate = pw.TextField(null=True)
    collectionDateTier = pw.IntegerField(null=True)
    endDate = pw.TextField(null=True)
    endDateTier = pw.IntegerField(null=True)
    eventType = pw.TextField(null=True)
    eventTypeTier = pw.IntegerField(null=True)
    testResults = pw.TextField(null=True)
    testResultsTier = pw.IntegerField(null=True)
    timePoint = pw.TextField(null=True)
    timePointTier = pw.IntegerField(null=True)
    recordingDate = pw.TextField(null=True)
    recordingDateTier = pw.IntegerField(null=True)

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
