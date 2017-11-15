"""
Biodata objects
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import json

import ga4gh.server.datamodel as datamodel
import ga4gh.server.exceptions as exceptions

import ga4gh.schemas.protocol as protocol


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

    def toProtocolElement(self):
        disease = None
        if self.getDisease():
            disease = protocol.fromJson(
                json.dumps(self.getDisease()), protocol.OntologyTerm)
        individualAgeAtCollection = None
        if self.getIndividualAgeAtCollection():
            individualAgeAtCollection = protocol.fromJson(
                json.dumps(self.getIndividualAgeAtCollection()), protocol.Age)
        biosample = protocol.Biosample(
            dataset_id=self._datasetId,
            created=self.getCreated(),
            updated=self.getUpdated(),
            description=self.getDescription(),
            id=self.getId(),
            individual_id=self.getIndividualId(),
            name=self.getName(),
            disease=disease,
            individual_age_at_collection=individualAgeAtCollection)
        self.serializeAttributes(biosample)
        return biosample

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
        return self

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


class Experiment(datamodel.DatamodelObject):
    """
    This class represents an abstract Experiment object.
    It sets default values and getters, as well as the
    toProtocolElement function.
    """
    compoundIdClass = datamodel.ExperimentCompoundId

    def __init__(self, localId):
        super(Experiment, self).__init__(None, localId)
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

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def toProtocolElement(self):
        experiment = protocol.Experiment(
            id=self.getId(),
            name=self.getName(),
            description=self.getDescription(),
            message_create_time=self.getCreated(),
            message_update_time=self.getUpdated(),
            run_time=self.getRunTime(),
            molecule=self.getMolecule(),
            strategy=self.getStrategy(),
            selection=self.getSelection(),
            library=self.getLibrary(),
            library_layout=self.getLibraryLayout(),
            instrument_model=self.getInstrumentModel(),
            instrument_data_file=self.getInstrumentDataFile(),
            sequencing_center=self.getSequencingCenter(),
            platform_unit=self.getPlatformUnit(),
            )
        self.serializeAttributes(experiment)
        return experiment

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
        return self

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


class Analysis(datamodel.DatamodelObject):
    """
    This class represents an abstract Analysis object.
    It sets default values and getters, as well as the
    toProtocolElement function.
    """
    compoundIdClass = datamodel.AnalysisCompoundId

    def __init__(self, localId):
        super(Analysis, self).__init__(None, localId)
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._type = None
        self._software = []
        self._attributes = {}

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def toProtocolElement(self):
        analysis = protocol.Analysis(
            id=self.getId(),
            name=self.getName(),
            description=self.getDescription(),
            created=self.getCreated(),
            updated=self.getUpdated(),
            type=self.getAnalysisType())
        analysis.software.extend(self.getSoftware())
        self.serializeAttributes(analysis)
        return analysis

    def populateFromJson(self, jsonString):
        try:
            parsed = protocol.fromJson(jsonString, protocol.Analysis)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        if parsed.created != "":
            self._created = parsed.created
        if parsed.updated != "":
            self._updated = parsed.updated
        self._description = parsed.description
        self._name = parsed.name
        self._type = parsed.type
        self._software = parsed.software
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
        self.setAttributes(attributes)
        return self

    def populateFromRow(self, analysisRecord):
        # TODO coerce to types
        self._created = analysisRecord.created
        self._updated = analysisRecord.updated
        self._description = analysisRecord.description
        self._name = analysisRecord.name
        self._type = analysisRecord.analysistype
        self.setAttributesJson(analysisRecord.attributes)
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

    def toProtocolElement(self):
        species = None
        sex = None
        if self.getSpecies():
            species = protocol.fromJson(
                json.dumps(self.getSpecies()), protocol.OntologyTerm)
        if self.getSex():
            sex = protocol.fromJson(
                json.dumps(self.getSex()), protocol.OntologyTerm)
        gaIndividual = protocol.Individual(
            dataset_id=self._datasetId,
            created=self.getCreated(),
            updated=self.getUpdated(),
            description=self.getDescription(),
            id=self.getId(),
            name=self.getName(),
            species=species,
            sex=sex)
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
