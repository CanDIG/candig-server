"""
repo manager cli
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import glob
import json
import os
import sys
import textwrap
import traceback
import urlparse

import candig.server.cli as cli
import candig.server.datamodel.bio_metadata as bio_metadata
import candig.server.datamodel.datasets as datasets
import candig.server.datamodel.genotype_phenotype as genotype_phenotype
import candig.server.datamodel.ontologies as ontologies
import candig.server.datamodel.reads as reads
import candig.server.datamodel.references as references
import candig.server.datamodel.rna_quantification as rna_quantification
import candig.server.datamodel.sequence_annotations as sequence_annotations
import candig.server.datamodel.continuous as continuous
import candig.server.datamodel.variants as variants
import candig.server.datamodel.peers as peers
import candig.server.datarepo as datarepo
import candig.server.exceptions as exceptions
import candig.server.repo.rnaseq2ga as rnaseq2ga

import ga4gh.common.cli as common_cli


def getNameFromPath(filePath):
    """
    Returns the filename of the specified path without its extensions.
    This is usually how we derive the default name for a given object.
    """
    if len(filePath) == 0:
        raise ValueError("Cannot have empty path for name")
    fileName = os.path.split(os.path.normpath(filePath))[1]
    # We need to handle things like .fa.gz, so we can't use
    # os.path.splitext
    ret = fileName.split(".")[0]
    assert ret != ""
    return ret


def getRawInput(display):
    """
    Wrapper around raw_input; put into separate function so that it
    can be easily mocked for tests.
    """
    return raw_input(display)


class RepoManager(object):
    """
    Class that provide command line functionality to manage a
    data repository.
    """
    def __init__(self, args):
        self._args = args
        self._registryPath = args.registryPath
        self._repo = datarepo.SqlDataRepository(self._registryPath)

    def _confirmDelete(self, objectType, name, func):
        if self._args.force:
            func()
        else:
            displayString = (
                "Are you sure you want to delete the {} '{}'? "
                "[y|N] ".format(objectType, name))
            userResponse = getRawInput(displayString)
            if userResponse.strip() == 'y':
                func()
            else:
                print("Aborted")

    def _updateRepo(self, func, *args, **kwargs):
        """
        Runs the specified function that updates the repo with the specified
        arguments. This method ensures that all updates are transactional,
        so that if any part of the update fails no changes are made to the
        repo.
        """
        # TODO how do we make this properly transactional?
        self._repo.open(datarepo.MODE_WRITE)
        try:
            func(*args, **kwargs)
            self._repo.commit()
        finally:
            self._repo.close()

    def _openRepo(self):
        if not self._repo.exists():
            raise exceptions.RepoManagerException(
                "Repo '{}' does not exist. Please create a new repo "
                "using the 'init' command.".format(self._registryPath))
        self._repo.open(datarepo.MODE_READ)

    def _checkSequenceOntology(self, ontology):
        so = ontologies.SEQUENCE_ONTOLOGY_PREFIX
        if ontology.getOntologyPrefix() != so:
            raise exceptions.RepoManagerException(
                "Ontology '{}' does not have ontology prefix '{}'".format(
                    ontology.getName(), so))

    def _getFilePath(self, filePath, useRelativePath):
        return filePath if useRelativePath else os.path.abspath(filePath)

    def init(self):
        forceMessage = (
            "Respository '{}' already exists. Use --force to overwrite")
        if self._repo.exists():
            if self._args.force:
                self._repo.delete()
            else:
                raise exceptions.RepoManagerException(
                    forceMessage.format(self._registryPath))
        self._updateRepo(self._repo.initialise)

    def list(self):
        """
        Lists the contents of this repo.
        """
        self._openRepo()
        # TODO this is _very_ crude. We need much more options and detail here.
        self._repo.printSummary()

    def listAnnouncements(self):
        """
        Lists all the announcements the repo has received.
        """
        self._openRepo()
        self._repo.printAnnouncements()
        
    def clearAnnouncements(self):
        """
        Clears the list of announcements from the repo.
        """
        self._openRepo()
        self._repo.clearAnnouncements()

    def verify(self):
        """
        Checks that the data pointed to in the repository works and
        we don't have any broken URLs, missing files, etc.
        """
        self._openRepo()
        self._repo.verify()

    def addOntology(self):
        """
        Adds a new Ontology to this repo.
        """
        self._openRepo()
        name = self._args.name
        filePath = self._getFilePath(self._args.filePath,
                                     self._args.relativePath)
        if name is None:
            name = getNameFromPath(filePath)
        ontology = ontologies.Ontology(name)
        ontology.populateFromFile(filePath)
        self._updateRepo(self._repo.insertOntology, ontology)

    def addDataset(self):
        """
        Adds a new dataset into this repo.
        """
        self._openRepo()
        dataset = datasets.Dataset(self._args.datasetName)
        dataset.setDescription(self._args.description)
        dataset.setAttributes(json.loads(self._args.attributes))
        self._updateRepo(self._repo.insertDataset, dataset)

    def addReferenceSet(self):
        """
        Adds a new reference set into this repo.
        """
        self._openRepo()
        name = self._args.name
        filePath = self._getFilePath(self._args.filePath,
                                     self._args.relativePath)
        if name is None:
            name = getNameFromPath(self._args.filePath)
        referenceSet = references.HtslibReferenceSet(name)
        referenceSet.populateFromFile(filePath)
        referenceSet.setDescription(self._args.description)
        if self._args.species is not None:
            referenceSet.setSpeciesFromJson(self._args.species)
        referenceSet.setIsDerived(self._args.isDerived)
        referenceSet.setAssemblyId(self._args.assemblyId)
        referenceSet.setAttributes(json.loads(self._args.attributes))
        sourceAccessions = []
        if self._args.sourceAccessions is not None:
            sourceAccessions = self._args.sourceAccessions.split(",")
        referenceSet.setSourceAccessions(sourceAccessions)
        referenceSet.setSourceUri(self._args.sourceUri)
        self._updateRepo(self._repo.insertReferenceSet, referenceSet)

    def addReadGroupSet(self):
        """
        Adds a new ReadGroupSet into this repo.
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        dataUrl = self._args.dataFile
        indexFile = self._args.indexFile
        parsed = urlparse.urlparse(dataUrl)
        # TODO, add https support and others when they have been
        # tested.
        if parsed.scheme in ['http', 'ftp']:
            if indexFile is None:
                raise exceptions.MissingIndexException(dataUrl)
        else:
            if indexFile is None:
                indexFile = dataUrl + ".bai"
            dataUrl = self._getFilePath(self._args.dataFile,
                                        self._args.relativePath)
            indexFile = self._getFilePath(indexFile, self._args.relativePath)
        name = self._args.name
        if self._args.name is None:
            name = getNameFromPath(dataUrl)
        readGroupSet = reads.HtslibReadGroupSet(dataset, name)
        readGroupSet.populateFromFile(dataUrl, indexFile)
        referenceSetName = self._args.referenceSetName
        if referenceSetName is None:
            # Try to find a reference set name from the BAM header.
            referenceSetName = readGroupSet.getBamHeaderReferenceSetName()
        referenceSet = self._repo.getReferenceSetByName(referenceSetName)
        readGroupSet.setReferenceSet(referenceSet)
        patientId = self._args.patientId
        if patientId is None:
            raise exceptions.RepoManagerException(
                "Please provide a corresponding patient ID"
            )
        sampleId = self._args.sampleId
        if sampleId is None:
            raise exceptions.RepoManagerException(
                "Please provide a corresponding sample ID"
            )
        readGroupSet.setPatientId(patientId)
        readGroupSet.setSampleId(sampleId)
        readGroupSet.setAttributes(json.loads(self._args.attributes))
        self._updateRepo(self._repo.insertReadGroupSet, readGroupSet)

    def addVariantSet(self):
        """
        Adds a new VariantSet into this repo.
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        dataUrls = self._args.dataFiles
        name = self._args.name
        if len(dataUrls) == 1:
            if self._args.name is None:
                name = getNameFromPath(dataUrls[0])
            if os.path.isdir(dataUrls[0]):
                # Read in the VCF files from the directory.
                # TODO support uncompressed VCF and BCF files
                vcfDir = dataUrls[0]
                pattern = os.path.join(vcfDir, "*.vcf.gz")
                dataUrls = glob.glob(pattern)
                if len(dataUrls) == 0:
                    raise exceptions.RepoManagerException(
                        "Cannot find any VCF files in the directory "
                        "'{}'.".format(vcfDir))
                dataUrls[0] = self._getFilePath(dataUrls[0],
                                                self._args.relativePath)
        elif self._args.name is None:
            raise exceptions.RepoManagerException(
                "Cannot infer the intended name of the VariantSet when "
                "more than one VCF file is provided. Please provide a "
                "name argument using --name.")
        parsed = urlparse.urlparse(dataUrls[0])
        if parsed.scheme not in ['http', 'ftp']:
            dataUrls = map(lambda url: self._getFilePath(
                url, self._args.relativePath), dataUrls)
        # Now, get the index files for the data files that we've now obtained.
        indexFiles = self._args.indexFiles
        if indexFiles is None:
            # First check if all the paths exist locally, as they must
            # if we are making a default index path.
            for dataUrl in dataUrls:
                if not os.path.exists(dataUrl):
                    raise exceptions.MissingIndexException(
                        "Cannot find file '{}'. All variant files must be "
                        "stored locally if the default index location is "
                        "used. If you are trying to create a VariantSet "
                        "based on remote URLs, please download the index "
                        "files to the local file system and provide them "
                        "with the --indexFiles argument".format(dataUrl))
            # We assume that the indexes are made by adding .tbi
            indexSuffix = ".tbi"
            # TODO support BCF input properly here by adding .csi
            indexFiles = [filename + indexSuffix for filename in dataUrls]
        indexFiles = map(lambda url: self._getFilePath(
            url, self._args.relativePath), indexFiles)
        variantSet = variants.HtslibVariantSet(dataset, name)
        variantSet.populateFromFile(dataUrls, indexFiles)
        # Get the reference set that is associated with the variant set.
        referenceSetName = self._args.referenceSetName
        if referenceSetName is None:
            # Try to find a reference set name from the VCF header.
            referenceSetName = variantSet.getVcfHeaderReferenceSetName()
        if referenceSetName is None:
            raise exceptions.RepoManagerException(
                "Cannot infer the ReferenceSet from the VCF header. Please "
                "specify the ReferenceSet to associate with this "
                "VariantSet using the --referenceSetName option")
        referenceSet = self._repo.getReferenceSetByName(referenceSetName)
        variantSet.setReferenceSet(referenceSet)
        patientId = self._args.patientId
        if patientId is None:
            raise exceptions.RepoManagerException(
                "Please provide a corresponding patient ID"
            )
        sampleId = self._args.sampleId
        if sampleId is None:
            raise exceptions.RepoManagerException(
                "Please provide a corresponding sample ID"
            )
        variantSet.setPatientId(patientId)
        variantSet.setSampleId(sampleId)
        variantSet.setAttributes(json.loads(self._args.attributes))
        # Now check for annotations
        annotationSets = []
        if variantSet.isAnnotated() and self._args.addAnnotationSets:
            ontologyName = self._args.ontologyName
            if ontologyName is None:
                raise exceptions.RepoManagerException(
                    "A sequence ontology name must be provided")
            ontology = self._repo.getOntologyByName(ontologyName)
            self._checkSequenceOntology(ontology)
            for annotationSet in variantSet.getVariantAnnotationSets():
                annotationSet.setOntology(ontology)
                annotationSets.append(annotationSet)

        # Add the annotation sets and the variant set as an atomic update
        def updateRepo():
            self._repo.insertVariantSet(variantSet)
            for annotationSet in annotationSets:
                self._repo.insertVariantAnnotationSet(annotationSet)
        self._updateRepo(updateRepo)

    def addPhenotypeAssociationSet(self):
        """
        Adds a new phenotype association set to this repo.
        """
        self._openRepo()
        name = self._args.name
        if name is None:
            name = getNameFromPath(self._args.dirPath)
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        phenotypeAssociationSet = \
            genotype_phenotype.RdfPhenotypeAssociationSet(
                dataset, name, self._args.dirPath)
        phenotypeAssociationSet.setAttributes(
            json.loads(self._args.attributes))
        self._updateRepo(
            self._repo.insertPhenotypeAssociationSet,
            phenotypeAssociationSet)

    def removePhenotypeAssociationSet(self):
        """
        Removes a phenotype association set from the repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        phenotypeAssociationSet = dataset.getPhenotypeAssociationSetByName(
            self._args.name)

        def func():
            self._updateRepo(
                self._repo.removePhenotypeAssociationSet,
                phenotypeAssociationSet)
        self._confirmDelete(
            "PhenotypeAssociationSet",
            phenotypeAssociationSet.getLocalId(),
            func)

    def removeReferenceSet(self):
        """
        Removes a referenceSet from the repo.
        """
        self._openRepo()
        referenceSet = self._repo.getReferenceSetByName(
            self._args.referenceSetName)

        def func():
            self._updateRepo(self._repo.removeReferenceSet, referenceSet)
        self._confirmDelete("ReferenceSet", referenceSet.getLocalId(), func)

    def removeReadGroupSet(self):
        """
        Removes a readGroupSet from the repo.
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        readGroupSet = dataset.getReadGroupSetByName(
            self._args.readGroupSetName)

        def func():
            self._updateRepo(self._repo.removeReadGroupSet, readGroupSet)
        self._confirmDelete("ReadGroupSet", readGroupSet.getLocalId(), func)

    def removeVariantSet(self):
        """
        Removes a variantSet from the repo.
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        variantSet = dataset.getVariantSetByName(self._args.variantSetName)

        def func():
            self._updateRepo(self._repo.removeVariantSet, variantSet)
        self._confirmDelete("VariantSet", variantSet.getLocalId(), func)

    def removeDataset(self):
        """
        Removes a dataset from the repo.
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)

        def func():
            self._updateRepo(self._repo.removeDataset, dataset)
        self._confirmDelete("Dataset", dataset.getLocalId(), func)

    def addFeatureSet(self):
        """
        Adds a new feature set into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        filePath = self._getFilePath(self._args.filePath,
                                     self._args.relativePath)
        name = getNameFromPath(self._args.filePath)
        featureSet = sequence_annotations.Gff3DbFeatureSet(
            dataset, name)
        referenceSetName = self._args.referenceSetName
        if referenceSetName is None:
            raise exceptions.RepoManagerException(
                "A reference set name must be provided")
        referenceSet = self._repo.getReferenceSetByName(referenceSetName)
        featureSet.setReferenceSet(referenceSet)
        ontologyName = self._args.ontologyName
        if ontologyName is None:
            raise exceptions.RepoManagerException(
                "A sequence ontology name must be provided")
        ontology = self._repo.getOntologyByName(ontologyName)
        self._checkSequenceOntology(ontology)
        featureSet.setOntology(ontology)
        featureSet.populateFromFile(filePath)
        featureSet.setAttributes(json.loads(self._args.attributes))
        self._updateRepo(self._repo.insertFeatureSet, featureSet)

    def removeFeatureSet(self):
        """
        Removes a feature set from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        featureSet = dataset.getFeatureSetByName(self._args.featureSetName)

        def func():
            self._updateRepo(self._repo.removeFeatureSet, featureSet)
        self._confirmDelete("FeatureSet", featureSet.getLocalId(), func)

    def addContinuousSet(self):
        """
        Adds a new continuous set into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        filePath = self._getFilePath(self._args.filePath,
                                     self._args.relativePath)
        name = getNameFromPath(self._args.filePath)
        continuousSet = continuous.FileContinuousSet(dataset, name)
        referenceSetName = self._args.referenceSetName
        if referenceSetName is None:
            raise exceptions.RepoManagerException(
                "A reference set name must be provided")
        referenceSet = self._repo.getReferenceSetByName(referenceSetName)
        continuousSet.setReferenceSet(referenceSet)
        continuousSet.populateFromFile(filePath)
        self._updateRepo(self._repo.insertContinuousSet, continuousSet)

    def removeContinuousSet(self):
        """
        Removes a continuous set from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        continuousSet = dataset.getContinuousSetByName(self._args.continuousSetName)

        def func():
            self._updateRepo(self._repo.removeContinuousSet, continuousSet)
        self._confirmDelete("ContinuousSet", continuousSet.getLocalId(), func)

    def addBiosample(self):
        """
        Adds a new biosample into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        biosample = bio_metadata.Biosample(
            dataset, self._args.biosampleName)
        biosample.populateFromJson(self._args.biosample)
        self._updateRepo(self._repo.insertBiosample, biosample)

    def removeBiosample(self):
        """
        Removes a biosample from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        biosample = dataset.getBiosampleByName(self._args.biosampleName)

        def func():
            self._updateRepo(self._repo.removeBiosample, biosample)
        self._confirmDelete("Biosample", biosample.getLocalId(), func)

    def addIndividual(self):
        """
        Adds a new individual into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        individual = bio_metadata.Individual(
            dataset, self._args.individualName)
        individual.populateFromJson(self._args.individual)
        self._updateRepo(self._repo.insertIndividual, individual)

    def removeIndividual(self):
        """
        Removes an individual from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        individual = dataset.getIndividualByName(self._args.individualName)

        def func():
            self._updateRepo(self._repo.removeIndividual, individual)
        self._confirmDelete("Individual", individual.getLocalId(), func)

    def addPatient(self):
        """
        Adds a new patient into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        patient = bio_metadata.Patient(
            dataset, self._args.patientName)
        patient.populateFromJson(self._args.patient)
        self._updateRepo(self._repo.insertPatient, patient)

    def removePatient(self):
        """
        Removes an patient from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        patient = dataset.getPatientByName(self._args.patientName)

        def func():
            self._updateRepo(self._repo.removePatient, patient)
        self._confirmDelete("Patient", patient.getLocalId(), func)
        
    def addEnrollment(self):
        """
        Adds a new enrollment into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        enrollment = bio_metadata.Enrollment(
            dataset, self._args.enrollmentName)
        enrollment.populateFromJson(self._args.enrollment)
        self._updateRepo(self._repo.insertEnrollment, enrollment)

    def removeEnrollment(self):
        """
        Removes an enrollment from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        enrollment = dataset.getEnrollmentByName(self._args.enrollmentName)

        def func():
            self._updateRepo(self._repo.removeEnrollment, enrollment)
        self._confirmDelete("Enrollment", enrollment.getLocalId(), func)
        
    def addConsent(self):
        """
        Adds a new consent into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        consent = bio_metadata.Consent(
            dataset, self._args.consentName)
        consent.populateFromJson(self._args.consent)
        self._updateRepo(self._repo.insertConsent, consent)

    def removeConsent(self):
        """
        Removes an consent from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        consent = dataset.getConsentByName(self._args.consentName)

        def func():
            self._updateRepo(self._repo.removeConsent, consent)
        self._confirmDelete("Consent", consent.getLocalId(), func)
        
    def addDiagnosis(self):
        """
        Adds a new diagnosis into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        diagnosis = bio_metadata.Diagnosis(
            dataset, self._args.diagnosisName)
        diagnosis.populateFromJson(self._args.diagnosis)
        self._updateRepo(self._repo.insertDiagnosis, diagnosis)

    def removeDiagnosis(self):
        """
        Removes an diagnosis from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        diagnosis = dataset.getDiagnosisByName(self._args.diagnosisName)

        def func():
            self._updateRepo(self._repo.removeDiagnosis, diagnosis)
        self._confirmDelete("Diagnosis", diagnosis.getLocalId(), func)
        
    def addSample(self):
        """
        Adds a new sample into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        sample = bio_metadata.Sample(
            dataset, self._args.sampleName)
        sample.populateFromJson(self._args.sample)
        self._updateRepo(self._repo.insertSample, sample)

    def removeSample(self):
        """
        Removes an sample from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        sample = dataset.getSampleByName(self._args.sampleName)

        def func():
            self._updateRepo(self._repo.removeSample, sample)
        self._confirmDelete("Sample", sample.getLocalId(), func)
        
    def addTreatment(self):
        """
        Adds a new treatment into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        treatment = bio_metadata.Treatment(
            dataset, self._args.treatmentName)
        treatment.populateFromJson(self._args.treatment)
        self._updateRepo(self._repo.insertTreatment, treatment)

    def removeTreatment(self):
        """
        Removes an treatment from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        treatment = dataset.getTreatmentByName(self._args.treatmentName)

        def func():
            self._updateRepo(self._repo.removeTreatment, treatment)
        self._confirmDelete("Treatment", treatment.getLocalId(), func)
        
    def addOutcome(self):
        """
        Adds a new outcome into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        outcome = bio_metadata.Outcome(
            dataset, self._args.outcomeName)
        outcome.populateFromJson(self._args.outcome)
        self._updateRepo(self._repo.insertOutcome, outcome)

    def removeOutcome(self):
        """
        Removes an outcome from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        outcome = dataset.getOutcomeByName(self._args.outcomeName)

        def func():
            self._updateRepo(self._repo.removeOutcome, outcome)
        self._confirmDelete("Outcome", outcome.getLocalId(), func)
        
    def addComplication(self):
        """
        Adds a new complication into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        complication = bio_metadata.Complication(
            dataset, self._args.complicationName)
        complication.populateFromJson(self._args.complication)
        self._updateRepo(self._repo.insertComplication, complication)

    def removeComplication(self):
        """
        Removes an complication from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        complication = dataset.getComplicationByName(self._args.complicationName)

        def func():
            self._updateRepo(self._repo.removeComplication, complication)
        self._confirmDelete("Complication", complication.getLocalId(), func)
        
    def addTumourboard(self):
        """
        Adds a new tumourboard into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        tumourboard = bio_metadata.Tumourboard(
            dataset, self._args.tumourboardName)
        tumourboard.populateFromJson(self._args.tumourboard)
        self._updateRepo(self._repo.insertTumourboard, tumourboard)

    def removeTumourboard(self):
        """
        Removes an tumourboard from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        tumourboard = dataset.getTumourboardByName(self._args.tumourboardName)

        def func():
            self._updateRepo(self._repo.removeTumourboard, tumourboard)
        self._confirmDelete("Tumourboard", tumourboard.getLocalId(), func)

    def addChemotherapy(self):
        """
        Adds a new chemotherapy into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        chemotherapy = bio_metadata.Chemotherapy(
            dataset, self._args.chemotherapyName)
        chemotherapy.populateFromJson(self._args.chemotherapy)
        self._updateRepo(self._repo.insertChemotherapy, chemotherapy)

    def removeChemotherapy(self):
        """
        Removes an chemotherapy from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        chemotherapy = dataset.getChemotherapyByName(self._args.chemotherapyName)

        def func():
            self._updateRepo(self._repo.removeChemotherapy, chemotherapy)
        self._confirmDelete("Chemotherapy", chemotherapy.getLocalId(), func)

    def addRadiotherapy(self):
        """
        Adds a new radiotherapy into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        radiotherapy = bio_metadata.Radiotherapy(
            dataset, self._args.radiotherapyName)
        radiotherapy.populateFromJson(self._args.radiotherapy)
        self._updateRepo(self._repo.insertRadiotherapy, radiotherapy)

    def removeRadiotherapy(self):
        """
        Removes an radiotherapy from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        radiotherapy = dataset.getRadiotherapyByName(self._args.radiotherapyName)

        def func():
            self._updateRepo(self._repo.removeRadiotherapy, radiotherapy)
        self._confirmDelete("Radiotherapy", radiotherapy.getLocalId(), func)

    def addSurgery(self):
        """
        Adds a new surgery into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        surgery = bio_metadata.Surgery(
            dataset, self._args.surgeryName)
        surgery.populateFromJson(self._args.surgery)
        self._updateRepo(self._repo.insertSurgery, surgery)

    def removeSurgery(self):
        """
        Removes an surgery from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        surgery = dataset.getSurgeryByName(self._args.surgeryName)

        def func():
            self._updateRepo(self._repo.removeSurgery, surgery)
        self._confirmDelete("Surgery", surgery.getLocalId(), func)

    def addImmunotherapy(self):
        """
        Adds a new immunotherapy into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        immunotherapy = bio_metadata.Immunotherapy(
            dataset, self._args.immunotherapyName)
        immunotherapy.populateFromJson(self._args.immunotherapy)
        self._updateRepo(self._repo.insertImmunotherapy, immunotherapy)

    def removeImmunotherapy(self):
        """
        Removes an immunotherapy from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        immunotherapy = dataset.getImmunotherapyByName(self._args.immunotherapyName)

        def func():
            self._updateRepo(self._repo.removeImmunotherapy, immunotherapy)
        self._confirmDelete("Immunotherapy", immunotherapy.getLocalId(), func)

    def addCelltransplant(self):
        """
        Adds a new celltransplant into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        celltransplant = bio_metadata.Celltransplant(
            dataset, self._args.celltransplantName)
        celltransplant.populateFromJson(self._args.celltransplant)
        self._updateRepo(self._repo.insertCelltransplant, celltransplant)

    def removeCelltransplant(self):
        """
        Removes an celltransplant from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        celltransplant = dataset.getCelltransplantByName(self._args.celltransplantName)

        def func():
            self._updateRepo(self._repo.removeCelltransplant, celltransplant)
        self._confirmDelete("Celltransplant", celltransplant.getLocalId(), func)

    def addSlide(self):
        """
        Adds a new slide into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        slide = bio_metadata.Slide(
            dataset, self._args.slideName)
        slide.populateFromJson(self._args.slide)
        self._updateRepo(self._repo.insertSlide, slide)

    def removeSlide(self):
        """
        Removes an slide from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        slide = dataset.getSlideByName(self._args.slideName)

        def func():
            self._updateRepo(self._repo.removeSlide, slide)
        self._confirmDelete("Slide", slide.getLocalId(), func)

    def addStudy(self):
        """
        Adds a new study into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        study = bio_metadata.Study(
            dataset, self._args.studyName)
        study.populateFromJson(self._args.study)
        self._updateRepo(self._repo.insertStudy, study)

    def removeStudy(self):
        """
        Removes an study from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        study = dataset.getStudyByName(self._args.studyName)

        def func():
            self._updateRepo(self._repo.removeStudy, study)
        self._confirmDelete("Study", study.getLocalId(), func)

    def addLabtest(self):
        """
        Adds a new labtest into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        labtest = bio_metadata.Labtest(
            dataset, self._args.labtestName)
        labtest.populateFromJson(self._args.labtest)
        self._updateRepo(self._repo.insertLabtest, labtest)

    def removeLabtest(self):
        """
        Removes an labtest from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        labtest = dataset.getLabtestByName(self._args.labtestName)

        def func():
            self._updateRepo(self._repo.removeLabtest, labtest)
        self._confirmDelete("Labtest", labtest.getLocalId(), func)

    def addExtraction(self):
        """
        Adds a new extraction into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        extraction = bio_metadata.Extraction(
            dataset, self._args.extractionName)
        extraction.populateFromJson(self._args.extraction)
        self._updateRepo(self._repo.insertExtraction, extraction)

    def removeExtraction(self):
        """
        Removes an extraction from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        extraction = dataset.getExtractionByName(self._args.extractionName)

        def func():
            self._updateRepo(self._repo.removeExtraction, extraction)

        self._confirmDelete("Extraction", extraction.getLocalId(), func)

    def addSequencing(self):
        """
        Adds a new sequencing into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        sequencing = bio_metadata.Sequencing(
            dataset, self._args.sequencingName)
        sequencing.populateFromJson(self._args.sequencing)
        self._updateRepo(self._repo.insertSequencing, sequencing)

    def removeSequencing(self):
        """
        Removes an sequencing from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        sequencing = dataset.getSequencingByName(self._args.sequencingName)

        def func():
            self._updateRepo(self._repo.removeSequencing, sequencing)

        self._confirmDelete("Sequencing", sequencing.getLocalId(), func)

    def addAlignment(self):
        """
        Adds a new alignment into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        alignment = bio_metadata.Alignment(
            dataset, self._args.alignmentName)
        alignment.populateFromJson(self._args.alignment)
        self._updateRepo(self._repo.insertAlignment, alignment)

    def removeAlignment(self):
        """
        Removes an alignment from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        alignment = dataset.getAlignmentByName(self._args.alignmentName)

        def func():
            self._updateRepo(self._repo.removeAlignment, alignment)

        self._confirmDelete("Alignment", alignment.getLocalId(), func)

    def addVariantCalling(self):
        """
        Adds a new variantCalling into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        variantCalling = bio_metadata.VariantCalling(
            dataset, self._args.variantCallingName)
        variantCalling.populateFromJson(self._args.variantCalling)
        self._updateRepo(self._repo.insertVariantCalling, variantCalling)

    def removeVariantCalling(self):
        """
        Removes an variantCalling from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        variantCalling = dataset.getVariantCallingByName(self._args.variantCallingName)

        def func():
            self._updateRepo(self._repo.removeVariantCalling, variantCalling)

        self._confirmDelete("VariantCalling", variantCalling.getLocalId(), func)

    def addFusionDetection(self):
        """
        Adds a new expressionAnalysis into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        fusionDetection = bio_metadata.FusionDetection(
            dataset, self._args.fusionDetectionName)
        fusionDetection.populateFromJson(self._args.fusionDetection)
        self._updateRepo(self._repo.insertFusionDetection, fusionDetection)

    def removeFusionDetection(self):
        """
        Removes an fusionDetection from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        fusionDetection = dataset.getFusionDetectionByName(self._args.fusionDetectionName)

        def func():
            self._updateRepo(self._repo.removeFusionDetection, fusionDetection)

        self._confirmDelete("FusionDetection", fusionDetection.getLocalId(), func)

    def addExpressionAnalysis(self):
        """
        Adds a new expressionAnalysis into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        expressionAnalysis = bio_metadata.ExpressionAnalysis(
            dataset, self._args.expressionAnalysisName)
        expressionAnalysis.populateFromJson(self._args.expressionAnalysis)
        self._updateRepo(self._repo.insertExpressionAnalysis, expressionAnalysis)

    def removeExpressionAnalysis(self):
        """
        Removes an expressionAnalysis from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        expressionAnalysis = dataset.getExpressionAnalysisByName(self._args.expressionAnalysisName)

        def func():
            self._updateRepo(self._repo.removeExpressionAnalysis, expressionAnalysis)

        self._confirmDelete("ExpressionAnalysis", expressionAnalysis.getLocalId(), func)

    def addPeer(self):
        """
        Adds a new peer into this repo
        """
        self._openRepo()
        try:
            peer = peers.Peer(
                self._args.url, json.loads(self._args.attributes))
        except exceptions.BadUrlException:
            raise exceptions.RepoManagerException("The URL for the peer was "
                                                  "malformed.")
        except ValueError as e:
            raise exceptions.RepoManagerException(
                "The attributes message "
                "was malformed. {}".format(e))
        self._updateRepo(self._repo.insertPeer, peer)

    def removePeer(self):
        """
        Removes a peer by URL from this repo
        """
        self._openRepo()

        def func():
            self._updateRepo(self._repo.removePeer, self._args.url)
        self._confirmDelete("Peer", self._args.url, func)

    def removePeers(self):
        """
        Clears the list of peers from the repo.
        """
        self._openRepo()
        self._repo.removePeers()

    def addExperiment(self):
        """
        Adds a new experiment into this repo
        """
        self._openRepo()
        experiment = bio_metadata.Experiment(self._args.experimentName)
        experiment.populateFromJson(self._args.experiment)
        experiment.setDescription(self._args.description)
        self._updateRepo(self._repo.insertExperiment, experiment)

    def removeExperiment(self):
        """
        Removes an experiment from this repo
        """
        self._openRepo()
        experiment = self._repo.getExperimentByName(self._args.experimentName)

        def func():
            self._updateRepo(self._repo.removeExperiment, experiment)
        self._confirmDelete("Experiment", experiment.getLocalId(), func)

    def addAnalysis(self):
        """
        Adds a new analysis into this repo
        """
        self._openRepo()
        analysis = bio_metadata.Analysis(self._args.analysisName)
        analysis.populateFromJson(self._args.analysis)
        analysis.setName(self._args.analysisName)
        analysis.setDescription(self._args.description)
        self._updateRepo(self._repo.insertAnalysis, analysis)

    def removeAnalysis(self):
        """
        Removes an analysis from this repo
        """
        self._openRepo()
        analysis = self._repo.getAnalysisByName(self._args.analysisName)

        def func():
            self._updateRepo(self._repo.removeAnalysis, analysis)
        self._confirmDelete("Analysis", analysis.getLocalId(), func)

    def removeOntology(self):
        """
        Removes an ontology from the repo.
        """
        self._openRepo()
        ontology = self._repo.getOntologyByName(self._args.ontologyName)

        def func():
            self._updateRepo(self._repo.removeOntology, ontology)
        self._confirmDelete("Ontology", ontology.getName(), func)

    def addRnaQuantification(self):
        """
        Adds an rnaQuantification into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        biosampleId = ""
        if self._args.biosampleName:
            biosample = dataset.getBiosampleByName(self._args.biosampleName)
            biosampleId = biosample.getId()
        if self._args.name is None:
            name = getNameFromPath(self._args.quantificationFilePath)
        else:
            name = self._args.name
        # TODO: programs not fully supported by GA4GH yet
        sampleId = self._args.sampleId
        patientId = self._args.patientId
        programs = ""
        featureType = "gene"
        if self._args.transcript:
            featureType = "transcript"

        if patientId is None:
            raise exceptions.RepoManagerException(
                "Please provide a corresponding patient ID"
            )
        if sampleId is None:
            raise exceptions.RepoManagerException(
                "Please provide a corresponding sample ID"
            )
        rnaseq2ga.rnaseq2ga(
            self._args.quantificationFilePath, self._args.filePath, name,
            self._args.format, dataset=dataset, featureType=featureType,
            description=self._args.description, programs=programs,
            featureSetNames=self._args.featureSetNames,
            readGroupSetNames=self._args.readGroupSetName,
            biosampleId=biosampleId, sampleId=sampleId, patientId=patientId)

    def initRnaQuantificationSet(self):
        """
        Initialize an empty RNA quantification set
        """
        store = rnaseq2ga.RnaSqliteStore(self._args.filePath)
        store.createTables()

    def addRnaQuantificationSet(self):
        """
        Adds an rnaQuantificationSet into this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        if self._args.name is None:
            name = getNameFromPath(self._args.filePath)
        else:
            name = self._args.name
        rnaQuantificationSet = rna_quantification.SqliteRnaQuantificationSet(
            dataset, name)
        referenceSetName = self._args.referenceSetName
        if referenceSetName is None:
            raise exceptions.RepoManagerException(
                "A reference set name must be provided")
        referenceSet = self._repo.getReferenceSetByName(referenceSetName)
        rnaQuantificationSet.setReferenceSet(referenceSet)
        rnaQuantificationSet.populateFromFile(self._args.filePath)
        rnaQuantificationSet.setAttributes(json.loads(self._args.attributes))
        self._updateRepo(
            self._repo.insertRnaQuantificationSet, rnaQuantificationSet)

    def removeRnaQuantificationSet(self):
        """
        Removes an rnaQuantificationSet from this repo
        """
        self._openRepo()
        dataset = self._repo.getDatasetByName(self._args.datasetName)
        rnaQuantSet = dataset.getRnaQuantificationSetByName(
            self._args.rnaQuantificationSetName)

        def func():
            self._updateRepo(self._repo.removeRnaQuantificationSet,
                             rnaQuantSet)
        self._confirmDelete(
            "RnaQuantificationSet", rnaQuantSet.getLocalId(), func)

    #
    # Methods to simplify adding common arguments to the parser.
    #

    @classmethod
    def addRepoArgument(cls, subparser):
        subparser.add_argument(
            "registryPath",
            help="the location of the registry database")

    @classmethod
    def addForceOption(cls, subparser):
        subparser.add_argument(
            "-f", "--force", action='store_true',
            default=False, help="do not prompt for confirmation")

    @classmethod
    def addRelativePathOption(cls, subparser):
        subparser.add_argument(
            "-r", "--relativePath", action='store_true',
            default=False, help="store relative path in database")

    @classmethod
    def addDescriptionOption(cls, subparser, objectType):
        subparser.add_argument(
            "-d", "--description", default="",
            help="The human-readable description of the {}.".format(
                objectType))

    @classmethod
    def addDatasetNameArgument(cls, subparser):
        subparser.add_argument(
            "datasetName", help="the name of the dataset")

    @classmethod
    def addAttributesArgument(cls, subparser):
        subparser.add_argument(
            "-A", "--attributes", default="{}",
            help="additional attributes for the message expressed as JSON")

    @classmethod
    def addReferenceSetNameOption(cls, subparser, objectType):
        helpText = (
            "the name of the reference set to associate with this {}"
        ).format(objectType)
        subparser.add_argument(
            "-R", "--referenceSetName", default=None, help=helpText)

    @classmethod
    def addSequenceOntologyNameOption(cls, subparser, objectType):
        helpText = (
            "the name of the sequence ontology instance used to "
            "translate ontology term names to IDs in this {}"
        ).format(objectType)
        subparser.add_argument(
            "-O", "--ontologyName", default=None, help=helpText)

    @classmethod
    def addOntologyNameArgument(cls, subparser):
        subparser.add_argument(
            "ontologyName",
            help="the name of the ontology")

    @classmethod
    def addUrlArgument(cls, subparser):
        subparser.add_argument(
            "url",
            help="The URL of the given resource")

    @classmethod
    def addReadGroupSetNameArgument(cls, subparser):
        subparser.add_argument(
            "readGroupSetName",
            help="the name of the read group set")

    @classmethod
    def addVariantSetNameArgument(cls, subparser):
        subparser.add_argument(
            "variantSetName",
            help="the name of the variant set")

    @classmethod
    def addFeatureSetNameArgument(cls, subparser):
        subparser.add_argument(
            "featureSetName",
            help="the name of the feature set")

    @classmethod
    def addContinuousSetNameArgument(cls, subparser):
        subparser.add_argument(
            "continuousSetName",
            help="the name of the continuous set")

    @classmethod
    def addIndividualNameArgument(cls, subparser):
        subparser.add_argument(
            "individualName",
            help="the name of the individual")

    @classmethod
    def addPatientNameArgument(cls, subparser):
        subparser.add_argument(
            "patientName",
            help="the name of the patient")

    @classmethod
    def addPatientIdArgument(cls, subparser):
        subparser.add_argument(
            "patientId",
            help="the ID of the patient")

    @classmethod
    def addPatientArgument(cls, subparser):
        subparser.add_argument(
            "patient",
            help="the JSON of the patient")

    @classmethod
    def addEnrollmentNameArgument(cls, subparser):
        subparser.add_argument(
            "enrollmentName",
            help="the name of the enrollment")

    @classmethod
    def addEnrollmentArgument(cls, subparser):
        subparser.add_argument(
            "enrollment",
            help="the JSON of the enrollment")

    @classmethod
    def addConsentNameArgument(cls, subparser):
        subparser.add_argument(
            "consentName",
            help="the name of the consent")

    @classmethod
    def addConsentArgument(cls, subparser):
        subparser.add_argument(
            "consent",
            help="the JSON of the consent")

    @classmethod
    def addDiagnosisNameArgument(cls, subparser):
        subparser.add_argument(
            "diagnosisName",
            help="the name of the diagnosis")

    @classmethod
    def addDiagnosisArgument(cls, subparser):
        subparser.add_argument(
            "diagnosis",
            help="the JSON of the diagnosis")

    @classmethod
    def addSampleNameArgument(cls, subparser):
        subparser.add_argument(
            "sampleName",
            help="the name of the sample")

    @classmethod
    def addSampleIdArgument(cls, subparser):
        subparser.add_argument(
            "sampleId",
            help="the ID of the sample")

    @classmethod
    def addSampleArgument(cls, subparser):
        subparser.add_argument(
            "sample",
            help="the JSON of the sample")

    @classmethod
    def addTreatmentNameArgument(cls, subparser):
        subparser.add_argument(
            "treatmentName",
            help="the name of the treatment")

    @classmethod
    def addTreatmentArgument(cls, subparser):
        subparser.add_argument(
            "treatment",
            help="the JSON of the treatment")

    @classmethod
    def addOutcomeNameArgument(cls, subparser):
        subparser.add_argument(
            "outcomeName",
            help="the name of the outcome")

    @classmethod
    def addOutcomeArgument(cls, subparser):
        subparser.add_argument(
            "outcome",
            help="the JSON of the outcome")

    @classmethod
    def addComplicationNameArgument(cls, subparser):
        subparser.add_argument(
            "complicationName",
            help="the name of the complication")

    @classmethod
    def addComplicationArgument(cls, subparser):
        subparser.add_argument(
            "complication",
            help="the JSON of the complication")

    @classmethod
    def addTumourboardNameArgument(cls, subparser):
        subparser.add_argument(
            "tumourboardName",
            help="the name of the tumourboard")

    @classmethod
    def addTumourboardArgument(cls, subparser):
        subparser.add_argument(
            "tumourboard",
            help="the JSON of the tumourboard")

    @classmethod
    def addChemotherapyNameArgument(cls, subparser):
        subparser.add_argument(
            "chemotherapyName",
            help="the name of the chemotherapy")

    @classmethod
    def addChemotherapyArgument(cls, subparser):
        subparser.add_argument(
            "chemotherapy",
            help="the JSON of the chemotherapy")

    @classmethod
    def addRadiotherapyNameArgument(cls, subparser):
        subparser.add_argument(
            "radiotherapyName",
            help="the name of the radiotherapy")

    @classmethod
    def addRadiotherapyArgument(cls, subparser):
        subparser.add_argument(
            "radiotherapy",
            help="the JSON of the radiotherapy")

    @classmethod
    def addSurgeryNameArgument(cls, subparser):
        subparser.add_argument(
            "surgeryName",
            help="the name of the surgery")

    @classmethod
    def addSurgeryArgument(cls, subparser):
        subparser.add_argument(
            "surgery",
            help="the JSON of the surgery")

    @classmethod
    def addImmunotherapyNameArgument(cls, subparser):
        subparser.add_argument(
            "immunotherapyName",
            help="the name of the immunotherapy")

    @classmethod
    def addImmunotherapyArgument(cls, subparser):
        subparser.add_argument(
            "immunotherapy",
            help="the JSON of the immunotherapy")

    @classmethod
    def addCelltransplantNameArgument(cls, subparser):
        subparser.add_argument(
            "celltransplantName",
            help="the name of the celltransplant")

    @classmethod
    def addCelltransplantArgument(cls, subparser):
        subparser.add_argument(
            "celltransplant",
            help="the JSON of the celltransplant")

    @classmethod
    def addSlideNameArgument(cls, subparser):
        subparser.add_argument(
            "slideName",
            help="the name of the slide")

    @classmethod
    def addSlideArgument(cls, subparser):
        subparser.add_argument(
            "slide",
            help="the JSON of the slide")

    @classmethod
    def addStudyNameArgument(cls, subparser):
        subparser.add_argument(
            "studyName",
            help="the name of the study")

    @classmethod
    def addStudyArgument(cls, subparser):
        subparser.add_argument(
            "study",
            help="the JSON of the study")

    @classmethod
    def addLabtestNameArgument(cls, subparser):
        subparser.add_argument(
            "labtestName",
            help="the name of the labtest")

    @classmethod
    def addLabtestArgument(cls, subparser):
        subparser.add_argument(
            "labtest",
            help="the JSON of the labtest")

    @classmethod
    def addExtractionNameArgument(cls, subparser):
        subparser.add_argument(
            "extractionName",
            help="the name of the extraction")

    @classmethod
    def addExtractionArgument(cls, subparser):
        subparser.add_argument(
            "extraction",
            help="the JSON of the extraction")

    @classmethod
    def addSequencingNameArgument(cls, subparser):
        subparser.add_argument(
            "sequencingName",
            help="the name of the sequencing")

    @classmethod
    def addSequencingArgument(cls, subparser):
        subparser.add_argument(
            "sequencing",
            help="the JSON of the sequencing")

    @classmethod
    def addAlignmentNameArgument(cls, subparser):
        subparser.add_argument(
            "alignmentName",
            help="the name of the alignment")

    @classmethod
    def addAlignmentArgument(cls, subparser):
        subparser.add_argument(
            "alignment",
            help="the JSON of the alignment")

    @classmethod
    def addVariantCallingNameArgument(cls, subparser):
        subparser.add_argument(
            "variantCallingName",
            help="the name of the variantCalling")

    @classmethod
    def addVariantCallingArgument(cls, subparser):
        subparser.add_argument(
            "variantCalling",
            help="the JSON of the variantCalling")

    @classmethod
    def addFusionDetectionNameArgument(cls, subparser):
        subparser.add_argument(
            "fusionDetectionName",
            help="the name of the fusionDetection")

    @classmethod
    def addFusionDetectionArgument(cls, subparser):
        subparser.add_argument(
            "fusionDetection",
            help="the JSON of the fusionDetection")

    @classmethod
    def addExpressionAnalysisNameArgument(cls, subparser):
        subparser.add_argument(
            "expressionAnalysisName",
            help="the name of the expressionAnalysis")

    @classmethod
    def addExpressionAnalysisArgument(cls, subparser):
        subparser.add_argument(
            "expressionAnalysis",
            help="the JSON of the expressionAnalysis")

    @classmethod
    def addBiosampleNameArgument(cls, subparser):
        subparser.add_argument(
            "biosampleName",
            help="the name of the biosample")

    @classmethod
    def addBiosampleArgument(cls, subparser):
        subparser.add_argument(
            "biosample",
            help="the JSON of the biosample")

    @classmethod
    def addExperimentNameArgument(cls, subparser):
        subparser.add_argument(
            "experimentName",
            help="the name of the experiment")

    @classmethod
    def addExperimentArgument(cls, subparser):
        subparser.add_argument(
            "experiment",
            help="the JSON of the experiment")

    @classmethod
    def addAnalysisNameArgument(cls, subparser):
        subparser.add_argument(
            "analysisName",
            help="the name of the analysis")

    @classmethod
    def addAnalysisArgument(cls, subparser):
        subparser.add_argument(
            "analysis",
            help="the JSON of the analysis")

    @classmethod
    def addIndividualArgument(cls, subparser):
        subparser.add_argument(
            "individual",
            help="the JSON of the individual")

    @classmethod
    def addFilePathArgument(cls, subparser, helpText):
        subparser.add_argument("filePath", help=helpText)

    @classmethod
    def addDirPathArgument(cls, subparser, helpText):
        subparser.add_argument("dirPath", help=helpText)

    @classmethod
    def addNameOption(cls, parser, objectType):
        parser.add_argument(
            "-n", "--name", default=None,
            help="The name of the {}".format(objectType))

    @classmethod
    def addNameArgument(cls, parser, objectType):
        parser.add_argument(
            "name", help="The name of the {}".format(objectType))

    @classmethod
    def addRnaQuantificationNameArgument(cls, subparser):
        subparser.add_argument(
            "rnaQuantificationName",
            help="the name of the RNA Quantification")

    @classmethod
    def addClassNameOption(cls, subparser, objectType):
        helpText = (
            "the name of the class used to "
            "fetch features in this {}"
        ).format(objectType)
        subparser.add_argument(
            "-C", "--className",
            default="candig.datamodel.sequence_annotations.Gff3DbFeatureSet",
            help=helpText)

    @classmethod
    def addRnaQuantificationSetNameArgument(cls, subparser):
        subparser.add_argument(
            "rnaQuantificationSetName",
            help="the name of the RNA Quantification Set")

    @classmethod
    def addQuantificationFilePathArgument(cls, subparser, helpText):
        subparser.add_argument("quantificationFilePath", help=helpText)

    @classmethod
    def addRnaFormatArgument(cls, subparser):
        subparser.add_argument(
            "format", help="format of the quantification input data")

    @classmethod
    def addRnaFeatureTypeOption(cls, subparser):
        subparser.add_argument(
            "-t", "--transcript", action="store_true", default=False,
            help="sets the quantification type to transcript")

    @classmethod
    def getParser(cls):
        parser = common_cli.createArgumentParser(
            "GA4GH data repository management tool")
        subparsers = parser.add_subparsers(title='subcommands',)
        cli.addVersionArgument(parser)

        initParser = common_cli.addSubparser(
            subparsers, "init", "Initialize a data repository")
        initParser.set_defaults(runner="init")
        cls.addRepoArgument(initParser)
        cls.addForceOption(initParser)

        verifyParser = common_cli.addSubparser(
            subparsers, "verify",
            "Verifies the repository by examing all data files")
        verifyParser.set_defaults(runner="verify")
        cls.addRepoArgument(verifyParser)

        listParser = common_cli.addSubparser(
            subparsers, "list", "List the contents of the repo")
        listParser.set_defaults(runner="list")
        cls.addRepoArgument(listParser)

        listAnnouncementsParser = common_cli.addSubparser(
            subparsers, "list-announcements", "List the announcements in"
                                              "the repo.")
        listAnnouncementsParser.set_defaults(runner="listAnnouncements")
        cls.addRepoArgument(listAnnouncementsParser)

        clearAnnouncementsParser = common_cli.addSubparser(
            subparsers, "clear-announcements", "List the announcements in"
                                               "the repo.")
        clearAnnouncementsParser.set_defaults(runner="clearAnnouncements")
        cls.addRepoArgument(clearAnnouncementsParser)

        addPeerParser = common_cli.addSubparser(
            subparsers, "add-peer", "Add a peer to the registry by URL.")
        addPeerParser.set_defaults(runner="addPeer")
        cls.addRepoArgument(addPeerParser)
        cls.addUrlArgument(addPeerParser)
        cls.addAttributesArgument(addPeerParser)

        removePeerParser = common_cli.addSubparser(
            subparsers, "remove-peer", "Remove a peer from "
                                       "the registry by URL.")
        removePeerParser.set_defaults(runner="removePeer")
        cls.addRepoArgument(removePeerParser)
        cls.addUrlArgument(removePeerParser)
        cls.addForceOption(removePeerParser)

        removeAllPeersParser = common_cli.addSubparser(
            subparsers, "remove-peers", "Remove all peers from the registry.")
        removeAllPeersParser.set_defaults(runner="removePeers")
        cls.addRepoArgument(removeAllPeersParser)

        addDatasetParser = common_cli.addSubparser(
            subparsers, "add-dataset", "Add a dataset to the data repo")
        addDatasetParser.set_defaults(runner="addDataset")
        cls.addRepoArgument(addDatasetParser)
        cls.addDatasetNameArgument(addDatasetParser)
        cls.addAttributesArgument(addDatasetParser)
        cls.addDescriptionOption(addDatasetParser, "dataset")

        removeDatasetParser = common_cli.addSubparser(
            subparsers, "remove-dataset",
            "Remove a dataset from the data repo")
        removeDatasetParser.set_defaults(runner="removeDataset")
        cls.addRepoArgument(removeDatasetParser)
        cls.addDatasetNameArgument(removeDatasetParser)
        cls.addForceOption(removeDatasetParser)

        addExperimentParser = common_cli.addSubparser(
            subparsers, "add-experiment", "Add an experiment to the data repo")
        addExperimentParser.set_defaults(runner="addExperiment")
        cls.addRepoArgument(addExperimentParser)
        cls.addExperimentNameArgument(addExperimentParser)
        cls.addDescriptionOption(addExperimentParser, "Experiment description")
        cls.addExperimentArgument(addExperimentParser)

        removeExperimentParser = common_cli.addSubparser(
            subparsers, "remove-experiment",
            "Remove an experiment from the data repo")
        removeExperimentParser.set_defaults(runner="removeExperiment")
        cls.addRepoArgument(removeExperimentParser)
        cls.addExperimentNameArgument(removeExperimentParser)
        cls.addForceOption(removeExperimentParser)

        addAnalysisParser = common_cli.addSubparser(
            subparsers, "add-analysis", "Add an analysis to the data repo")
        addAnalysisParser.set_defaults(runner="addAnalysis")
        cls.addRepoArgument(addAnalysisParser)
        cls.addAnalysisNameArgument(addAnalysisParser)
        cls.addDescriptionOption(addAnalysisParser, "Analysis description")
        cls.addAnalysisArgument(addAnalysisParser)

        removeAnalysisParser = common_cli.addSubparser(
            subparsers, "remove-analysis",
            "Remove an analysis from the data repo")
        removeAnalysisParser.set_defaults(runner="removeAnalysis")
        cls.addRepoArgument(removeAnalysisParser)
        cls.addAnalysisNameArgument(removeAnalysisParser)
        cls.addForceOption(removeAnalysisParser)

        objectType = "reference set"
        addReferenceSetParser = common_cli.addSubparser(
            subparsers, "add-referenceset",
            "Add a reference set to the data repo")
        addReferenceSetParser.set_defaults(runner="addReferenceSet")
        cls.addRepoArgument(addReferenceSetParser)
        cls.addFilePathArgument(
            addReferenceSetParser,
            "The path of the FASTA file to use as a reference set. This "
            "file must be bgzipped and indexed.")
        cls.addAttributesArgument(addReferenceSetParser)
        cls.addRelativePathOption(addReferenceSetParser)
        cls.addNameOption(addReferenceSetParser, objectType)
        cls.addDescriptionOption(addReferenceSetParser, objectType)
        addReferenceSetParser.add_argument(
            "--species", default=None,
            help="The species ontology term as a JSON string")
        addReferenceSetParser.add_argument(
            "--isDerived", default=False, type=bool,
            help="Indicates if this reference set is derived from another")
        addReferenceSetParser.add_argument(
            "--assemblyId", default=None,
            help="The assembly id")
        addReferenceSetParser.add_argument(
            "--sourceAccessions", default=None,
            help="The source accessions (pass as comma-separated list)")
        addReferenceSetParser.add_argument(
            "--sourceUri", default=None,
            help="The source URI")

        removeReferenceSetParser = common_cli.addSubparser(
            subparsers, "remove-referenceset",
            "Remove a reference set from the repo")
        removeReferenceSetParser.set_defaults(runner="removeReferenceSet")
        cls.addRepoArgument(removeReferenceSetParser)
        removeReferenceSetParser.add_argument(
            "referenceSetName",
            help="the name of the reference set")
        cls.addForceOption(removeReferenceSetParser)

        objectType = "ReadGroupSet"
        addReadGroupSetParser = common_cli.addSubparser(
            subparsers, "add-readgroupset",
            "Add a read group set to the data repo")
        addReadGroupSetParser.set_defaults(runner="addReadGroupSet")
        cls.addRepoArgument(addReadGroupSetParser)
        cls.addDatasetNameArgument(addReadGroupSetParser)
        cls.addPatientIdArgument(addReadGroupSetParser)
        cls.addSampleIdArgument(addReadGroupSetParser)
        cls.addNameOption(addReadGroupSetParser, objectType)
        cls.addReferenceSetNameOption(addReadGroupSetParser, "ReadGroupSet")
        cls.addAttributesArgument(addReadGroupSetParser)
        cls.addRelativePathOption(addReadGroupSetParser)
        addReadGroupSetParser.add_argument(
            "dataFile",
            help="The file path or URL of the BAM file for this ReadGroupSet")
        addReadGroupSetParser.add_argument(
            "-I", "--indexFile", default=None,
            help=(
                "The file path of the BAM index for this ReadGroupSet. "
                "If the dataFile argument is a local file, this will "
                "be automatically inferred by appending '.bai' to the "
                "file name. If the dataFile is a remote URL the path to "
                "a local file containing the BAM index must be provided"))

        addOntologyParser = common_cli.addSubparser(
            subparsers, "add-ontology",
            "Adds an ontology in OBO format to the repo. Currently, "
            "a sequence ontology (SO) instance is required to translate "
            "ontology term names held in annotations to ontology IDs. "
            "Sequence ontology files can be found at "
            "https://github.com/The-Sequence-Ontology/SO-Ontologies")
        addOntologyParser.set_defaults(runner="addOntology")
        cls.addRepoArgument(addOntologyParser)
        cls.addFilePathArgument(
            addOntologyParser,
            "The path of the OBO file defining this ontology.")
        cls.addRelativePathOption(addOntologyParser)
        cls.addNameOption(addOntologyParser, "ontology")

        removeOntologyParser = common_cli.addSubparser(
            subparsers, "remove-ontology",
            "Remove an ontology from the repo")
        removeOntologyParser.set_defaults(runner="removeOntology")
        cls.addRepoArgument(removeOntologyParser)
        cls.addOntologyNameArgument(removeOntologyParser)
        cls.addForceOption(removeOntologyParser)

        removeReadGroupSetParser = common_cli.addSubparser(
            subparsers, "remove-readgroupset",
            "Remove a read group set from the repo")
        removeReadGroupSetParser.set_defaults(runner="removeReadGroupSet")
        cls.addRepoArgument(removeReadGroupSetParser)
        cls.addDatasetNameArgument(removeReadGroupSetParser)
        cls.addReadGroupSetNameArgument(removeReadGroupSetParser)
        cls.addForceOption(removeReadGroupSetParser)

        objectType = "VariantSet"
        addVariantSetParser = common_cli.addSubparser(
            subparsers, "add-variantset",
            "Add a variant set to the data repo based on one or "
            "more VCF files. ")
        addVariantSetParser.set_defaults(runner="addVariantSet")
        cls.addRepoArgument(addVariantSetParser)
        cls.addDatasetNameArgument(addVariantSetParser)
        cls.addPatientIdArgument(addVariantSetParser)
        cls.addSampleIdArgument(addVariantSetParser)
        cls.addRelativePathOption(addVariantSetParser)
        addVariantSetParser.add_argument(
            "dataFiles", nargs="+",
            help=(
                "The VCF/BCF files representing the new VariantSet. "
                "These may be specified either one or more paths "
                "to local files or remote URLS, or as a path to "
                "a local directory containing VCF files. Either "
                "a single directory argument may be passed or a "
                "list of file paths/URLS, but not a mixture of "
                "directories and paths.")
        )
        addVariantSetParser.add_argument(
            "-I", "--indexFiles", nargs="+", metavar="indexFiles",
            help=(
                "The index files for the VCF/BCF files provided in "
                "the dataFiles argument. These must be provided in the "
                "same order as the data files."
            )
        )
        cls.addNameOption(addVariantSetParser, objectType)
        cls.addReferenceSetNameOption(addVariantSetParser, objectType)
        cls.addSequenceOntologyNameOption(addVariantSetParser, objectType)
        cls.addAttributesArgument(addVariantSetParser)
        addVariantSetParser.add_argument(
            "-a", "--addAnnotationSets", action="store_true",
            help=(
                "If the supplied VCF file contains annotations, create the "
                "corresponding VariantAnnotationSet."))

        removeVariantSetParser = common_cli.addSubparser(
            subparsers, "remove-variantset",
            "Remove a variant set from the repo")
        removeVariantSetParser.set_defaults(runner="removeVariantSet")
        cls.addRepoArgument(removeVariantSetParser)
        cls.addDatasetNameArgument(removeVariantSetParser)
        cls.addVariantSetNameArgument(removeVariantSetParser)
        cls.addForceOption(removeVariantSetParser)

        addFeatureSetParser = common_cli.addSubparser(
            subparsers, "add-featureset", "Add a feature set to the data repo")
        addFeatureSetParser.set_defaults(runner="addFeatureSet")
        cls.addRepoArgument(addFeatureSetParser)
        cls.addDatasetNameArgument(addFeatureSetParser)
        cls.addAttributesArgument(addFeatureSetParser)
        cls.addRelativePathOption(addFeatureSetParser)
        cls.addFilePathArgument(
            addFeatureSetParser,
            "The path to the converted SQLite database containing Feature "
            "data")
        cls.addReferenceSetNameOption(addFeatureSetParser, "feature set")
        cls.addSequenceOntologyNameOption(addFeatureSetParser, "feature set")
        cls.addClassNameOption(addFeatureSetParser, "feature set")

        removeFeatureSetParser = common_cli.addSubparser(
            subparsers, "remove-featureset",
            "Remove a feature set from the repo")
        removeFeatureSetParser.set_defaults(runner="removeFeatureSet")
        cls.addRepoArgument(removeFeatureSetParser)
        cls.addDatasetNameArgument(removeFeatureSetParser)
        cls.addFeatureSetNameArgument(removeFeatureSetParser)
        cls.addForceOption(removeFeatureSetParser)

        addContinuousSetParser = common_cli.addSubparser(
            subparsers, "add-continuousset",
            "Add a continuous set to the data repo")
        addContinuousSetParser.set_defaults(runner="addContinuousSet")
        cls.addRepoArgument(addContinuousSetParser)
        cls.addDatasetNameArgument(addContinuousSetParser)
        cls.addRelativePathOption(addContinuousSetParser)
        cls.addFilePathArgument(
            addContinuousSetParser,
            "The path to the file contianing the continuous data ")
        cls.addReferenceSetNameOption(addContinuousSetParser, "continuous set")
        cls.addClassNameOption(addContinuousSetParser, "continuous set")

        removeContinuousSetParser = common_cli.addSubparser(
            subparsers, "remove-continuousset",
            "Remove a continuous set from the repo")
        removeContinuousSetParser.set_defaults(runner="removeContinuousSet")
        cls.addRepoArgument(removeContinuousSetParser)
        cls.addDatasetNameArgument(removeContinuousSetParser)
        cls.addContinuousSetNameArgument(removeContinuousSetParser)
        cls.addForceOption(removeContinuousSetParser)

        addBiosampleParser = common_cli.addSubparser(
            subparsers, "add-biosample", "Add a Biosample to the dataset")
        addBiosampleParser.set_defaults(runner="addBiosample")
        cls.addRepoArgument(addBiosampleParser)
        cls.addDatasetNameArgument(addBiosampleParser)
        cls.addBiosampleNameArgument(addBiosampleParser)
        cls.addBiosampleArgument(addBiosampleParser)

        removeBiosampleParser = common_cli.addSubparser(
            subparsers, "remove-biosample",
            "Remove a Biosample from the repo")
        removeBiosampleParser.set_defaults(runner="removeBiosample")
        cls.addRepoArgument(removeBiosampleParser)
        cls.addDatasetNameArgument(removeBiosampleParser)
        cls.addBiosampleNameArgument(removeBiosampleParser)
        cls.addForceOption(removeBiosampleParser)

        addIndividualParser = common_cli.addSubparser(
            subparsers, "add-individual", "Add an Individual to the dataset")
        addIndividualParser.set_defaults(runner="addIndividual")
        cls.addRepoArgument(addIndividualParser)
        cls.addDatasetNameArgument(addIndividualParser)
        cls.addIndividualNameArgument(addIndividualParser)
        cls.addIndividualArgument(addIndividualParser)

        removeIndividualParser = common_cli.addSubparser(
            subparsers, "remove-individual",
            "Remove an Individual from the repo")
        removeIndividualParser.set_defaults(runner="removeIndividual")
        cls.addRepoArgument(removeIndividualParser)
        cls.addDatasetNameArgument(removeIndividualParser)
        cls.addIndividualNameArgument(removeIndividualParser)
        cls.addForceOption(removeIndividualParser)

        addPatientParser = common_cli.addSubparser(
            subparsers, "add-patient", "Add an Patient to the dataset")
        addPatientParser.set_defaults(runner="addPatient")
        cls.addRepoArgument(addPatientParser)
        cls.addDatasetNameArgument(addPatientParser)
        cls.addPatientNameArgument(addPatientParser)
        cls.addPatientArgument(addPatientParser)

        removePatientParser = common_cli.addSubparser(
            subparsers, "remove-patient",
            "Remove an Patient from the repo")
        removePatientParser.set_defaults(runner="removePatient")
        cls.addRepoArgument(removePatientParser)
        cls.addDatasetNameArgument(removePatientParser)
        cls.addPatientNameArgument(removePatientParser)
        cls.addForceOption(removePatientParser)

        addEnrollmentParser = common_cli.addSubparser(
            subparsers, "add-enrollment", "Add an Enrollment to the dataset")
        addEnrollmentParser.set_defaults(runner="addEnrollment")
        cls.addRepoArgument(addEnrollmentParser)
        cls.addDatasetNameArgument(addEnrollmentParser)
        cls.addEnrollmentNameArgument(addEnrollmentParser)
        cls.addEnrollmentArgument(addEnrollmentParser)

        removeEnrollmentParser = common_cli.addSubparser(
            subparsers, "remove-enrollment",
            "Remove an Enrollment from the repo")
        removeEnrollmentParser.set_defaults(runner="removeEnrollment")
        cls.addRepoArgument(removeEnrollmentParser)
        cls.addDatasetNameArgument(removeEnrollmentParser)
        cls.addEnrollmentNameArgument(removeEnrollmentParser)
        cls.addForceOption(removeEnrollmentParser)

        addConsentParser = common_cli.addSubparser(
            subparsers, "add-consent", "Add an Consent to the dataset")
        addConsentParser.set_defaults(runner="addConsent")
        cls.addRepoArgument(addConsentParser)
        cls.addDatasetNameArgument(addConsentParser)
        cls.addConsentNameArgument(addConsentParser)
        cls.addConsentArgument(addConsentParser)

        removeConsentParser = common_cli.addSubparser(
            subparsers, "remove-consent",
            "Remove an Consent from the repo")
        removeConsentParser.set_defaults(runner="removeConsent")
        cls.addRepoArgument(removeConsentParser)
        cls.addDatasetNameArgument(removeConsentParser)
        cls.addConsentNameArgument(removeConsentParser)
        cls.addForceOption(removeConsentParser)

        addDiagnosisParser = common_cli.addSubparser(
            subparsers, "add-diagnosis", "Add an Diagnosis to the dataset")
        addDiagnosisParser.set_defaults(runner="addDiagnosis")
        cls.addRepoArgument(addDiagnosisParser)
        cls.addDatasetNameArgument(addDiagnosisParser)
        cls.addDiagnosisNameArgument(addDiagnosisParser)
        cls.addDiagnosisArgument(addDiagnosisParser)

        removeDiagnosisParser = common_cli.addSubparser(
            subparsers, "remove-diagnosis",
            "Remove an Diagnosis from the repo")
        removeDiagnosisParser.set_defaults(runner="removeDiagnosis")
        cls.addRepoArgument(removeDiagnosisParser)
        cls.addDatasetNameArgument(removeDiagnosisParser)
        cls.addDiagnosisNameArgument(removeDiagnosisParser)
        cls.addForceOption(removeDiagnosisParser)

        addSampleParser = common_cli.addSubparser(
            subparsers, "add-sample", "Add an Sample to the dataset")
        addSampleParser.set_defaults(runner="addSample")
        cls.addRepoArgument(addSampleParser)
        cls.addDatasetNameArgument(addSampleParser)
        cls.addSampleNameArgument(addSampleParser)
        cls.addSampleArgument(addSampleParser)

        removeSampleParser = common_cli.addSubparser(
            subparsers, "remove-sample",
            "Remove an Sample from the repo")
        removeSampleParser.set_defaults(runner="removeSample")
        cls.addRepoArgument(removeSampleParser)
        cls.addDatasetNameArgument(removeSampleParser)
        cls.addSampleNameArgument(removeSampleParser)
        cls.addForceOption(removeSampleParser)

        addTreatmentParser = common_cli.addSubparser(
            subparsers, "add-treatment", "Add an Treatment to the dataset")
        addTreatmentParser.set_defaults(runner="addTreatment")
        cls.addRepoArgument(addTreatmentParser)
        cls.addDatasetNameArgument(addTreatmentParser)
        cls.addTreatmentNameArgument(addTreatmentParser)
        cls.addTreatmentArgument(addTreatmentParser)

        removeTreatmentParser = common_cli.addSubparser(
            subparsers, "remove-treatment",
            "Remove an Treatment from the repo")
        removeTreatmentParser.set_defaults(runner="removeTreatment")
        cls.addRepoArgument(removeTreatmentParser)
        cls.addDatasetNameArgument(removeTreatmentParser)
        cls.addTreatmentNameArgument(removeTreatmentParser)
        cls.addForceOption(removeTreatmentParser)

        addOutcomeParser = common_cli.addSubparser(
            subparsers, "add-outcome", "Add an Outcome to the dataset")
        addOutcomeParser.set_defaults(runner="addOutcome")
        cls.addRepoArgument(addOutcomeParser)
        cls.addDatasetNameArgument(addOutcomeParser)
        cls.addOutcomeNameArgument(addOutcomeParser)
        cls.addOutcomeArgument(addOutcomeParser)

        removeOutcomeParser = common_cli.addSubparser(
            subparsers, "remove-outcome",
            "Remove an Outcome from the repo")
        removeOutcomeParser.set_defaults(runner="removeOutcome")
        cls.addRepoArgument(removeOutcomeParser)
        cls.addDatasetNameArgument(removeOutcomeParser)
        cls.addOutcomeNameArgument(removeOutcomeParser)
        cls.addForceOption(removeOutcomeParser)

        addComplicationParser = common_cli.addSubparser(
            subparsers, "add-complication", "Add an Complication to the dataset")
        addComplicationParser.set_defaults(runner="addComplication")
        cls.addRepoArgument(addComplicationParser)
        cls.addDatasetNameArgument(addComplicationParser)
        cls.addComplicationNameArgument(addComplicationParser)
        cls.addComplicationArgument(addComplicationParser)

        removeComplicationParser = common_cli.addSubparser(
            subparsers, "remove-complication",
            "Remove an Complication from the repo")
        removeComplicationParser.set_defaults(runner="removeComplication")
        cls.addRepoArgument(removeComplicationParser)
        cls.addDatasetNameArgument(removeComplicationParser)
        cls.addComplicationNameArgument(removeComplicationParser)
        cls.addForceOption(removeComplicationParser)

        addTumourboardParser = common_cli.addSubparser(
            subparsers, "add-tumourboard", "Add an Tumourboard to the dataset")
        addTumourboardParser.set_defaults(runner="addTumourboard")
        cls.addRepoArgument(addTumourboardParser)
        cls.addDatasetNameArgument(addTumourboardParser)
        cls.addTumourboardNameArgument(addTumourboardParser)
        cls.addTumourboardArgument(addTumourboardParser)

        removeTumourboardParser = common_cli.addSubparser(
            subparsers, "remove-tumourboard",
            "Remove an Tumourboard from the repo")
        removeTumourboardParser.set_defaults(runner="removeTumourboard")
        cls.addRepoArgument(removeTumourboardParser)
        cls.addDatasetNameArgument(removeTumourboardParser)
        cls.addTumourboardNameArgument(removeTumourboardParser)
        cls.addForceOption(removeTumourboardParser)

        addChemotherapyParser = common_cli.addSubparser(
            subparsers, "add-chemotherapy", "Add an Chemotherapy to the dataset")
        addChemotherapyParser.set_defaults(runner="addChemotherapy")
        cls.addRepoArgument(addChemotherapyParser)
        cls.addDatasetNameArgument(addChemotherapyParser)
        cls.addChemotherapyNameArgument(addChemotherapyParser)
        cls.addChemotherapyArgument(addChemotherapyParser)

        removeChemotherapyParser = common_cli.addSubparser(
            subparsers, "remove-chemotherapy",
            "Remove an Chemotherapy from the repo")
        removeChemotherapyParser.set_defaults(runner="removeChemotherapy")
        cls.addRepoArgument(removeChemotherapyParser)
        cls.addDatasetNameArgument(removeChemotherapyParser)
        cls.addChemotherapyNameArgument(removeChemotherapyParser)
        cls.addForceOption(removeChemotherapyParser)

        addRadiotherapyParser = common_cli.addSubparser(
            subparsers, "add-radiotherapy", "Add an Radiotherapy to the dataset")
        addRadiotherapyParser.set_defaults(runner="addRadiotherapy")
        cls.addRepoArgument(addRadiotherapyParser)
        cls.addDatasetNameArgument(addRadiotherapyParser)
        cls.addRadiotherapyNameArgument(addRadiotherapyParser)
        cls.addRadiotherapyArgument(addRadiotherapyParser)

        removeRadiotherapyParser = common_cli.addSubparser(
            subparsers, "remove-radiotherapy",
            "Remove an Radiotherapy from the repo")
        removeRadiotherapyParser.set_defaults(runner="removeRadiotherapy")
        cls.addRepoArgument(removeRadiotherapyParser)
        cls.addDatasetNameArgument(removeRadiotherapyParser)
        cls.addRadiotherapyNameArgument(removeRadiotherapyParser)
        cls.addForceOption(removeRadiotherapyParser)

        addSurgeryParser = common_cli.addSubparser(
            subparsers, "add-surgery", "Add an Surgery to the dataset")
        addSurgeryParser.set_defaults(runner="addSurgery")
        cls.addRepoArgument(addSurgeryParser)
        cls.addDatasetNameArgument(addSurgeryParser)
        cls.addSurgeryNameArgument(addSurgeryParser)
        cls.addSurgeryArgument(addSurgeryParser)

        removeSurgeryParser = common_cli.addSubparser(
            subparsers, "remove-surgery",
            "Remove an Surgery from the repo")
        removeSurgeryParser.set_defaults(runner="removeSurgery")
        cls.addRepoArgument(removeSurgeryParser)
        cls.addDatasetNameArgument(removeSurgeryParser)
        cls.addSurgeryNameArgument(removeSurgeryParser)
        cls.addForceOption(removeSurgeryParser)

        addImmunotherapyParser = common_cli.addSubparser(
            subparsers, "add-immunotherapy", "Add an Immunotherapy to the dataset")
        addImmunotherapyParser.set_defaults(runner="addImmunotherapy")
        cls.addRepoArgument(addImmunotherapyParser)
        cls.addDatasetNameArgument(addImmunotherapyParser)
        cls.addImmunotherapyNameArgument(addImmunotherapyParser)
        cls.addImmunotherapyArgument(addImmunotherapyParser)

        removeImmunotherapyParser = common_cli.addSubparser(
            subparsers, "remove-immunotherapy",
            "Remove an Immunotherapy from the repo")
        removeImmunotherapyParser.set_defaults(runner="removeImmunotherapy")
        cls.addRepoArgument(removeImmunotherapyParser)
        cls.addDatasetNameArgument(removeImmunotherapyParser)
        cls.addImmunotherapyNameArgument(removeImmunotherapyParser)
        cls.addForceOption(removeImmunotherapyParser)

        addCelltransplantParser = common_cli.addSubparser(
            subparsers, "add-celltransplant", "Add an Celltransplant to the dataset")
        addCelltransplantParser.set_defaults(runner="addCelltransplant")
        cls.addRepoArgument(addCelltransplantParser)
        cls.addDatasetNameArgument(addCelltransplantParser)
        cls.addCelltransplantNameArgument(addCelltransplantParser)
        cls.addCelltransplantArgument(addCelltransplantParser)

        removeCelltransplantParser = common_cli.addSubparser(
            subparsers, "remove-celltransplant",
            "Remove an Celltransplant from the repo")
        removeCelltransplantParser.set_defaults(runner="removeCelltransplant")
        cls.addRepoArgument(removeCelltransplantParser)
        cls.addDatasetNameArgument(removeCelltransplantParser)
        cls.addCelltransplantNameArgument(removeCelltransplantParser)
        cls.addForceOption(removeCelltransplantParser)

        addSlideParser = common_cli.addSubparser(
            subparsers, "add-slide", "Add an Slide to the dataset")
        addSlideParser.set_defaults(runner="addSlide")
        cls.addRepoArgument(addSlideParser)
        cls.addDatasetNameArgument(addSlideParser)
        cls.addSlideNameArgument(addSlideParser)
        cls.addSlideArgument(addSlideParser)

        removeSlideParser = common_cli.addSubparser(
            subparsers, "remove-slide",
            "Remove an Slide from the repo")
        removeSlideParser.set_defaults(runner="removeSlide")
        cls.addRepoArgument(removeSlideParser)
        cls.addDatasetNameArgument(removeSlideParser)
        cls.addSlideNameArgument(removeSlideParser)
        cls.addForceOption(removeSlideParser)

        addStudyParser = common_cli.addSubparser(
            subparsers, "add-study", "Add an Study to the dataset")
        addStudyParser.set_defaults(runner="addStudy")
        cls.addRepoArgument(addStudyParser)
        cls.addDatasetNameArgument(addStudyParser)
        cls.addStudyNameArgument(addStudyParser)
        cls.addStudyArgument(addStudyParser)

        removeStudyParser = common_cli.addSubparser(
            subparsers, "remove-study",
            "Remove an Study from the repo")
        removeStudyParser.set_defaults(runner="removeStudy")
        cls.addRepoArgument(removeStudyParser)
        cls.addDatasetNameArgument(removeStudyParser)
        cls.addStudyNameArgument(removeStudyParser)
        cls.addForceOption(removeStudyParser)

        addLabtestParser = common_cli.addSubparser(
            subparsers, "add-labtest", "Add an Labtest to the dataset")
        addLabtestParser.set_defaults(runner="addLabtest")
        cls.addRepoArgument(addLabtestParser)
        cls.addDatasetNameArgument(addLabtestParser)
        cls.addLabtestNameArgument(addLabtestParser)
        cls.addLabtestArgument(addLabtestParser)

        removeLabtestParser = common_cli.addSubparser(
            subparsers, "remove-labtest",
            "Remove an Labtest from the repo")
        removeLabtestParser.set_defaults(runner="removeLabtest")
        cls.addRepoArgument(removeLabtestParser)
        cls.addDatasetNameArgument(removeLabtestParser)
        cls.addLabtestNameArgument(removeLabtestParser)
        cls.addForceOption(removeLabtestParser)

        addExtractionParser = common_cli.addSubparser(
            subparsers, "add-extraction", "Add a Extraction to the dataset")
        addExtractionParser.set_defaults(runner="addExtraction")
        cls.addRepoArgument(addExtractionParser)
        cls.addDatasetNameArgument(addExtractionParser)
        cls.addExtractionNameArgument(addExtractionParser)
        cls.addExtractionArgument(addExtractionParser)

        removeExtractionParser = common_cli.addSubparser(
            subparsers, "remove-extraction",
            "Remove an Extraction from the repo")
        removeExtractionParser.set_defaults(runner="removeExtraction")
        cls.addRepoArgument(removeExtractionParser)
        cls.addDatasetNameArgument(removeExtractionParser)
        cls.addExtractionNameArgument(removeExtractionParser)
        cls.addForceOption(removeExtractionParser)

        addSequencingParser = common_cli.addSubparser(
            subparsers, "add-sequencing", "Add a Sequencing to the dataset")
        addSequencingParser.set_defaults(runner="addSequencing")
        cls.addRepoArgument(addSequencingParser)
        cls.addDatasetNameArgument(addSequencingParser)
        cls.addSequencingNameArgument(addSequencingParser)
        cls.addSequencingArgument(addSequencingParser)

        removeSequencingParser = common_cli.addSubparser(
            subparsers, "remove-sequencing",
            "Remove an Sequencing from the repo")
        removeSequencingParser.set_defaults(runner="removeSequencing")
        cls.addRepoArgument(removeSequencingParser)
        cls.addDatasetNameArgument(removeSequencingParser)
        cls.addSequencingNameArgument(removeSequencingParser)
        cls.addForceOption(removeSequencingParser)

        addAlignmentParser = common_cli.addSubparser(
            subparsers, "add-alignment", "Add a Alignment to the dataset")
        addAlignmentParser.set_defaults(runner="addAlignment")
        cls.addRepoArgument(addAlignmentParser)
        cls.addDatasetNameArgument(addAlignmentParser)
        cls.addAlignmentNameArgument(addAlignmentParser)
        cls.addAlignmentArgument(addAlignmentParser)

        removeAlignmentParser = common_cli.addSubparser(
            subparsers, "remove-alignment",
            "Remove an Alignment from the repo")
        removeAlignmentParser.set_defaults(runner="removeAlignment")
        cls.addRepoArgument(removeAlignmentParser)
        cls.addDatasetNameArgument(removeAlignmentParser)
        cls.addAlignmentNameArgument(removeAlignmentParser)
        cls.addForceOption(removeAlignmentParser)

        addVariantCallingParser = common_cli.addSubparser(
            subparsers, "add-variantcalling", "Add a VariantCalling to the dataset")
        addVariantCallingParser.set_defaults(runner="addVariantCalling")
        cls.addRepoArgument(addVariantCallingParser)
        cls.addDatasetNameArgument(addVariantCallingParser)
        cls.addVariantCallingNameArgument(addVariantCallingParser)
        cls.addVariantCallingArgument(addVariantCallingParser)

        removeVariantCallingParser = common_cli.addSubparser(
            subparsers, "remove-variantcalling",
            "Remove an VariantCalling from the repo")
        removeVariantCallingParser.set_defaults(runner="removeVariantCalling")
        cls.addRepoArgument(removeVariantCallingParser)
        cls.addDatasetNameArgument(removeVariantCallingParser)
        cls.addVariantCallingNameArgument(removeVariantCallingParser)
        cls.addForceOption(removeVariantCallingParser)

        addFusionDetectionParser = common_cli.addSubparser(
            subparsers, "add-fusiondetection", "Add a FusionDetection to the dataset")
        addFusionDetectionParser.set_defaults(runner="addFusionDetection")
        cls.addRepoArgument(addFusionDetectionParser)
        cls.addDatasetNameArgument(addFusionDetectionParser)
        cls.addFusionDetectionNameArgument(addFusionDetectionParser)
        cls.addFusionDetectionArgument(addFusionDetectionParser)

        removeFusionDetectionParser = common_cli.addSubparser(
            subparsers, "remove-fusiondetection",
            "Remove an FusionDetection from the repo")
        removeFusionDetectionParser.set_defaults(runner="removeFusionDetection")
        cls.addRepoArgument(removeFusionDetectionParser)
        cls.addDatasetNameArgument(removeFusionDetectionParser)
        cls.addFusionDetectionNameArgument(removeFusionDetectionParser)
        cls.addForceOption(removeFusionDetectionParser)

        addExpressionAnalysisParser = common_cli.addSubparser(
            subparsers, "add-expressionanalysis", "Add a ExpressionAnalysis to the dataset")
        addExpressionAnalysisParser.set_defaults(runner="addExpressionAnalysis")
        cls.addRepoArgument(addExpressionAnalysisParser)
        cls.addDatasetNameArgument(addExpressionAnalysisParser)
        cls.addExpressionAnalysisNameArgument(addExpressionAnalysisParser)
        cls.addExpressionAnalysisArgument(addExpressionAnalysisParser)

        removeExpressionAnalysisParser = common_cli.addSubparser(
            subparsers, "remove-expressionanalysis",
            "Remove an ExpressionAnalysis from the repo")
        removeExpressionAnalysisParser.set_defaults(runner="removeExpressionAnalysis")
        cls.addRepoArgument(removeExpressionAnalysisParser)
        cls.addDatasetNameArgument(removeExpressionAnalysisParser)
        cls.addExpressionAnalysisNameArgument(removeExpressionAnalysisParser)
        cls.addForceOption(removeExpressionAnalysisParser)

        objectType = "RnaQuantification"
        addRnaQuantificationParser = common_cli.addSubparser(
            subparsers, "add-rnaquantification",
            "Add an RNA quantification to the data repo")
        addRnaQuantificationParser.set_defaults(
            runner="addRnaQuantification")
        cls.addFilePathArgument(
            addRnaQuantificationParser,
            "The path to the RNA SQLite database to create or modify")
        cls.addQuantificationFilePathArgument(
            addRnaQuantificationParser, "The path to the expression file.")
        cls.addRnaFormatArgument(addRnaQuantificationParser)
        cls.addRepoArgument(addRnaQuantificationParser)
        cls.addDatasetNameArgument(addRnaQuantificationParser)
        addRnaQuantificationParser.add_argument(
            "--biosampleName", default=None, help="Biosample Name")
        addRnaQuantificationParser.add_argument(
            "--sampleId", default=None, help="SampleId")
        addRnaQuantificationParser.add_argument(
            "--patientId", default=None, help="PatientId")
        addRnaQuantificationParser.add_argument(
            "--readGroupSetName", default=None, help="Read Group Set Name")
        addRnaQuantificationParser.add_argument(
            "--featureSetNames", default=None, help="Comma separated list")
        cls.addNameOption(addRnaQuantificationParser, "rna quantification")
        cls.addDescriptionOption(addRnaQuantificationParser, objectType)
        cls.addRnaFeatureTypeOption(addRnaQuantificationParser)
        cls.addAttributesArgument(addRnaQuantificationParser)

        objectType = "RnaQuantificationSet"
        initRnaQuantificationSetParser = common_cli.addSubparser(
            subparsers, "init-rnaquantificationset",
            "Initializes an RNA quantification set")
        initRnaQuantificationSetParser.set_defaults(
            runner="initRnaQuantificationSet")
        cls.addRepoArgument(initRnaQuantificationSetParser)
        cls.addFilePathArgument(
            initRnaQuantificationSetParser,
            "The path to the resulting Quantification Set")

        addRnaQuantificationSetParser = common_cli.addSubparser(
            subparsers, "add-rnaquantificationset",
            "Add an RNA quantification set to the data repo")
        addRnaQuantificationSetParser.set_defaults(
            runner="addRnaQuantificationSet")
        cls.addRepoArgument(addRnaQuantificationSetParser)
        cls.addDatasetNameArgument(addRnaQuantificationSetParser)
        cls.addFilePathArgument(
            addRnaQuantificationSetParser,
            "The path to the converted SQLite database containing RNA data")
        cls.addReferenceSetNameOption(
            addRnaQuantificationSetParser, objectType)
        cls.addNameOption(addRnaQuantificationSetParser, objectType)
        cls.addAttributesArgument(addRnaQuantificationSetParser)

        removeRnaQuantificationSetParser = common_cli.addSubparser(
            subparsers, "remove-rnaquantificationset",
            "Remove an RNA quantification set from the repo")
        removeRnaQuantificationSetParser.set_defaults(
            runner="removeRnaQuantificationSet")
        cls.addRepoArgument(removeRnaQuantificationSetParser)
        cls.addDatasetNameArgument(removeRnaQuantificationSetParser)
        cls.addRnaQuantificationSetNameArgument(
            removeRnaQuantificationSetParser)
        cls.addForceOption(removeRnaQuantificationSetParser)

        addPhenotypeAssociationSetParser = common_cli.addSubparser(
            subparsers, "add-phenotypeassociationset",
            "Adds phenotypes in ttl format to the repo.")
        addPhenotypeAssociationSetParser.set_defaults(
            runner="addPhenotypeAssociationSet")
        cls.addRepoArgument(addPhenotypeAssociationSetParser)
        cls.addDatasetNameArgument(addPhenotypeAssociationSetParser)
        cls.addDirPathArgument(
            addPhenotypeAssociationSetParser,
            "The path of the directory containing ttl files.")
        cls.addNameOption(
            addPhenotypeAssociationSetParser,
            "PhenotypeAssociationSet")
        cls.addAttributesArgument(addPhenotypeAssociationSetParser)

        removePhenotypeAssociationSetParser = common_cli.addSubparser(
            subparsers, "remove-phenotypeassociationset",
            "Remove an phenotypes from the repo")
        removePhenotypeAssociationSetParser.set_defaults(
            runner="removePhenotypeAssociationSet")
        cls.addRepoArgument(removePhenotypeAssociationSetParser)
        cls.addDatasetNameArgument(removePhenotypeAssociationSetParser)
        cls.addNameArgument(
            removePhenotypeAssociationSetParser,
            "phenotype association set")
        cls.addForceOption(removePhenotypeAssociationSetParser)

        return parser

    @classmethod
    def runCommand(cls, args):
        parser = cls.getParser()
        parsedArgs = parser.parse_args(args)
        if "runner" not in parsedArgs:
            parser.print_help()
        manager = RepoManager(parsedArgs)
        runMethod = getattr(manager, parsedArgs.runner)
        runMethod()


def getRepoManagerParser():
    """
    Used by sphinx.argparse.
    """
    return RepoManager.getParser()


def repoExitError(message):
    """
    Exits the repo manager with error status.
    """
    wrapper = textwrap.TextWrapper(
        break_on_hyphens=False, break_long_words=False)
    formatted = wrapper.fill("{}: error: {}".format(sys.argv[0], message))
    sys.exit(formatted)


def repo_main(args=None):
    try:
        RepoManager.runCommand(args)
    except exceptions.RepoManagerException as exception:
        # These are exceptions that happen throughout the CLI, and are
        # used to communicate back to the user
        repoExitError(str(exception))
    except exceptions.NotFoundException as exception:
        # We expect NotFoundExceptions to occur when we're looking for
        # datasets, readGroupsets, etc.
        repoExitError(str(exception))
    except exceptions.DataException as exception:
        # We expect DataExceptions to occur when a file open fails,
        # a URL cannot be reached, etc.
        repoExitError(str(exception))
    except Exception as exception:
        # Uncaught exception: this is a bug
        message = """
An internal error has occurred.  Please file a bug report at
https://github.com/candig/candig-server/issues
with all the relevant details, and the following stack trace.
"""
        print("{}: error:".format(sys.argv[0]), file=sys.stderr)
        print(message, file=sys.stderr)
        traceback.print_exception(*sys.exc_info())
        sys.exit(1)
