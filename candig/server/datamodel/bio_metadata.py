"""
Biodata objects
"""

import datetime
import json

import candig.server.datamodel as datamodel
import candig.server.exceptions as exceptions

import candig.schemas.protocol as protocol


class Biosample(datamodel.DatamodelObject):
    """
    This class represents an abstract Biosample object.
    It sets default values and getters, as well as the
    toProtocolElement function.
    """
    compoundIdClass = datamodel.BiosampleCompoundId

    def __init__(self, parentContainer, localId):
        super(Biosample, self).__init__(parentContainer, localId)
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._description = None
        self._disease = None
        self._name = localId
        self._individualId = None
        self._datasetId = parentContainer.getId()
        self._individualAgeAtCollection = None
        self._estimated_tumor_content = None
        self._normal_sample_source = None
        self._biopsy_data = None
        self._tumor_biopsy_anatomical_site = None
        self._biopsy_type = None
        self._sample_shipment_date = None

    def toProtocolElement(self, tier=0):
        disease = None
        if self.getDisease():
            disease = protocol.fromJson(
                json.dumps(self.getDisease()), protocol.OntologyTerm)
        individualAgeAtCollection = None
        if self.getIndividualAgeAtCollection():
            individualAgeAtCollection = protocol.fromJson(
                json.dumps(self.getIndividualAgeAtCollection()), protocol.Age)
        biosample = protocol.Biosample(
            dataset_id = self._datasetId,
            created = self.getCreated(),
            updated = self.getUpdated(),
            description = self.getDescription(),
            id = self.getId(),
            individual_id = self.getIndividualId(),
            name = self.getName(),
            disease = disease,
            individual_age_at_collection = individualAgeAtCollection,
            estimated_tumor_content = self.getEstimatedTumorContent(),
            normal_sample_source = self.getNormalSampleSource(),
            biopsy_data = self.getBiopsyData(),
            tumor_biopsy_anatomical_site = self.getTumorBiopsyAnatomicalSite(),
            biopsy_type = self.getBiopsyType(),
            sample_shipment_date = self.getSampleShipmentDate(),
        )
        self.serializeAttributes(biosample)
        return biosample

    def populateFromRow(self, biosampleRecord):
        # TODO coerce to types
        self._created = biosampleRecord.created
        self._updated = biosampleRecord.updated
        self._description = biosampleRecord.description
        self._disease = json.loads(biosampleRecord.disease)
        self._individualId = biosampleRecord.individualid
        self.setAttributesJson(biosampleRecord.attributes)
        self._individualAgeAtCollection = json.loads(
            biosampleRecord.individualAgeAtCollection)
        self._estimated_tumor_content = biosampleRecord.estimated_tumor_content
        self._normal_sample_source = biosampleRecord.normal_sample_source
        self._biopsy_data = biosampleRecord.biopsy_data
        self._tumor_biopsy_anatomical_site = biosampleRecord.tumor_biopsy_anatomical_site
        self._biopsy_type = biosampleRecord.biopsy_type
        self._sample_shipment_date = biosampleRecord.sample_shipment_date
        return self

    def populateFromJson(self, jsonString):
        try:
            parsed = protocol.fromJson(jsonString, protocol.Biosample)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._description = parsed.description
        self._disease = protocol.toJsonDict(parsed.disease)
        self._individualId = parsed.individual_id
        self._individualAgeAtCollection = protocol.toJsonDict(
            parsed.individual_age_at_collection)
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)
        self._estimated_tumor_content = parsed.estimated_tumor_content
        self._normal_sample_source = parsed.normal_sample_source
        self._biopsy_data = parsed.biopsy_data
        self._tumor_biopsy_anatomical_site = parsed.tumor_biopsy_anatomical_site
        self._biopsy_type = parsed.biopsy_type
        self._sample_shipment_date = parsed.sample_shipment_date
        return self

    def setIndividualId(self, individualId):
        self._individualId = individualId

    def getIndividualId(self):
        return self._individualId

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getDescription(self):
        return self._description

    def getDisease(self):
        if self._disease is not {}:
            return self._disease
        else:
            return None

    def getName(self):
        return self._name

    def getIndividualAgeAtCollection(self):
        if self._individualAgeAtCollection is not {}:
            return self._individualAgeAtCollection
        else:
            return None
        
    def getEstimatedTumorContent(self):
        return self._estimated_tumor_content

    def getNormalSampleSource(self):
        return self._normal_sample_source

    def getBiopsyData(self):
        return self._biopsy_data

    def getTumorBiopsyAnatomicalSite(self):
        return self._tumor_biopsy_anatomical_site

    def getBiopsyType(self):
        return self._biopsy_type

    def getSampleShipmentDate(self):
        return self._sample_shipment_date


class Experiment(datamodel.DatamodelObject):
    """
    This class represents an abstract Experiment object.
    It sets default values and getters, as well as the
    toProtocolElement function.
    """
    compoundIdClass = datamodel.ExperimentCompoundId

    def __init__(self, parentContainer, localId):
        super(Experiment, self).__init__(parentContainer, localId)
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._run_time = datetime.datetime.now().isoformat()
        self._molecule = None
        self._strategy = None
        self._selection = None
        self._library = None
        self._library_layout = None
        self._description = None
        self._instrument_model = None
        self._instrument_data_file = None
        self._sequencing_center = None
        self._platform_unit = None
        self._name = localId
        self._attributes = {}
        self._datasetId = parentContainer.getId()
        self._biosample_id = None
        self._dna_library_construction_method = None
        self._wgs_sequencing_completion_date = None
        self._rna_library_construction_method = None
        self._rna_sequencing_completion_date = None
        self._panel_completion_date = None

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def toProtocolElement(self, tier=0):
        experiment = protocol.Experiment(
            id = self.getId(),
            name = self.getName(),
            description = self.getDescription(),
            message_create_time = self.getCreated(),
            message_update_time = self.getUpdated(),
            run_time = self.getRunTime(),
            molecule = self.getMolecule(),
            strategy = self.getStrategy(),
            selection = self.getSelection(),
            library = self.getLibrary(),
            library_layout = self.getLibraryLayout(),
            instrument_model = self.getInstrumentModel(),
            instrument_data_file = self.getInstrumentDataFile(),
            sequencing_center = self.getSequencingCenter(),
            platform_unit = self.getPlatformUnit(),
            dataset_id = self._datasetId,
            biosample_id = self.getBiosampleId(),
            dna_library_construction_method = self.getDnaLibraryConstructionMethod(),
            wgs_sequencing_completion_date = self.getWgsSequencingCompletionDate(),
            rna_library_construction_method = self.getRnaLibraryConstructionMethod(),
            rna_sequencing_completion_date = self.getRnaSequencingCompletionDate(),
            panel_completion_date = self.getPanelCompletionDate(),
        )
        self.serializeAttributes(experiment)
        return experiment

    def populateFromRow(self, experimentRecord):
        # TODO coerce to types
        self._created = experimentRecord.created
        self._updated = experimentRecord.updated
        self._run_time = experimentRecord.runTime
        self._description = experimentRecord.description
        self._molecule = experimentRecord.molecule
        self._strategy = experimentRecord.strategy
        self._selection = experimentRecord.selection
        self._library = experimentRecord.library
        self._library_layout = experimentRecord.libraryLayout
        self._instrument_model = experimentRecord.instrumentModel
        self._instrument_data_file = experimentRecord.instrumentDataFile
        self._sequencing_center = experimentRecord.sequencingCenter
        self._platform_unit = experimentRecord.platformUnit
        self.setAttributesJson(experimentRecord.attributes)
        self._biosample_id = experimentRecord.biosample_id
        self._dna_library_construction_method = experimentRecord.dna_library_construction_method
        self._wgs_sequencing_completion_date = experimentRecord.wgs_sequencing_completion_date
        self._rna_library_construction_method = experimentRecord.rna_library_construction_method
        self._rna_sequencing_completion_date = experimentRecord.rna_sequencing_completion_date
        self._panel_completion_date = experimentRecord.panel_completion_date
        return self

    def populateFromJson(self, jsonString):
        try:
            parsed = protocol.fromJson(jsonString, protocol.Experiment)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        if parsed.message_create_time != "":
            self._created = parsed.message_create_time
        if parsed.message_update_time != "":
            self._updated = parsed.message_update_time
        self._run_time = parsed.run_time
        self._description = parsed.description
        self._molecule = parsed.molecule
        self._strategy = parsed.strategy
        self._selection = parsed.selection
        self._library = parsed.library
        self._library_layout = parsed.library_layout
        self._instrument_model = parsed.instrument_model
        self._instrument_data_file = parsed.instrument_data_file
        self._sequencing_center = parsed.sequencing_center
        self._platform_unit = parsed.platform_unit
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)
        self._biosample_id = parsed.biosample_id
        self._dna_library_construction_method = parsed.dna_library_construction_method
        self._wgs_sequencing_completion_date = parsed.wgs_sequencing_completion_date
        self._rna_library_construction_method = parsed.rna_library_construction_method
        self._rna_sequencing_completion_date = parsed.rna_sequencing_completion_date
        self._panel_completion_date = parsed.panel_completion_date
        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getRunTime(self):
        return self._run_time

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def getName(self):
        return self._name

    def getMolecule(self):
        return self._molecule

    def setMolecule(self, molecule):
        self._molecule = molecule

    def getStrategy(self):
        return self._strategy

    def getSelection(self):
        return self._selection

    def getLibrary(self):
        return self._library

    def getLibraryLayout(self):
        return self._library_layout

    def getInstrumentModel(self):
        return self._instrument_model

    def getInstrumentDataFile(self):
        return self._instrument_data_file

    def getSequencingCenter(self):
        return self._sequencing_center

    def setSequencingCenter(self, centre):
        self._sequencing_center = centre

    def getPlatformUnit(self):
        return self._platform_unit

    def getBiosampleId(self):
        return self._biosample_id

    def getDnaLibraryConstructionMethod(self):
        return self._dna_library_construction_method

    def getWgsSequencingCompletionDate(self):
        return self._wgs_sequencing_completion_date

    def getRnaLibraryConstructionMethod(self):
        return self._rna_library_construction_method

    def getRnaSequencingCompletionDate(self):
        return self._rna_sequencing_completion_date

    def getPanelCompletionDate(self):
        return self._panel_completion_date


class Analysis(datamodel.DatamodelObject):
    """
    This class represents an abstract Analysis object.
    It sets default values and getters, as well as the
    toProtocolElement function.
    """
    compoundIdClass = datamodel.AnalysisCompoundId

    def __init__(self, parentContainer, localId):
        super(Analysis, self).__init__(parentContainer, localId)
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._type = None
        self._software = []
        self._attributes = {}
        self._datasetId = parentContainer.getId()
        self._experiment_id = None
        self._other_analysis_descriptor = None
        self._other_analysis_completition_date = None

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def toProtocolElement(self, tier=0):
        analysis = protocol.Analysis(
            id=self.getId(),
            name=self.getName(),
            description=self.getDescription(),
            created=self.getCreated(),
            updated=self.getUpdated(),
            type=self.getAnalysisType(),
            dataset_id = self._datasetId,
            experiment_id = self.getExperimentId(),
            other_analysis_descriptor = self.getOtherAnalysisDescriptor(),
            other_analysis_completition_date = self.getOtherAnalysisCompletitionDate(),
        )
        analysis.software.extend(self.getSoftware())
        self.serializeAttributes(analysis)
        return analysis

    def populateFromRow(self, analysisRecord):
        # TODO coerce to types
        self._created = analysisRecord.created
        self._updated = analysisRecord.updated
        self._description = analysisRecord.description
        self._name = analysisRecord.name
        self._type = analysisRecord.analysistype
        self.setAttributesJson(analysisRecord.attributes)
        self._experiment_id = analysisRecord.experiment_id
        self._other_analysis_descriptor = analysisRecord.other_analysis_descriptor
        self._other_analysis_completition_date = analysisRecord.other_analysis_completition_date
        return self

    def populateFromJson(self, jsonString):
        try:
            parsed = protocol.fromJson(jsonString, protocol.Analysis)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        if parsed.created:
            self._created = parsed.created
        if parsed.updated:
            self._updated = parsed.updated
        self._description = parsed.description
#        if parsed.name:
#            self._name = parsed.name
        self._type = parsed.type
        self._software = parsed.software
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)
        self._experiment_id = parsed.experiment_id
        self._other_analysis_descriptor = parsed.other_analysis_descriptor
        self._other_analysis_completition_date = parsed.other_analysis_completition_date
        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getAnalysisType(self):
        return self._type

    def setAnalysisType(self, analysistype):
        self._type = analysistype

    def getSoftware(self):
        return self._software

    def setSoftware(self, software):
        self._type = software[:]

    def getPlatformUnit(self):
        return self._platform_unit

    def getExperimentId(self):
        return self._experiment_id

    def getOtherAnalysisDescriptor(self):
        return self._other_analysis_descriptor

    def getOtherAnalysisCompletitionDate(self):
        return self._other_analysis_completition_date


class Individual(datamodel.DatamodelObject):
    """
    This class represents an abstract Individual object.
    It sets default values and getters, as well as the
    toProtocolElement function.
    """
    compoundIdClass = datamodel.IndividualCompoundId

    def __init__(self, parentContainer, localId):
        super(Individual, self).__init__(parentContainer, localId)
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._description = None
        self._species = None
        self._sex = None
        self._name = localId
        self._datasetId = parentContainer.getId()
        self._patient_id = None
        self._regional_profiling_centre = None
        self._diagnosis = None
        self._pathology_type = None 
        self._enrollment_approval_date = None
        self._enrollment_approval_initials = None
        self._date_of_upload_to_sFTP = None
        self._tumor_board_presentation_date_and_analyses = None
        self._comments = None

    def toProtocolElement(self, tier=0):
        species = None
        sex = None
        if self.getSpecies():
            species = protocol.fromJson(
                json.dumps(self.getSpecies()), protocol.OntologyTerm)
        if self.getSex():
            sex = protocol.fromJson(
                json.dumps(self.getSex()), protocol.OntologyTerm)
        if self.getDiagnosis():
            diagnosis = protocol.fromJson(
                json.dumps(self.getDiagnosis()), protocol.OntologyTerm)
        else:
            diagnosis = None
        gaIndividual = protocol.Individual(
            dataset_id=self._datasetId,
            created=self.getCreated(),
            updated=self.getUpdated(),
            description=self.getDescription(),
            id=self.getId(),
            name=self.getName(),
            species=species,
            sex=sex,
            patient_id = self.getPatientId(),
            regional_profiling_centre = self.getRegionalProfilingCentre(),
            diagnosis = diagnosis,
            pathology_type = self.getPathologyType(),
            enrollment_approval_date = self.getEnrollmentApprovalDate(),
            enrollment_approval_initials = self.getEnrollmentApprovalInitials(),
            date_of_upload_to_sFTP = self.getDateOfUploadToSftp(),
            tumor_board_presentation_date_and_analyses = self.getTumorBoardPresentationDateAndAnalyses(),
            comments = self.getComments(),
        )
        self.serializeAttributes(gaIndividual)
        return gaIndividual

    def populateFromRow(self, individualRecord):
        # TODO coerce to types
        self._name = individualRecord.name
        self._created = individualRecord.created
        self._updated = individualRecord.updated
        self._description = individualRecord.description
        self._species = json.loads(individualRecord.species)
        self._sex = json.loads(individualRecord.sex)
        self.setAttributesJson(individualRecord.attributes)
        self._patient_id = individualRecord.patient_id
        self._regional_profiling_centre = individualRecord.regional_profiling_centre
        self._diagnosis = json.loads(individualRecord.diagnosis)
        self._pathology_type = individualRecord.pathology_type
        self._enrollment_approval_date = individualRecord.enrollment_approval_date
        self._enrollment_approval_initials = individualRecord.enrollment_approval_initials
        self._date_of_upload_to_sFTP = individualRecord.date_of_upload_to_sFTP
        self._tumor_board_presentation_date_and_analyses = individualRecord.tumor_board_presentation_date_and_analyses
        self._comments = individualRecord.comments
        return self

    def populateFromJson(self, jsonString):
        # TODO validate
        try:
            parsed = protocol.fromJson(jsonString, protocol.Individual)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._description = parsed.description
        self._species = protocol.toJsonDict(parsed.species)
        self._sex = protocol.toJsonDict(parsed.sex)
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)
        self._patient_id = parsed.patient_id
        self._regional_profiling_centre = parsed.regional_profiling_centre
        self._diagnosis = json.dumps(protocol.toJsonDict(parsed.diagnosis))
        self._pathology_type = parsed.pathology_type
        self._enrollment_approval_date = parsed.enrollment_approval_date
        self._enrollment_approval_initials = parsed.enrollment_approval_initials
        self._date_of_upload_to_sFTP = parsed.date_of_upload_to_sFTP
        self._tumor_board_presentation_date_and_analyses = parsed.tumor_board_presentation_date_and_analyses
        self._comments = parsed.comments
        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getDescription(self):
        return self._description

    def getSpecies(self):
        return self._species

    def getSex(self):
        return self._sex

    def getName(self):
        return self._name
        
    def getPatientId(self):
        return self._patient_id

    def getRegionalProfilingCentre(self):
        return self._regional_profiling_centre

    def getDiagnosis(self):
        return self._diagnosis

    def getPathologyType(self):
        return self._pathology_type

    def getEnrollmentApprovalDate(self):
        return self._enrollment_approval_date

    def getEnrollmentApprovalInitials(self):
        return self._enrollment_approval_initials

    def getDateOfUploadToSftp(self):
        return self._date_of_upload_to_sFTP

    def getTumorBoardPresentationDateAndAnalyses(self):
        return self._tumor_board_presentation_date_and_analyses

    def getComments(self):
        return self._comments
