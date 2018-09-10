"""
Dataset objects
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ga4gh.server.datamodel as datamodel
import ga4gh.server.datamodel.reads as reads
import ga4gh.server.datamodel.sequence_annotations as sequence_annotations
import ga4gh.server.datamodel.continuous as continuous
import ga4gh.server.datamodel.variants as variants
import ga4gh.server.exceptions as exceptions
import ga4gh.server.datamodel.bio_metadata as biodata
import ga4gh.server.datamodel.genotype_phenotype as g2p
import ga4gh.server.datamodel.rna_quantification as rnaQuantification

import ga4gh.schemas.pb as pb
import ga4gh.schemas.protocol as protocol


class Dataset(datamodel.DatamodelObject):
    """
    The base class of datasets containing variants and reads
    """
    compoundIdClass = datamodel.DatasetCompoundId

    def __init__(self, localId):
        super(Dataset, self).__init__(None, localId)
        self._description = None
        self._variantSetIds = []
        self._variantSetIdMap = {}
        self._variantSetNameMap = {}
        self._featureSetIds = []
        self._featureSetIdMap = {}
        self._featureSetNameMap = {}
        self._continuousSetIds = []
        self._continuousSetIdMap = {}
        self._continuousSetNameMap = {}
        self._readGroupSetIds = []
        self._readGroupSetIdMap = {}
        self._readGroupSetNameMap = {}
        self._biosampleIds = []
        self._biosampleIdMap = {}
        self._biosampleNameMap = {}
        self._individualIds = []
        self._individualIdMap = {}
        self._individualNameMap = {}
        self._phenotypeAssociationSetIdMap = {}
        self._phenotypeAssociationSetNameMap = {}
        self._phenotypeAssociationSetIds = []
        self._rnaQuantificationSetIds = []
        self._rnaQuantificationSetIdMap = {}
        self._rnaQuantificationSetNameMap = {}
### ======================================================================= ###
### METADATA
### ======================================================================= ###
        # Patient
        self._patientIds = []
        self._patientIdMap = {}
        self._patientNameMap = {}

        # Enrollment
        self._enrollmentIds = []
        self._enrollmentIdMap = {}
        self._enrollmentNameMap = {}

        # Consent
        self._consentIds = []
        self._consentIdMap = {}
        self._consentNameMap = {}

        # Diagnosis
        self._diagnosisIds = []
        self._diagnosisIdMap = {}
        self._diagnosisNameMap = {}

        # Sample
        self._sampleIds = []
        self._sampleIdMap = {}
        self._sampleNameMap = {}

        # Treatment
        self._treatmentIds = []
        self._treatmentIdMap = {}
        self._treatmentNameMap = {}

        # Outcome
        self._outcomeIds = []
        self._outcomeIdMap = {}
        self._outcomeNameMap = {}

        # Complication
        self._complicationIds = []
        self._complicationIdMap = {}
        self._complicationNameMap = {}

        # Tumourboard
        self._tumourboardIds = []
        self._tumourboardIdMap = {}
        self._tumourboardNameMap = {}

        # Extraction
        self._extractionIds = []
        self._extractionIdMap = {}
        self._extractionNameMap = {}

        # Sequencing
        self._sequencingIds = []
        self._sequencingIdMap = {}
        self._sequencingNameMap = {}

        # Alignment
        self._alignmentIds = []
        self._alignmentIdMap = {}
        self._alignmentNameMap = {}

        # VariantCalling
        self._variantCallingIds = []
        self._variantCallingIdMap = {}
        self._variantCallingNameMap = {}

        # FusionDetection
        self._fusionDetectionIds = []
        self._fusionDetectionIdMap = {}
        self._fusionDetectionNameMap = {}

        # Extraction
        self._expressionAnalysisIds = []
        self._expressionAnalysisIdMap = {}
        self._expressionAnalysisNameMap = {}
### ======================================================================= ###
### METADATA END
### ======================================================================= ###

    def populateFromRow(self, dataset):
        """
        Populates the instance variables of this Dataset from the
        specified database row.
        """
        self._description = dataset.description
        self.setAttributesJson(dataset.attributes)

    def setDescription(self, description):
        """
        Sets the description for this dataset to the specified value.
        """
        self._description = description

    def addVariantSet(self, variantSet):
        """
        Adds the specified variantSet to this dataset.
        """
        id_ = variantSet.getId()
        self._variantSetIdMap[id_] = variantSet
        self._variantSetNameMap[variantSet.getLocalId()] = variantSet
        self._variantSetIds.append(id_)

    def addBiosample(self, biosample):
        """
        Adds the specified biosample to this dataset.
        """
        id_ = biosample.getId()
        self._biosampleIdMap[id_] = biosample
        self._biosampleIds.append(id_)
        self._biosampleNameMap[biosample.getName()] = biosample

    def addIndividual(self, individual):
        """
        Adds the specified individual to this dataset.
        """
        id_ = individual.getId()
        self._individualIdMap[id_] = individual
        self._individualIds.append(id_)
        self._individualNameMap[individual.getName()] = individual

### ======================================================================= ###
### METADATA
### ======================================================================= ###
    def addPatient(self, patient):
        """
        Adds the specified patient to this dataset.
        """
        id_ = patient.getId()
        self._patientIdMap[id_] = patient
        self._patientIds.append(id_)
        self._patientNameMap[patient.getName()] = patient

    def addEnrollment(self, enrollment):
        """
        Adds the specified enrollment to this dataset.
        """
        id_ = enrollment.getId()
        self._enrollmentIdMap[id_] = enrollment
        self._enrollmentIds.append(id_)
        self._enrollmentNameMap[enrollment.getName()] = enrollment

    def addConsent(self, consent):
        """
        Adds the specified consent to this dataset.
        """
        id_ = consent.getId()
        self._consentIdMap[id_] = consent
        self._consentIds.append(id_)
        self._consentNameMap[consent.getName()] = consent

    def addDiagnosis(self, diagnosis):
        """
        Adds the specified diagnosis to this dataset.
        """
        id_ = diagnosis.getId()
        self._diagnosisIdMap[id_] = diagnosis
        self._diagnosisIds.append(id_)
        self._diagnosisNameMap[diagnosis.getName()] = diagnosis

    def addSample(self, sample):
        """
        Adds the specified sample to this dataset.
        """
        id_ = sample.getId()
        self._sampleIdMap[id_] = sample
        self._sampleIds.append(id_)
        self._sampleNameMap[sample.getName()] = sample

    def addTreatment(self, treatment):
        """
        Adds the specified treatment to this dataset.
        """
        id_ = treatment.getId()
        self._treatmentIdMap[id_] = treatment
        self._treatmentIds.append(id_)
        self._treatmentNameMap[treatment.getName()] = treatment

    def addOutcome(self, outcome):
        """
        Adds the specified outcome to this dataset.
        """
        id_ = outcome.getId()
        self._outcomeIdMap[id_] = outcome
        self._outcomeIds.append(id_)
        self._outcomeNameMap[outcome.getName()] = outcome

    def addComplication(self, complication):
        """
        Adds the specified complication to this dataset.
        """
        id_ = complication.getId()
        self._complicationIdMap[id_] = complication
        self._complicationIds.append(id_)
        self._complicationNameMap[complication.getName()] = complication

    def addTumourboard(self, tumourboard):
        """
        Adds the specified tumourboard to this dataset.
        """
        id_ = tumourboard.getId()
        self._tumourboardIdMap[id_] = tumourboard
        self._tumourboardIds.append(id_)
        self._tumourboardNameMap[tumourboard.getName()] = tumourboard

    def addExtraction(self, extraction):
        """
        Adds the specified extraction to this dataset.
        """
        id_ = extraction.getId()
        self._extractionIdMap[id_] = extraction
        self._extractionIds.append(id_)
        self._extractionNameMap[extraction.getName()] = extraction

    def addSequencing(self, sequencing):
        """
        Adds the specified extraction to this dataset.
        """
        id_ = sequencing.getId()
        self._extractionIdMap[id_] = sequencing
        self._extractionIds.append(id_)
        self._extractionNameMap[sequencing.getName()] = sequencing

    def addAlignment(self, alignment):
        """
        Adds the specified extraction to this dataset.
        """
        id_ = alignment.getId()
        self._extractionIdMap[id_] = alignment
        self._extractionIds.append(id_)
        self._extractionNameMap[alignment.getName()] = alignment

    def addVariantCalling(self, variantCalling):
        """
        Adds the specified extraction to this dataset.
        """
        id_ = variantCalling.getId()
        self._extractionIdMap[id_] = variantCalling
        self._extractionIds.append(id_)
        self._extractionNameMap[variantCalling.getName()] = variantCalling

    def addFusionDetection(self, fusionDetection):
        """
        Adds the specified extraction to this dataset.
        """
        id_ = fusionDetection.getId()
        self._extractionIdMap[id_] = fusionDetection
        self._extractionIds.append(id_)
        self._extractionNameMap[fusionDetection.getName()] = fusionDetection

    def addExpressionAnalysis(self, expressionAnalysis):
        """
        Adds the specified extraction to this dataset.
        """
        id_ = expressionAnalysis.getId()
        self._extractionIdMap[id_] = expressionAnalysis
        self._extractionIds.append(id_)
        self._extractionNameMap[expressionAnalysis.getName()] = expressionAnalysis

### ======================================================================= ###
### METADATA END
### ======================================================================= ###

    def addFeatureSet(self, featureSet):
        """
        Adds the specified featureSet to this dataset.
        """
        id_ = featureSet.getId()
        self._featureSetIdMap[id_] = featureSet
        self._featureSetIds.append(id_)
        name = featureSet.getLocalId()
        self._featureSetNameMap[name] = featureSet

    def addContinuousSet(self, continuousSet):
        """
        Adds the specified continuousSet to this dataset.
        """
        id_ = continuousSet.getId()
        self._continuousSetIdMap[id_] = continuousSet
        self._continuousSetIds.append(id_)
        name = continuousSet.getLocalId()
        self._continuousSetNameMap[name] = continuousSet

    def addReadGroupSet(self, readGroupSet):
        """
        Adds the specified readGroupSet to this dataset.
        """
        id_ = readGroupSet.getId()
        self._readGroupSetIdMap[id_] = readGroupSet
        self._readGroupSetNameMap[readGroupSet.getLocalId()] = readGroupSet
        self._readGroupSetIds.append(id_)

    def addRnaQuantificationSet(self, rnaQuantSet):
        """
        Adds the specified rnaQuantification set to this dataset.
        """
        id_ = rnaQuantSet.getId()
        self._rnaQuantificationSetIdMap[id_] = rnaQuantSet
        self._rnaQuantificationSetIds.append(id_)
        name = rnaQuantSet.getLocalId()
        self._rnaQuantificationSetNameMap[name] = rnaQuantSet

    def toProtocolElement(self, tier=0):
        dataset = protocol.Dataset()
        dataset.id = self.getId()
        dataset.name = pb.string(self.getLocalId())
        dataset.description = pb.string(self.getDescription())
        self.serializeAttributes(dataset)
        return dataset

    def getVariantSets(self):
        """
        Returns the list of VariantSets in this dataset
        """
        return [self._variantSetIdMap[id_] for id_ in self._variantSetIds]

    def getNumVariantSets(self):
        """
        Returns the number of variant sets in this dataset.
        """
        return len(self._variantSetIds)

    def getVariantSet(self, id_):
        """
        Returns the VariantSet with the specified name, or raises a
        VariantSetNotFoundException otherwise.
        """
        if id_ not in self._variantSetIdMap:
            raise exceptions.VariantSetNotFoundException(id_)
        return self._variantSetIdMap[id_]

    def getVariantSetByIndex(self, index):
        """
        Returns the variant set at the specified index in this dataset.
        """
        return self._variantSetIdMap[self._variantSetIds[index]]

    def getVariantSetByName(self, name):
        """
        Returns a VariantSet with the specified name, or raises a
        VariantSetNameNotFoundException if it does not exist.
        """
        if name not in self._variantSetNameMap:
            raise exceptions.VariantSetNameNotFoundException(name)
        return self._variantSetNameMap[name]

    def addPhenotypeAssociationSet(self, phenotypeAssociationSet):
        """
        Adds the specified g2p association set to this backend.
        """
        id_ = phenotypeAssociationSet.getId()
        self._phenotypeAssociationSetIdMap[id_] = phenotypeAssociationSet
        self._phenotypeAssociationSetNameMap[
            phenotypeAssociationSet.getLocalId()] = phenotypeAssociationSet
        self._phenotypeAssociationSetIds.append(id_)

    def getPhenotypeAssociationSets(self):
        return [self._phenotypeAssociationSetIdMap[id_]
                for id_ in self._phenotypeAssociationSetIdMap]

    def getPhenotypeAssociationSet(self, id_):
        return self._phenotypeAssociationSetIdMap[id_]

    def getPhenotypeAssociationSetByName(self, name):
        if name not in self._phenotypeAssociationSetNameMap:
            raise exceptions.PhenotypeAssociationSetNotFoundException(name)
        return self._phenotypeAssociationSetNameMap[name]

    def getPhenotypeAssociationSetByIndex(self, index):
        return self._phenotypeAssociationSetIdMap[
            self._phenotypeAssociationSetIds[index]]

    def getNumPhenotypeAssociationSets(self):
        """
        Returns the number of reference sets in this data repository.
        """
        return len(self._phenotypeAssociationSetIds)

    def getFeatureSets(self):
        """
        Returns the list of FeatureSets in this dataset
        """
        return [self._featureSetIdMap[id_] for id_ in self._featureSetIds]

    def getNumFeatureSets(self):
        """
        Returns the number of feature sets in this dataset.
        """
        return len(self._featureSetIds)

    def getFeatureSet(self, id_):
        """
        Returns the FeatureSet with the specified id, or raises a
        FeatureSetNotFoundException otherwise.
        """
        if id_ not in self._featureSetIdMap:
            raise exceptions.FeatureSetNotFoundException(id_)
        return self._featureSetIdMap[id_]

    def getFeatureSetByName(self, name):
        """
        Returns the FeatureSet with the specified name, or raises
        an exception otherwise.
        """
        if name not in self._featureSetNameMap:
            raise exceptions.FeatureSetNameNotFoundException(name)
        return self._featureSetNameMap[name]

    def getFeatureSetByIndex(self, index):
        """
        Returns the feature set at the specified index in this dataset.
        """
        return self._featureSetIdMap[self._featureSetIds[index]]

    def getContinuousSets(self):
        """
        Returns the list of ContinuousSets in this dataset
        """
        return [self._continuousSetIdMap[id_]
                for id_ in self._continuousSetIds]

    def getNumContinuousSets(self):
        """
        Returns the number of continuous sets in this dataset.
        """
        return len(self._continuousSetIds)

    def getContinuousSet(self, id_):
        """
        Returns the ContinuousSet with the specified id, or raises a
        ContinuousSetNotFoundException otherwise.
        """
        if id_ not in self._continuousSetIdMap:
            raise exceptions.ContinuousSetNotFoundException(id_)
        return self._continuousSetIdMap[id_]

    def getContinuousSetByName(self, name):
        """
        Returns the ContinuousSet with the specified name, or raises
        an exception otherwise.
        """
        if name not in self._continuousSetNameMap:
            raise exceptions.ContinuousSetNameNotFoundException(name)
        return self._continuousSetNameMap[name]

    def getContinuousSetByIndex(self, index):
        """
        Returns the continuous set at the specified index in this dataset.
        """
        return self._continuousSetIdMap[self._continuousSetIds[index]]

    def getBiosamples(self):
        """
        Returns the list of biosamples in this dataset
        """
        return [self._biosampleIdMap[id_] for id_ in self._biosampleIds]

    def getBiosampleByName(self, name):
        """
        Returns a Biosample with the specified name, or raises a
        BiosampleNameNotFoundException if it does not exist.
        """
        if name not in self._biosampleNameMap:
            raise exceptions.BiosampleNameNotFoundException(name)
        return self._biosampleNameMap[name]

    def getBiosample(self, id_):
        """
        Returns the Biosample with the specified id, or raises
        a BiosampleNotFoundException otherwise.
        """
        if id_ not in self._biosampleIdMap:
            raise exceptions.BiosampleNotFoundException(id_)
        return self._biosampleIdMap[id_]

    def getIndividuals(self):
        """
        Returns the list of individuals in this dataset
        """
        return [self._individualIdMap[id_] for id_ in self._individualIds]

    def getIndividualByName(self, name):
        """
        Returns an individual with the specified name, or raises a
        IndividualNameNotFoundException if it does not exist.
        """
        if name not in self._individualNameMap:
            raise exceptions.IndividualNameNotFoundException(name)
        return self._individualNameMap[name]

    def getIndividual(self, id_):
        """
        Returns the Individual with the specified id, or raises
        a IndividualNotFoundException otherwise.
        """
        if id_ not in self._individualIdMap:
            raise exceptions.IndividualNotFoundException(id_)
        return self._individualIdMap[id_]

### ======================================================================= ###
### METADATA
### ======================================================================= ###
    def getPatients(self):
        """
        Returns the list of patients in this dataset
        """
        return [self._patientIdMap[id_] for id_ in self._patientIds]

    def getPatientByName(self, name):
        """
        Returns an patient with the specified name, or raises a
        PatientNameNotFoundException if it does not exist.
        """
        if name not in self._patientNameMap:
            raise exceptions.PatientNameNotFoundException(name)
        return self._patientNameMap[name]

    def getPatient(self, id_):
        """
        Returns the Patient with the specified id, or raises
        a PatientNotFoundException otherwise.
        """
        if id_ not in self._patientIdMap:
            raise exceptions.PatientNotFoundException(id_)
        return self._patientIdMap[id_]

    def getEnrollments(self):
        """
        Returns the list of enrollments in this dataset
        """
        return [self._enrollmentIdMap[id_] for id_ in self._enrollmentIds]

    def getEnrollmentByName(self, name):
        """
        Returns an enrollment with the specified name, or raises a
        EnrollmentNameNotFoundException if it does not exist.
        """
        if name not in self._enrollmentNameMap:
            raise exceptions.EnrollmentNameNotFoundException(name)
        return self._enrollmentNameMap[name]

    def getEnrollment(self, id_):
        """
        Returns the Enrollment with the specified id, or raises
        a EnrollmentNotFoundException otherwise.
        """
        if id_ not in self._enrollmentIdMap:
            raise exceptions.EnrollmentNotFoundException(id_)
        return self._enrollmentIdMap[id_]

    def getConsents(self):
        """
        Returns the list of consents in this dataset
        """
        return [self._consentIdMap[id_] for id_ in self._consentIds]

    def getConsentByName(self, name):
        """
        Returns an consent with the specified name, or raises a
        ConsentNameNotFoundException if it does not exist.
        """
        if name not in self._consentNameMap:
            raise exceptions.ConsentNameNotFoundException(name)
        return self._consentNameMap[name]

    def getConsent(self, id_):
        """
        Returns the Consent with the specified id, or raises
        a ConsentNotFoundException otherwise.
        """
        if id_ not in self._consentIdMap:
            raise exceptions.ConsentNotFoundException(id_)
        return self._consentIdMap[id_]

    def getDiagnoses(self):
        """
        Returns the list of diagnoses in this dataset
        """
        return [self._diagnosisIdMap[id_] for id_ in self._diagnosisIds]

    def getDiagnosisByName(self, name):
        """
        Returns an diagnosis with the specified name, or raises a
        DiagnosisNameNotFoundException if it does not exist.
        """
        if name not in self._diagnosisNameMap:
            raise exceptions.DiagnosisNameNotFoundException(name)
        return self._diagnosisNameMap[name]

    def getDiagnosis(self, id_):
        """
        Returns the Diagnosis with the specified id, or raises
        a DiagnosisNotFoundException otherwise.
        """
        if id_ not in self._diagnosisIdMap:
            raise exceptions.DiagnosisNotFoundException(id_)
        return self._diagnosisIdMap[id_]

    def getSamples(self):
        """
        Returns the list of samples in this dataset
        """
        return [self._sampleIdMap[id_] for id_ in self._sampleIds]

    def getSampleByName(self, name):
        """
        Returns an sample with the specified name, or raises a
        SampleNameNotFoundException if it does not exist.
        """
        if name not in self._sampleNameMap:
            raise exceptions.SampleNameNotFoundException(name)
        return self._sampleNameMap[name]

    def getSample(self, id_):
        """
        Returns the Sample with the specified id, or raises
        a SampleNotFoundException otherwise.
        """
        if id_ not in self._sampleIdMap:
            raise exceptions.SampleNotFoundException(id_)
        return self._sampleIdMap[id_]

    def getTreatments(self):
        """
        Returns the list of treatments in this dataset
        """
        return [self._treatmentIdMap[id_] for id_ in self._treatmentIds]

    def getTreatmentByName(self, name):
        """
        Returns an treatment with the specified name, or raises a
        TreatmentNameNotFoundException if it does not exist.
        """
        if name not in self._treatmentNameMap:
            raise exceptions.TreatmentNameNotFoundException(name)
        return self._treatmentNameMap[name]

    def getTreatment(self, id_):
        """
        Returns the Treatment with the specified id, or raises
        a TreatmentNotFoundException otherwise.
        """
        if id_ not in self._treatmentIdMap:
            raise exceptions.TreatmentNotFoundException(id_)
        return self._treatmentIdMap[id_]

    def getOutcomes(self):
        """
        Returns the list of outcomes in this dataset
        """
        return [self._outcomeIdMap[id_] for id_ in self._outcomeIds]

    def getOutcomeByName(self, name):
        """
        Returns an outcome with the specified name, or raises a
        OutcomeNameNotFoundException if it does not exist.
        """
        if name not in self._outcomeNameMap:
            raise exceptions.OutcomeNameNotFoundException(name)
        return self._outcomeNameMap[name]

    def getOutcome(self, id_):
        """
        Returns the Outcome with the specified id, or raises
        a OutcomeNotFoundException otherwise.
        """
        if id_ not in self._outcomeIdMap:
            raise exceptions.OutcomeNotFoundException(id_)
        return self._outcomeIdMap[id_]

    def getComplications(self):
        """
        Returns the list of complications in this dataset
        """
        return [self._complicationIdMap[id_] for id_ in self._complicationIds]

    def getComplicationByName(self, name):
        """
        Returns an complication with the specified name, or raises a
        ComplicationNameNotFoundException if it does not exist.
        """
        if name not in self._complicationNameMap:
            raise exceptions.ComplicationNameNotFoundException(name)
        return self._complicationNameMap[name]

    def getComplication(self, id_):
        """
        Returns the Complication with the specified id, or raises
        a ComplicationNotFoundException otherwise.
        """
        if id_ not in self._complicationIdMap:
            raise exceptions.ComplicationNotFoundException(id_)
        return self._complicationIdMap[id_]

    def getTumourboards(self):
        """
        Returns the list of tumourboards in this dataset
        """
        return [self._tumourboardIdMap[id_] for id_ in self._tumourboardIds]

    def getTumourboardByName(self, name):
        """
        Returns an tumourboard with the specified name, or raises a
        TumourboardNameNotFoundException if it does not exist.
        """
        if name not in self._tumourboardNameMap:
            raise exceptions.TumourboardNameNotFoundException(name)
        return self._tumourboardNameMap[name]

    def getTumourboard(self, id_):
        """
        Returns the Tumourboard with the specified id, or raises
        a TumourboardNotFoundException otherwise.
        """
        if id_ not in self._tumourboardIdMap:
            raise exceptions.TumourboardNotFoundException(id_)
        return self._tumourboardIdMap[id_]

    def getExtractions(self):
        """
        Returns the list of extractions in this dataset
        """
        return [self._extractionIdMap[id_] for id_ in self._extractionIds]

    def getExtractionByName(self, name):
        """
        Returns an extraction with the specified name, or raises a
        extractionNameNotFoundException if it does not exist.
        """
        if name not in self._extractionNameMap:
            raise exceptions.ObjectNameNotFoundException(name)
        return self._extractionNameMap[name]

    def getExtraction(self, id_):
        """
        Returns the extraction with the specified id, or raises
        a extractionNotFoundException otherwise.
        """
        if id_ not in self._extractionIdMap:
            raise exceptions.ObjectNotFoundException(id_)
        return self._extractionIdMap[id_]

    def getSequencings(self):
        """
        Returns the list of sequencings in this dataset
        """
        return [self._sequencingIdMap[id_] for id_ in self._sequencingIds]

    def getSequencingByName(self, name):
        """
        Returns an sequencing with the specified name, or raises a
        sequencingNameNotFoundException if it does not exist.
        """
        if name not in self._sequencingNameMap:
            raise exceptions.ObjectNameNotFoundException(name)
        return self._sequencingNameMap[name]

    def getSequencing(self, id_):
        """
        Returns the sequencing with the specified id, or raises
        a sequencingNotFoundException otherwise.
        """
        if id_ not in self._sequencingIdMap:
            raise exceptions.ObjectNotFoundException(id_)
        return self._sequencingIdMap[id_]

    def getAlignments(self):
        """
        Returns the list of alignments in this dataset
        """
        return [self._alignmentIdMap[id_] for id_ in self._alignmentIds]

    def getAlignmentByName(self, name):
        """
        Returns an alignment with the specified name, or raises a
        alignmentNameNotFoundException if it does not exist.
        """
        if name not in self._alignmentNameMap:
            raise exceptions.ObjectNameNotFoundException(name)
        return self._alignmentNameMap[name]

    def getAlignment(self, id_):
        """
        Returns the alignment with the specified id, or raises
        a alignmentNotFoundException otherwise.
        """
        if id_ not in self._alignmentIdMap:
            raise exceptions.ObjectNotFoundException(id_)
        return self._alignmentIdMap[id_]

    def getVariantCallings(self):
        """
        Returns the list of variantCallings in this dataset
        """
        return [self._variantCallingIdMap[id_] for id_ in self._variantCallingIds]

    def getVariantCallingByName(self, name):
        """
        Returns an variantCalling with the specified name, or raises a
        variantCallingNameNotFoundException if it does not exist.
        """
        if name not in self._variantCallingNameMap:
            raise exceptions.ObjectNameNotFoundException(name)
        return self._variantCallingNameMap[name]

    def getVariantCalling(self, id_):
        """
        Returns the variantCalling with the specified id, or raises
        a variantCallingNotFoundException otherwise.
        """
        if id_ not in self._variantCallingIdMap:
            raise exceptions.ObjectNotFoundException(id_)
        return self._variantCallingIdMap[id_]

    def getFusionDetections(self):
        """
        Returns the list of fusionDetections in this dataset
        """
        return [self._fusionDetectionIdMap[id_] for id_ in self._fusionDetectionIds]

    def getFusionDetectionByName(self, name):
        """
        Returns an fusionDetection with the specified name, or raises a
        fusionDetectionNameNotFoundException if it does not exist.
        """
        if name not in self._fusionDetectionNameMap:
            raise exceptions.ObjectNameNotFoundException(name)
        return self._fusionDetectionNameMap[name]

    def getFusionDetection(self, id_):
        """
        Returns the fusionDetection with the specified id, or raises
        a fusionDetectionNotFoundException otherwise.
        """
        if id_ not in self._fusionDetectionIdMap:
            raise exceptions.ObjectNotFoundException(id_)
        return self._fusionDetectionIdMap[id_]

    def getExpressionAnalyses(self):
        """
        Returns the list of expressionAnalyses in this dataset
        """
        return [self._expressionAnalysisIdMap[id_] for id_ in self._expressionAnalysisIds]

    def getExpressionAnalysisByName(self, name):
        """
        Returns an expressionAnalysis with the specified name, or raises a
        expressionAnalysisNameNotFoundException if it does not exist.
        """
        if name not in self._expressionAnalysisNameMap:
            raise exceptions.ObjectNameNotFoundException(name)
        return self._expressionAnalysisNameMap[name]

    def getExpressionAnalysis(self, id_):
        """
        Returns the expressionAnalysis with the specified id, or raises
        a expressionAnalysisNotFoundException otherwise.
        """
        if id_ not in self._expressionAnalysisIdMap:
            raise exceptions.ObjectNotFoundException(id_)
        return self._expressionAnalysisIdMap[id_]
### ======================================================================= ###
### METADATA END
### ======================================================================= ###

    def getNumReadGroupSets(self):
        """
        Returns the number of readgroup sets in this dataset.
        """
        return len(self._readGroupSetIds)

    def getReadGroupSets(self):
        """
        Returns the list of ReadGroupSets in this dataset
        """
        return [self._readGroupSetIdMap[id_] for id_ in self._readGroupSetIds]

    def getReadGroupSetByName(self, name):
        """
        Returns a ReadGroupSet with the specified name, or raises a
        ReadGroupSetNameNotFoundException if it does not exist.
        """
        if name not in self._readGroupSetNameMap:
            raise exceptions.ReadGroupSetNameNotFoundException(name)
        return self._readGroupSetNameMap[name]

    def getReadGroupSetByIndex(self, index):
        """
        Returns the readgroup set at the specified index in this dataset.
        """
        return self._readGroupSetIdMap[self._readGroupSetIds[index]]

    def getReadGroupSet(self, id_):
        """
        Returns the ReadGroupSet with the specified name, or raises
        a ReadGroupSetNotFoundException otherwise.
        """
        if id_ not in self._readGroupSetIdMap:
            raise exceptions.ReadGroupNotFoundException(id_)
        return self._readGroupSetIdMap[id_]

    def getInfo(self):
        """
        Returns the info of this dataset.
        """
        return self._info

    def getDescription(self):
        """
        Returns the free text description of this dataset.
        """
        return self._description

    def getNumRnaQuantificationSets(self):
        """
        Returns the number of rna quantification sets in this dataset.
        """
        return len(self._rnaQuantificationSetIds)

    def getRnaQuantificationSets(self):
        """
        Returns the list of RnaQuantification sets in this dataset
        """
        return [self._rnaQuantificationSetIdMap[id_] for
                id_ in self._rnaQuantificationSetIds]

    def getRnaQuantificationSetByIndex(self, index):
        """
        Returns the rna quantification set at the specified index in this
        dataset.
        """
        return self._rnaQuantificationSetIdMap[
            self._rnaQuantificationSetIds[index]]

    def getRnaQuantificationSetByName(self, name):
        """
        Returns the RnaQuantification set with the specified name, or raises
        an exception otherwise.
        """
        if name not in self._rnaQuantificationSetNameMap:
            raise exceptions.RnaQuantificationSetNameNotFoundException(name)
        return self._rnaQuantificationSetNameMap[name]

    def getRnaQuantificationSet(self, id_):
        """
        Returns the RnaQuantification set with the specified name, or raises
        a RnaQuantificationSetNotFoundException otherwise.
        """
        if id_ not in self._rnaQuantificationSetIdMap:
            raise exceptions.RnaQuantificationSetNotFoundException(id_)
        return self._rnaQuantificationSetIdMap[id_]


class SimulatedDataset(Dataset):
    """
    A simulated dataset
    """
    def __init__(
            self, localId, referenceSet, randomSeed=0,
            numVariantSets=1, numCalls=1, variantDensity=0.5,
            numReadGroupSets=1, numReadGroupsPerReadGroupSet=1,
            numAlignments=1, numFeatureSets=1, numContinuousSets=1,
            numPhenotypeAssociationSets=1,
            numPhenotypeAssociations=2, numRnaQuantSets=2,
            numExpressionLevels=2):
        super(SimulatedDataset, self).__init__(localId)
        self._description = "Simulated dataset {}".format(localId)

        for i in range(numPhenotypeAssociationSets):
            localId = "simPas{}".format(i)
            seed = randomSeed + i
            phenotypeAssociationSet = g2p.SimulatedPhenotypeAssociationSet(
                self, localId, seed, numPhenotypeAssociations)
            self.addPhenotypeAssociationSet(phenotypeAssociationSet)

        # TODO create a simulated Ontology
        # Variants
        for i in range(numVariantSets):
            localId = "simVs{}".format(i)
            seed = randomSeed + i
            variantSet = variants.SimulatedVariantSet(
                self, referenceSet, localId, seed, numCalls, variantDensity)
            callSets = variantSet.getCallSets()
            # Add biosamples
            for callSet in callSets:
                biosample = biodata.Biosample(
                    self, callSet.getLocalId())
                biosample2 = biodata.Biosample(
                    self, callSet.getLocalId() + "2")
                individual = biodata.Individual(
                    self, callSet.getLocalId())
                biosample.setIndividualId(individual.getId())
                biosample2.setIndividualId(individual.getId())
                self.addIndividual(individual)
                self.addBiosample(biosample)
                self.addBiosample(biosample2)
            self.addVariantSet(variantSet)
            variantAnnotationSet = variants.SimulatedVariantAnnotationSet(
                variantSet, "simVas{}".format(i), seed)
            variantSet.addVariantAnnotationSet(variantAnnotationSet)
        # Reads
        for i in range(numReadGroupSets):
            localId = 'simRgs{}'.format(i)
            seed = randomSeed + i
            readGroupSet = reads.SimulatedReadGroupSet(
                self, localId, referenceSet, seed,
                numReadGroupsPerReadGroupSet, numAlignments)
            for rg in readGroupSet.getReadGroups():
                biosample = biodata.Biosample(
                    self, rg.getLocalId())
                individual = biodata.Individual(
                    self, rg.getLocalId())
                biosample.setIndividualId(individual.getId())
                rg.setBiosampleId(biosample.getId())
                self.addIndividual(individual)
                self.addBiosample(biosample)
            self.addReadGroupSet(readGroupSet)
        # Features
        for i in range(numFeatureSets):
            localId = "simFs{}".format(i)
            seed = randomSeed + i
            featureSet = sequence_annotations.SimulatedFeatureSet(
                self, localId, seed)
            featureSet.setReferenceSet(referenceSet)
            self.addFeatureSet(featureSet)
        # Continuous
        for i in range(numContinuousSets):
            localId = "simConts{}".format(i)
            seed = randomSeed + i
            continuousSet = continuous.SimulatedContinuousSet(
                self, localId, seed)
            continuousSet.setReferenceSet(referenceSet)
            self.addContinuousSet(continuousSet)
        # RnaQuantificationSets
        for i in range(numRnaQuantSets):
            localId = 'simRqs{}'.format(i)
            rnaQuantSet = rnaQuantification.SimulatedRnaQuantificationSet(
                self, localId)
            rnaQuantSet.setReferenceSet(referenceSet)
            self.addRnaQuantificationSet(rnaQuantSet)
