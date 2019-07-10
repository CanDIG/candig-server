"""
The backing data store for the GA4GH server
"""

import json
import os
import datetime

import candig.server.datamodel as datamodel
import candig.server.datamodel.datasets as datasets
import candig.server.datamodel.ontologies as ontologies
import candig.server.datamodel.reads as reads
import candig.server.datamodel.references as references
import candig.server.datamodel.variants as variants
import candig.server.datamodel.sequence_annotations as sequence_annotations
import candig.server.datamodel.continuous as continuous
import candig.server.datamodel.bio_metadata as biodata
import candig.server.datamodel.genotype_phenotype as genotype_phenotype
import candig.server.datamodel.genotype_phenotype_featureset as g2pFeatureset
import candig.server.datamodel.rna_quantification as rna_quantification
import candig.server.datamodel.peers as peers
import candig.server.exceptions as exceptions
import candig.server.repo.models as models
import candig.server.datamodel.clinical_metadata as clinical_metadata
import candig.server.datamodel.pipeline_metadata as pipeline_metadata

import candig.schemas.protocol as protocol

MODE_READ = 'r'
MODE_WRITE = 'w'


class AbstractDataRepository(object):
    """
    An abstract GA4GH data repository
    """
    def __init__(self):
        self._datasetIdMap = {}
        self._datasetNameMap = {}
        self._datasetIds = []
        self._referenceSetIdMap = {}
        self._referenceSetNameMap = {}
        self._referenceSetIds = []
        self._ontologyNameMap = {}
        self._ontologyIdMap = {}
        self._ontologyIds = []
        self._peers = []
        # these should eventually be "in" datasets, if not biosamples
        # but will have to change the schema first
        self._experimentIds = []
        self._experimentNameMap = {}
        self._experimentIdMap = {}
        self._analysisIds = []
        self._analysisNameMap = {}
        self._analysisIdMap = {}

    def addDataset(self, dataset):
        """
        Adds the specified dataset to this data repository.
        """
        id_ = dataset.getId()
        self._datasetIdMap[id_] = dataset
        self._datasetNameMap[dataset.getLocalId()] = dataset
        self._datasetIds.append(id_)

    def addExperiment(self, experiment):
        """
        Adds the specified experiment to this data repository.
        """
        id_ = experiment.getId()
        self._experimentIdMap[id_] = experiment
        self._experimentNameMap[experiment.getLocalId()] = experiment
        self._experimentIds.append(id_)

    def addAnalysis(self, analysis):
        """
        Adds the specified analysis to this data repository.
        """
        id_ = analysis.getId()
        self._analysisIdMap[id_] = analysis
        self._analysisNameMap[analysis.getLocalId()] = analysis
        self._analysisIds.append(id_)

    def addReferenceSet(self, referenceSet):
        """
        Adds the specified reference set to this data repository.
        """
        id_ = referenceSet.getId()
        self._referenceSetIdMap[id_] = referenceSet
        self._referenceSetNameMap[referenceSet.getLocalId()] = referenceSet
        self._referenceSetIds.append(id_)

    def addOntology(self, ontology):
        """
        Add an ontology map to this data repository.
        """
        self._ontologyNameMap[ontology.getName()] = ontology
        self._ontologyIdMap[ontology.getId()] = ontology
        self._ontologyIds.append(ontology.getId())

    def getDatasets(self):
        """
        Returns a list of datasets in this data repository
        """
        return [self._datasetIdMap[id_] for id_ in self._datasetIds]

    def getExperiments(self):
        """
        Returns a list of datasets in this data repository
        """
        return [self._experimentIdMap[id_] for id_ in self._experimentIds]

    def getAnalyses(self):
        """
        Returns a list of datasets in this data repository
        """
        return [self._analysisIdMap[id_] for id_ in self._analysisIds]

    def insertPeer(self, peer):
        """
        Adds a peer to the list of peers in the repository. Used only in
        testing.
        """
        self._peers.append(peer)

    def getPeer(self, url):
        """
        Select the first peer in the datarepo with the given url simulating
        the behavior of selecting by URL. This is only used during testing.
        """
        peers = [x for x in self.getPeers() if x.getUrl() == url]
        if len(peers) == 0:
            raise exceptions.PeerNotFoundException(url)
        return peers[0]

    def getPeers(self, offset=0, limit=100):
        """
        Returns the list of peers with an optional offset and limit
        simulating the SQL registry for testing.
        """
        return self._peers[offset:offset + limit]

    def insertAnnouncement(self, announcement):
        """
        A placeholder function to simulate receiving an announcement used
        in testing. It will throw an exception if the URL is invalid.
        """
        peers.Peer(announcement.get('url'))

    def getNumDatasets(self):
        """
        Returns the number of datasets in this data repository.
        """
        return len(self._datasetIds)

    def getDataset(self, id_):
        """
        Returns a dataset with the specified ID, or raises a
        DatasetNotFoundException if it does not exist.
        """
        if id_ not in self._datasetIdMap:
            raise exceptions.DatasetNotFoundException(id_)
        return self._datasetIdMap[id_]

    def getDatasetByIndex(self, index):
        """
        Returns the dataset at the specified index.
        """
        return self._datasetIdMap[self._datasetIds[index]]

    def getAuthzDatasetByIndex(self, index, access_map):
        """
        Returns the dataset at the specified index if authorized to do so
        """
        dataset = self._datasetIdMap[self._datasetIds[index]]
        dataset_name = dataset.getLocalId()

        return dataset if dataset_name in access_map else None

    def getDatasetByName(self, name):
        """
        Returns the dataset with the specified name.
        """
        if name not in self._datasetNameMap:
            raise exceptions.DatasetNameNotFoundException(name)
        return self._datasetNameMap[name]

    def getExperiment(self, id_):
        """
        Returns a experiment with the specified ID, or raises a
        ExperimentNotFoundException if it does not exist.
        """
        if id_ not in self._experimentIdMap:
            raise exceptions.ExperimentNotFoundException(id_)
        return self._experimentIdMap[id_]

    def getNumExperiments(self):
        """
        Returns the number of experiments in this data repository.
        """
        return len(self._experimentIds)

    def getExperimentByIndex(self, index):
        """
        Returns the experiment at the specified index.
        """
        return self._experimentIdMap[self._experimentIds[index]]

    def getExperimentByName(self, name):
        """
        Returns the experiment with the specified name.
        """
        if name not in self._experimentNameMap:
            raise exceptions.ExperimentNameNotFoundException(name)
        return self._experimentNameMap[name]

    def getAnalysis(self, id_):
        """
        Returns a analysis with the specified ID, or raises a
        AnalysisNotFoundException if it does not exist.
        """
        if id_ not in self._analysisIdMap:
            raise exceptions.AnalysisNotFoundException(id_)
        return self._analysisIdMap[id_]

    def getNumAnalyses(self):
        """
        Returns the number of analyses in this data repository.
        """
        return len(self._analysisIds)

    def getAnalysisByIndex(self, index):
        """
        Returns the analysis at the specified index.
        """
        return self._analysisIdMap[self._analysisIds[index]]

    def getAnalysisByName(self, name):
        """
        Returns the analysis with the specified name.
        """
        if name not in self._analysisNameMap:
            raise exceptions.AnalysisNameNotFoundException(name)
        return self._analysisNameMap[name]

    def getReferenceSets(self):
        """
        Returns the list of ReferenceSets in this data repository
        """
        return [self._referenceSetIdMap[id_] for id_ in self._referenceSetIds]

    def getNumReferenceSets(self):
        """
        Returns the number of reference sets in this data repository.
        """
        return len(self._referenceSetIds)

    def getOntology(self, id_):
        """
        Returns the ontology with the specified ID.
        """
        if id_ not in self._ontologyIdMap:
            raise exceptions.OntologyNotFoundException(id_)
        return self._ontologyIdMap[id_]

    def getOntologyByName(self, name):
        """
        Returns an ontology by name
        """
        if name not in self._ontologyNameMap:
            raise exceptions.OntologyNameNotFoundException(name)
        return self._ontologyNameMap[name]

    def getOntologys(self):
        """
        Returns all ontologys in the repo
        """
        return [self._ontologyIdMap[id_] for id_ in self._ontologyIds]

    def getReferenceSet(self, id_):
        """
        Retuns the ReferenceSet with the specified ID, or raises a
        ReferenceSetNotFoundException if it does not exist.
        """
        if id_ not in self._referenceSetIdMap:
            raise exceptions.ReferenceSetNotFoundException(id_)
        return self._referenceSetIdMap[id_]

    def getReferenceSetByIndex(self, index):
        """
        Returns the reference set at the specified index.
        """
        return self._referenceSetIdMap[self._referenceSetIds[index]]

    def getReferenceSetByName(self, name):
        """
        Returns the reference set with the specified name.
        """
        if name not in self._referenceSetNameMap:
            raise exceptions.ReferenceSetNameNotFoundException(name)
        return self._referenceSetNameMap[name]

    def getReadGroupSet(self, id_):
        """
        Returns the readgroup set with the specified ID.
        """
        compoundId = datamodel.ReadGroupSetCompoundId.parse(id_)
        dataset = self.getDataset(compoundId.dataset_id)
        return dataset.getReadGroupSet(id_)

    def getVariantSet(self, id_):
        """
        Returns the readgroup set with the specified ID.
        """
        compoundId = datamodel.VariantSetCompoundId.parse(id_)
        dataset = self.getDataset(compoundId.dataset_id)
        return dataset.getVariantSet(id_)

    def printSummary(self):
        """
        Prints a summary of this data repository to stdout.
        """
        print("Ontologies:")
        for ontology in self.getOntologys():
            print(
                "",
                ontology.getOntologyPrefix(),
                ontology.getName(),
                ontology.getDataUrl(),
                sep="\t")
        print("ReferenceSets:")
        for referenceSet in self.getReferenceSets():
            print(
                "", referenceSet.getLocalId(), referenceSet.getId(),
                referenceSet.getDescription(), referenceSet.getDataUrl(),
                sep="\t")
            for reference in referenceSet.getReferences():
                print(
                    "\t", reference.getLocalId(), reference.getId(),
                    sep="\t")
        print("Datasets:")
        for dataset in self.getDatasets():
            print(
                "", dataset.getLocalId(), dataset.getId(),
                dataset.getDescription(), sep="\t")
            print("\tReadGroupSets:")
            for readGroupSet in dataset.getReadGroupSets():
                print(
                    "\t", readGroupSet.getLocalId(),
                    readGroupSet.getReferenceSet().getLocalId(),
                    readGroupSet.getId(),
                    readGroupSet.getDataUrl(), sep="\t")
                for readGroup in readGroupSet.getReadGroups():
                    print(
                        "\t\t", readGroup.getId(), readGroup.getLocalId(),
                        sep="\t")
            print("\tVariantSets:")
            for variantSet in dataset.getVariantSets():
                print(
                    "\t", variantSet.getLocalId(),
                    variantSet.getReferenceSet().getLocalId(),
                    variantSet.getId(),
                    sep="\t")
                if variantSet.getNumVariantAnnotationSets() > 0:
                    print("\t\tVariantAnnotationSets:")
                    for vas in variantSet.getVariantAnnotationSets():
                        print(
                            "\t\t", vas.getLocalId(),
                            vas.getAnnotationType(),
                            vas.getOntology().getName(), sep="\t")
            print("\tFeatureSets:")
            for featureSet in dataset.getFeatureSets():
                print(
                    "\t", featureSet.getLocalId(),
                    featureSet.getReferenceSet().getLocalId(),
                    featureSet.getOntology().getName(),
                    featureSet.getId(),
                    sep="\t")
            print("\tContinuousSets:")
            for continuousSet in dataset.getContinuousSets():
                print(
                    "\t", continuousSet.getLocalId(),
                    continuousSet.getReferenceSet().getLocalId(),
                    continuousSet.getId(),
                    sep="\t")
            print("\tPhenotypeAssociationSets:")
            for phenotypeAssociationSet in \
                    dataset.getPhenotypeAssociationSets():
                print(
                    "\t", phenotypeAssociationSet.getLocalId(),
                    phenotypeAssociationSet.getParentContainer().getId(),
                    sep="\t")
                # TODO -  please improve this listing
            print("\tRnaQuantificationSets:")
            for rna_quantification_set in dataset.getRnaQuantificationSets():
                print(
                    "\t", rna_quantification_set.getLocalId(),
                    rna_quantification_set.getId(), sep="\t")
                for quant in rna_quantification_set.getRnaQuantifications():
                        print(
                            "\t\t", quant.getLocalId(),
                            quant._description,
                            ",".join(quant._readGroupIds),
                            ",".join(quant._featureSetIds), sep="\t")
        print("Experiments:")
        for experiment in self.getExperiments():
            print(
                "", experiment.getLocalId(), experiment.getId(),
                experiment.getName(), experiment.getDescription(), sep="\t")

        print("Analyses:")
        for analysis in self.getAnalyses():
            print(
                "", analysis.getLocalId(), analysis.getId(),
                analysis.getName(), analysis.getDescription(), sep="\t")

    def allReferences(self):
        """
        Return an iterator over all references in the data repo
        """
        for referenceSet in self.getReferenceSets():
            for reference in referenceSet.getReferences():
                yield reference

    def allBiosamples(self):
        """
        Return an iterator over all biosamples in the data repo
        """
        for dataset in self.getDatasets():
            for biosample in dataset.getBiosamples():
                yield biosample

    def allIndividuals(self):
        """
        Return an iterator over all individuals in the data repo
        """
        for dataset in self.getDatasets():
            for individual in dataset.getIndividuals():
                yield individual

    def allPatient(self):
        """
        Return an iterator over all Patient in the data repo
        """
        for dataset in self.getDatasets():
            for patient in dataset.getPatient():
                yield patient

    def allEnrollment(self):
        """
        Return an iterator over all Enrollment in the data repo
        """
        for dataset in self.getDatasets():
            for enrollment in dataset.getEnrollment():
                yield enrollment

    def allConsent(self):
        """
        Return an iterator over all Consent in the data repo
        """
        for dataset in self.getDatasets():
            for consent in dataset.getConsent():
                yield consent

    def allDiagnosis(self):
        """
        Return an iterator over all Diagnosis in the data repo
        """
        for dataset in self.getDatasets():
            for diagnosis in dataset.getDiagnosis():
                yield diagnosis

    def allSample(self):
        """
        Return an iterator over all Sample in the data repo
        """
        for dataset in self.getDatasets():
            for sample in dataset.getSample():
                yield sample

    def allTreatment(self):
        """
        Return an iterator over all Treatment in the data repo
        """
        for dataset in self.getDatasets():
            for treatment in dataset.getTreatment():
                yield treatment

    def allOutcome(self):
        """
        Return an iterator over all Outcome in the data repo
        """
        for dataset in self.getDatasets():
            for outcome in dataset.getOutcome():
                yield outcome

    def allComplication(self):
        """
        Return an iterator over all Complication in the data repo
        """
        for dataset in self.getDatasets():
            for complication in dataset.getComplication():
                yield complication

    def allTumourboard(self):
        """
        Return an iterator over all Tumourboard in the data repo
        """
        for dataset in self.getDatasets():
            for tumourboard in dataset.getTumourboard():
                yield tumourboard

    def allChemotherapy(self):
        """
        Return an iterator over all Chemotherapy in the data repo
        """
        for dataset in self.getDatasets():
            for chemotherapy in dataset.getChemotherapy():
                yield chemotherapy

    def allRadiotherapy(self):
        """
        Return an iterator over all Radiotherapy in the data repo
        """
        for dataset in self.getDatasets():
            for radiotherapy in dataset.getRadiotherapy():
                yield radiotherapy

    def allSurgery(self):
        """
        Return an iterator over all Surgery in the data repo
        """
        for dataset in self.getDatasets():
            for surgery in dataset.getSurgery():
                yield surgery

    def allImmunotherapy(self):
        """
        Return an iterator over all Immunotherapy in the data repo
        """
        for dataset in self.getDatasets():
            for immunotherapy in dataset.getImmunotherapy():
                yield immunotherapy

    def allCelltransplant(self):
        """
        Return an iterator over all Celltransplant in the data repo
        """
        for dataset in self.getDatasets():
            for celltransplant in dataset.getCelltransplant():
                yield celltransplant

    def allSlide(self):
        """
        Return an iterator over all Slide in the data repo
        """
        for dataset in self.getDatasets():
            for slide in dataset.getSlide():
                yield slide

    def allStudy(self):
        """
        Return an iterator over all Study in the data repo
        """
        for dataset in self.getDatasets():
            for study in dataset.getStudy():
                yield study

    def allLabtest(self):
        """
        Return an iterator over all Labtest in the data repo
        """
        for dataset in self.getDatasets():
            for labtest in dataset.getLabtest():
                yield labtest

    def allReadGroupSets(self):
        """
        Return an iterator over all read group sets in the data repo
        """
        for dataset in self.getDatasets():
            for readGroupSet in dataset.getReadGroupSets():
                yield readGroupSet

    def allReadGroups(self):
        """
        Return an iterator over all read groups in the data repo
        """
        for dataset in self.getDatasets():
            for readGroupSet in dataset.getReadGroupSets():
                for readGroup in readGroupSet.getReadGroups():
                    yield readGroup

    def allVariantSets(self):
        """
        Return an iterator over all read variant sets in the data repo
        """
        for dataset in self.getDatasets():
            for variantSet in dataset.getVariantSets():
                yield variantSet

    def allFeatureSets(self):
        """
        Return an iterator over all feature sets in the data repo
        """
        for dataset in self.getDatasets():
            for featureSet in dataset.getFeatureSets():
                yield featureSet

    def allFeatures(self):
        """
        Return an iterator over all features in the data repo
        """
        for dataset in self.getDatasets():
            for featureSet in dataset.getFeatureSets():
                for feature in featureSet.getFeatures():
                    yield feature

    def allContinuousSets(self):
        """
        Return an iterator over all continuous sets in the data repo
        """
        for dataset in self.getDatasets():
            for continuousSet in dataset.getContinuousSets():
                yield continuousSet

    def allCallSets(self):
        """
        Return an iterator over all call sets in the data repo
        """
        for dataset in self.getDatasets():
            for variantSet in dataset.getVariantSets():
                for callSet in variantSet.getCallSets():
                    yield callSet

    def allVariantAnnotationSets(self):
        """
        Return an iterator over all variant annotation sets
        in the data repo
        """
        for dataset in self.getDatasets():
            for variantSet in dataset.getVariantSets():
                for vaSet in variantSet.getVariantAnnotationSets():
                    yield vaSet

    def allPhenotypeAssociationSets(self):
        """
        Return an iterator over all phenotype association sets
        in the data repo
        """
        for dataset in self.getDatasets():
            for paSet in dataset.getPhenotypeAssociationSets():
                yield paSet

    def allRnaQuantificationSets(self):
        """
        Return an iterator over all rna quantification sets
        """
        for dataset in self.getDatasets():
            for rnaQuantificationSet in dataset.getRnaQuantificationSets():
                yield rnaQuantificationSet

    def allRnaQuantifications(self):
        """
        Return an iterator over all rna quantifications
        """
        for dataset in self.getDatasets():
            for rnaQuantificationSet in dataset.getRnaQuantificationSets():
                for rnaQuantification in \
                        rnaQuantificationSet.getRnaQuantifications():
                    yield rnaQuantification

    def allExpressionLevels(self):
        """
        Return an iterator over all expression levels
        """
        for dataset in self.getDatasets():
            for rnaQuantificationSet in dataset.getRnaQuantificationSets():
                for rnaQuantification in \
                        rnaQuantificationSet.getRnaQuantifications():
                    for expressionLevel in \
                            rnaQuantification.getExpressionLevels():
                        yield expressionLevel


class EmptyDataRepository(AbstractDataRepository):
    """
    A data repository that contains no data
    """
    def __init__(self):
        super(EmptyDataRepository, self).__init__()


class SimulatedDataRepository(AbstractDataRepository):
    """
    A data repository that is simulated
    """
    def __init__(
            self, randomSeed=0, numDatasets=2,
            numVariantSets=1, numCalls=1, variantDensity=0.5,
            numReferenceSets=1, numReferencesPerReferenceSet=1,
            numReadGroupSets=1, numReadGroupsPerReadGroupSet=1,
            numPhenotypeAssociations=2,
            numPhenotypeAssociationSets=1,
            numAlignments=2, numRnaQuantSets=2, numExpressionLevels=2,
            numPeers=1):
        super(SimulatedDataRepository, self).__init__()
        for i in range(numPeers):
            peer = peers.Peer("http://test{}.org".format(i))
            self.insertPeer(peer)

        # References
        for i in range(numReferenceSets):
            localId = "referenceSet{}".format(i)
            seed = randomSeed + i
            referenceSet = references.SimulatedReferenceSet(
                localId, seed, numReferencesPerReferenceSet)
            self.addReferenceSet(referenceSet)

        # Datasets
        for i in range(numDatasets):
            seed = randomSeed + i
            localId = "simulatedDataset{}".format(i)
            referenceSet = self.getReferenceSetByIndex(i % numReferenceSets)
            dataset = datasets.SimulatedDataset(
                localId, referenceSet=referenceSet, randomSeed=seed,
                numCalls=numCalls, variantDensity=variantDensity,
                numVariantSets=numVariantSets,
                numReadGroupSets=numReadGroupSets,
                numReadGroupsPerReadGroupSet=numReadGroupsPerReadGroupSet,
                numAlignments=numAlignments,
                numPhenotypeAssociations=numPhenotypeAssociations,
                numPhenotypeAssociationSets=numPhenotypeAssociationSets,
                numRnaQuantSets=numRnaQuantSets,
                numExpressionLevels=numExpressionLevels)
            self.addDataset(dataset)


class SqlDataRepository(AbstractDataRepository):
    """
    A data repository based on a SQL database.
    """
    class SchemaVersion(object):
        """
        The version of the data repository SQL schema
        """
        def __init__(self, versionString):
            splits = versionString.split('.')
            assert len(splits) == 2
            self.major = splits[0]
            self.minor = splits[1]

        def __str__(self):
            return "{}.{}".format(self.major, self.minor)

    version = SchemaVersion("2.1")
    systemKeySchemaVersion = "schemaVersion"
    systemKeyCreationTimeStamp = "creationTimeStamp"

    def __init__(self, fileName):
        super(SqlDataRepository, self).__init__()
        self._dbFilename = fileName
        # We open the repo in either read or write mode. When we want to
        # update the repo we open it in write mode. For normal online
        # server use, we open it in read mode.
        self._openMode = None
        # Values filled in using the DB. These will all be None until
        # we have called load()
        self._schemaVersion = None
        # Connection to the DB.
        self.database = models.SqliteDatabase(self._dbFilename, **{})
        models.databaseProxy.initialize(self.database)

    def _checkWriteMode(self):
        if self._openMode != MODE_WRITE:
            raise ValueError("Repo must be opened in write mode")

    def getPeer(self, url):
        """
        Finds a peer by URL and return the first peer record with that URL.
        """
        peers = list(models.Peer.select().where(models.Peer.url == url))
        if len(peers) == 0:
            raise exceptions.PeerNotFoundException(url)
        return peers[0]

    def getPeers(self, offset=0, limit=1000):
        """
        Get the list of peers using an SQL offset and limit. Returns a list
        of peer datamodel objects in a list.
        """
        select = models.Peer.select().order_by(
            models.Peer.url).limit(limit).offset(offset)
        return [peers.Peer(p.url, record=p) for p in select]

    def tableToTsv(self, model):
        """
        Takes a model class and attempts to create a table in TSV format
        that can be imported into a spreadsheet program.
        """
        first = True
        for item in model.select():
            if first:
                header = "".join(
                    ["{}\t".format(x) for x in model._meta.fields.keys()])
                print(header)
                first = False
            row = "".join(
                ["{}\t".format(
                    getattr(item, key)) for key in model._meta.fields.keys()])
            print(row)

    def printAnnouncements(self):
        """
        Prints the announcement table to the log in tsv format.
        """
        self.tableToTsv(models.Announcement)

    def clearAnnouncements(self):
        """
        Flushes the announcement table.
        """
        try:
            q = models.Announcement.delete().where(
                models.Announcement.id > 0)
            q.execute()
        except Exception as e:
            raise exceptions.RepoManagerException(e)

    def insertAnnouncement(self, announcement):
        """
        Adds an announcement to the registry for later analysis.
        """
        url = announcement.get('url', None)
        try:
            peers.Peer(url)
        except:
            raise exceptions.BadUrlException(url)
        try:
            # TODO get more details about the user agent
            models.Announcement.create(
                url=announcement.get('url'),
                attributes=json.dumps(announcement.get('attributes', {})),
                remote_addr=announcement.get('remote_addr', None),
                user_agent=announcement.get('user_agent', None))
        except Exception as e:
            raise exceptions.RepoManagerException(e)

    def open(self, mode=MODE_READ):
        """
        Opens this repo in the specified mode.

        TODO: figure out the correct semantics of this and document
        the intended future behaviour as well as the current
        transitional behaviour.
        """
        if mode not in [MODE_READ, MODE_WRITE]:
            error = "Open mode must be '{}' or '{}'".format(
                MODE_READ, MODE_WRITE)
            raise ValueError(error)
        self._openMode = mode
        if mode == MODE_READ:
            self.assertExists()
        if mode == MODE_READ:
            # This is part of the transitional behaviour where
            # we load the whole DB into memory to get access to
            # the data model.
            self.load()

    def commit(self):
        """
        Commits any changes made to the repo. It is an error to call
        this function if the repo is not opened in write-mode.
        """
        self._checkWriteMode()

    def close(self):
        """
        Closes this repo.
        """
        if self._openMode is None:
            raise ValueError("Repo already closed")
        self._openMode = None

    def verify(self):
        """
        Verifies that the data in the repository is consistent.
        """
        #
        # TODO - verify experiments (but probably wait until they
        # reside, properly, in datasets/biosamples)
        #
        # TODO this should emit to a log that we can configure so we can
        # have verbosity levels. We should provide a way to configure
        # where we look at various chromosomes and so on. This will be
        # an important debug tool for administrators.
        for ontology in self.getOntologys():
            print(
                "Verifying Ontology", ontology.getName(),
                "@", ontology.getDataUrl())
            # TODO how do we verify this? Check some well-know SO terms?
        # TODO: how do we verify the experiments
        for experiment in self.getExperiments():
            print("Not really verifying Expt", experiment.getName())
        for analysis in self.getAnalyses():
            print("Not really verifying Analysis", analysis.getName())
        for referenceSet in self.getReferenceSets():
            print(
                "Verifying ReferenceSet", referenceSet.getLocalId(),
                "@", referenceSet.getDataUrl())
            for reference in referenceSet.getReferences():
                length = min(reference.getLength(), 1000)
                bases = reference.getBases(0, length)
                assert len(bases) == length
                print(
                    "\tReading", length, "bases from",
                    reference.getLocalId())
        for dataset in self.getDatasets():
            print("Verifying Dataset", dataset.getLocalId())
            for featureSet in dataset.getFeatureSets():
                for referenceSet in self.getReferenceSets():
                    # TODO cycle through references?
                    reference = referenceSet.getReferences()[0]
                    print(
                        "\tVerifying FeatureSet",
                        featureSet.getLocalId(),
                        "with reference", reference.getLocalId())
                    length = min(reference.getLength(), 1000)
                    features = featureSet.getFeatures(
                        reference.getLocalId(), 0, length, None, 3)
                    for feature in features:
                        print("\t{}".format(feature))
            # for continuousSet in dataset.getContinuousSets():
            # -- there is no getContinuous
            for readGroupSet in dataset.getReadGroupSets():
                print(
                    "\tVerifying ReadGroupSet", readGroupSet.getLocalId(),
                    "@", readGroupSet.getDataUrl())
                references = readGroupSet.getReferenceSet().getReferences()
                # TODO should we cycle through the references? Should probably
                # be an option.
                reference = references[0]
                max_alignments = 10
                for readGroup in readGroupSet.getReadGroups():
                    alignments = readGroup.getReadAlignments(reference)
                    for i, alignment in enumerate(alignments):
                        if i == max_alignments:
                            break
                    print(
                        "\t\tRead", i, "alignments from",
                        readGroup.getLocalId())
            for variantSet in dataset.getVariantSets():
                print("\tVerifying VariantSet", variantSet.getLocalId())
                max_variants = 10
                max_annotations = 10
                refMap = variantSet.getReferenceToDataUrlIndexMap()
                for referenceName, (dataUrl, indexFile) in list(refMap.items()):
                    variants = variantSet.getVariants(referenceName, 0, 2**31)
                    for i, variant in enumerate(variants):
                        if i == max_variants:
                            break
                    print(
                        "\t\tRead", i, "variants from reference",
                        referenceName, "@", dataUrl)
                for annotationSet in variantSet.getVariantAnnotationSets():
                    print(
                        "\t\tVerifying VariantAnnotationSet",
                        annotationSet.getLocalId())
                    for referenceName in list(refMap.keys()):
                        annotations = annotationSet.getVariantAnnotations(
                            referenceName, 0, 2**31)
                        for i, annotation in enumerate(annotations):
                            if i == max_annotations:
                                break
                    print(
                        "\t\t\tRead", i, "annotations from reference",
                        referenceName)
            for phenotypeAssociationSet \
                    in dataset.getPhenotypeAssociationSets():
                print("\t\tVerifying PhenotypeAssociationSet")
                print(
                    "\t\t\t", phenotypeAssociationSet.getLocalId(),
                    phenotypeAssociationSet.getParentContainer().getId(),
                    sep="\t")
                # TODO - please improve this verification,
                #        print out number of tuples in graph

    def _createSystemTable(self):
        self.database.create_table(models.System)
        models.System.create(
            key=self.systemKeySchemaVersion, value=self.version)
        models.System.create(
            key=self.systemKeyCreationTimeStamp, value=datetime.datetime.now())

    def _readSystemTable(self):
        if not self.exists():
            raise exceptions.RepoNotFoundException(
                self._dbFilename)
        try:
            self._schemaVersion = models.System.get(
                models.System.key == self.systemKeySchemaVersion).value
        except Exception:
            raise exceptions.RepoInvalidDatabaseException(self._dbFilename)
        schemaVersion = self.SchemaVersion(self._schemaVersion)
        if schemaVersion.major != self.version.major:
            raise exceptions.RepoSchemaVersionMismatchException(
                schemaVersion, self.version)

    def _createOntologyTable(self):
        self.database.create_table(models.Ontology)

    def insertOntology(self, ontology):
        """
        Inserts the specified ontology into this repository.
        """
        try:
            models.Ontology.create(
                id=ontology.getName(),
                name=ontology.getName(),
                dataurl=ontology.getDataUrl(),
                ontologyprefix=ontology.getOntologyPrefix())
        except Exception:
            raise exceptions.DuplicateNameException(
                ontology.getName())
        # TODO we need to create a proper ID when we're doing ID generation
        # for the rest of the container objects.

    def _readOntologyTable(self):
        for ont in models.Ontology.select():
            ontology = ontologies.Ontology(ont.name)
            ontology.populateFromRow(ont)
            self.addOntology(ontology)

    def removeOntology(self, ontology):
        """
        Removes the specified ontology term map from this repository.
        """
        q = models.Ontology.delete().where(id == ontology.getId())
        q.execute()

    def _createReferenceTable(self):
        self.database.create_table(models.Reference)

    def insertReference(self, reference):
        """
        Inserts the specified reference into this repository.
        """
        models.Reference.create(
            id=reference.getId(),
            referencesetid=reference.getParentContainer().getId(),
            name=reference.getLocalId(),
            length=reference.getLength(),
            isderived=reference.getIsDerived(),
            species=json.dumps(reference.getSpecies()),
            md5checksum=reference.getMd5Checksum(),
            sourceaccessions=json.dumps(reference.getSourceAccessions()),
            sourceuri=reference.getSourceUri())

    def _readReferenceTable(self):
        for referenceRecord in models.Reference.select():
            referenceSet = self.getReferenceSet(
                referenceRecord.referencesetid.id)
            reference = references.HtslibReference(
                referenceSet, referenceRecord.name)
            reference.populateFromRow(referenceRecord)
            assert reference.getId() == referenceRecord.id
            referenceSet.addReference(reference)

    def _createReferenceSetTable(self):
        self.database.create_table(models.Referenceset)

    def insertReferenceSet(self, referenceSet):
        """
        Inserts the specified referenceSet into this repository.
        """
        try:
            models.Referenceset.create(
                id=referenceSet.getId(),
                name=referenceSet.getLocalId(),
                description=referenceSet.getDescription(),
                assemblyid=referenceSet.getAssemblyId(),
                isderived=referenceSet.getIsDerived(),
                species=json.dumps(referenceSet.getSpecies()),
                md5checksum=referenceSet.getMd5Checksum(),
                sourceaccessions=json.dumps(
                    referenceSet.getSourceAccessions()),
                sourceuri=referenceSet.getSourceUri(),
                dataurl=referenceSet.getDataUrl())
            for reference in referenceSet.getReferences():
                self.insertReference(reference)
        except Exception:
            raise exceptions.DuplicateNameException(
                referenceSet.getLocalId())

    def _readReferenceSetTable(self):
        for referenceSetRecord in models.Referenceset.select():
            referenceSet = references.HtslibReferenceSet(
                referenceSetRecord.name)
            referenceSet.populateFromRow(referenceSetRecord)
            assert referenceSet.getId() == referenceSetRecord.id
            # Insert the referenceSet into the memory-based object model.
            self.addReferenceSet(referenceSet)

    def _createDatasetTable(self):
        self.database.create_table(models.Dataset)

    def insertDataset(self, dataset):
        """
        Inserts the specified dataset into this repository.
        """
        try:
            models.Dataset.create(
                id=dataset.getId(),
                name=dataset.getLocalId(),
                description=dataset.getDescription(),
                attributes=json.dumps(dataset.getAttributes()))
        except Exception:
            raise exceptions.DuplicateNameException(
                dataset.getLocalId())

    def removeDataset(self, dataset):
        """
        Removes the specified dataset from this repository. This performs
        a cascading removal of all items within this dataset.
        """
        for datasetRecord in models.Dataset.select().where(
                models.Dataset.id == dataset.getId()):
                    datasetRecord.delete_instance(recursive=True)

    def removePhenotypeAssociationSet(self, phenotypeAssociationSet):
        """
        Remove a phenotype association set from the repo
        """
        q = models.Phenotypeassociationset.delete().where(
            models.Phenotypeassociationset.id ==
            phenotypeAssociationSet.getId())
        q.execute()

    def removeFeatureSet(self, featureSet):
        """
        Removes the specified featureSet from this repository.
        """
        q = models.Featureset.delete().where(
            models.Featureset.id == featureSet.getId())
        q.execute()

    def removeContinuousSet(self, continuousSet):
        """
        Removes the specified continuousSet from this repository.
        """
        q = models.ContinuousSet.delete().where(
            models.ContinuousSet.id == continuousSet.getId())
        q.execute()

    def _readDatasetTable(self):
        for datasetRecord in models.Dataset.select():
            dataset = datasets.Dataset(datasetRecord.name)
            dataset.populateFromRow(datasetRecord)
            assert dataset.getId() == datasetRecord.id
            # Insert the dataset into the memory-based object model.
            self.addDataset(dataset)

    def _createReadGroupTable(self):
        self.database.create_table(models.Readgroup)

    def insertReadGroup(self, readGroup):
        """
        Inserts the specified readGroup into the DB.
        """
        statsJson = json.dumps(protocol.toJsonDict(readGroup.getStats()))
        experimentJson = json.dumps(
            protocol.toJsonDict(readGroup.getExperiment()))
        try:
            models.Readgroup.create(
                id=readGroup.getId(),
                readgroupsetid=readGroup.getParentContainer().getId(),
                name=readGroup.getLocalId(),
                predictedinsertedsize=readGroup.getPredictedInsertSize(),
                samplename=readGroup.getSampleName(),
                description=readGroup.getDescription(),
                experiment=experimentJson,
                stats=statsJson,
                biosampleid=readGroup.getBiosampleId(),
                attributes=json.dumps(readGroup.getAttributes()))
        except Exception as e:
            raise exceptions.RepoManagerException(e)

    def removeReadGroupSet(self, readGroupSet):
        """
        Removes the specified readGroupSet from this repository. This performs
        a cascading removal of all items within this readGroupSet.
        """
        for readGroupSetRecord in models.Readgroupset.select().where(
                models.Readgroupset.id == readGroupSet.getId()):
                    readGroupSetRecord.delete_instance(recursive=True)

    def removeVariantSet(self, variantSet):
        """
        Removes the specified variantSet from this repository. This performs
        a cascading removal of all items within this variantSet.
        """
        for variantSetRecord in models.Variantset.select().where(
                models.Variantset.id == variantSet.getId()):
                    variantSetRecord.delete_instance(recursive=True)

    def removeBiosample(self, biosample):
        """
        Removes the specified biosample from this repository.
        """
        q = models.Biosample.delete().where(
            models.Biosample.id == biosample.getId())
        q.execute()

    def removeExperiment(self, experiment):
        """
        Removes the specified experiment from this repository.
        """
        q = models.Experiment.delete().where(
            models.Experiment.id == experiment.getId())
        q.execute()

    def removeAnalysis(self, analysis):
        """
        Removes the specified analysis from this repository.
        """
        q = models.Analysis.delete().where(
            models.Analysis.id == analysis.getId())
        q.execute()

    def removeIndividual(self, individual):
        """
        Removes the specified individual from this repository.
        """
        q = models.Individual.delete().where(
            models.Individual.id == individual.getId())
        q.execute()

    def removePatient(self, patient):
        """
        Removes the specified patient from this repository.
        """
        q = models.Patient.delete().where(
            models.Patient.id == patient.getId())
        q.execute()

    def removeEnrollment(self, enrollment):
        """
        Removes the specified enrollment from this repository.
        """
        q = models.Enrollment.delete().where(
            models.Enrollment.id == enrollment.getId())
        q.execute()

    def removeConsent(self, consent):
        """
        Removes the specified consent from this repository.
        """
        q = models.Consent.delete().where(
            models.Consent.id == consent.getId())
        q.execute()

    def removeDiagnosis(self, diagnosis):
        """
        Removes the specified diagnosis from this repository.
        """
        q = models.Diagnosis.delete().where(
            models.Diagnosis.id == diagnosis.getId())
        q.execute()

    def removeSample(self, sample):
        """
        Removes the specified sample from this repository.
        """
        q = models.Sample.delete().where(
            models.Sample.id == sample.getId())
        q.execute()

    def removeTreatment(self, treatment):
        """
        Removes the specified treatment from this repository.
        """
        q = models.Treatment.delete().where(
            models.Treatment.id == treatment.getId())
        q.execute()

    def removeOutcome(self, outcome):
        """
        Removes the specified outcome from this repository.
        """
        q = models.Outcome.delete().where(
            models.Outcome.id == outcome.getId())
        q.execute()

    def removeComplication(self, complication):
        """
        Removes the specified complication from this repository.
        """
        q = models.Complication.delete().where(
            models.Complication.id == complication.getId())
        q.execute()

    def removeTumourboard(self, tumourboard):
        """
        Removes the specified tumourboard from this repository.
        """
        q = models.Tumourboard.delete().where(
            models.Tumourboard.id == tumourboard.getId())
        q.execute()

    def removeChemotherapy(self, chemotherapy):
        """
        Removes the specified chemotherapy from this repository.
        """
        q = models.Chemotherapy.delete().where(
            models.Chemotherapy.id == chemotherapy.getId())
        q.execute()

    def removeRadiotherapy(self, radiotherapy):
        """
        Removes the specified radiotherapy from this repository.
        """
        q = models.Radiotherapy.delete().where(
            models.Radiotherapy.id == radiotherapy.getId())
        q.execute()

    def removeSurgery(self, surgery):
        """
        Removes the specified surgery from this repository.
        """
        q = models.Surgery.delete().where(
            models.Surgery.id == surgery.getId())
        q.execute()

    def removeImmunotherapy(self, immunotherapy):
        """
        Removes the specified immunotherapy from this repository.
        """
        q = models.Immunotherapy.delete().where(
            models.Immunotherapy.id == immunotherapy.getId())
        q.execute()

    def removeCelltransplant(self, celltransplant):
        """
        Removes the specified celltransplant from this repository.
        """
        q = models.Celltransplant.delete().where(
            models.Celltransplant.id == celltransplant.getId())
        q.execute()

    def removeSlide(self, slide):
        """
        Removes the specified slide from this repository.
        """
        q = models.Slide.delete().where(
            models.Slide.id == slide.getId())
        q.execute()

    def removeStudy(self, study):
        """
        Removes the specified study from this repository.
        """
        q = models.Study.delete().where(
            models.Study.id == study.getId())
        q.execute()

    def removeLabtest(self, labtest):
        """
        Removes the specified labtest from this repository.
        """
        q = models.Labtest.delete().where(
            models.Labtest.id == labtest.getId())
        q.execute()

    def removeExtraction(self, extraction):
        """
        Removes the specified diagnosis from this repository.
        """
        q = models.Extraction.delete().where(
            models.Extraction.id == extraction.getId())
        q.execute()

    def removeSequencing(self, sequencing):
        """
        Removes the specified sample from this repository.
        """
        q = models.Sequencing.delete().where(
            models.Sequencing.id == sequencing.getId())
        q.execute()

    def removeAlignment(self, alignment):
        """
        Removes the specified treatment from this repository.
        """
        q = models.Alignment.delete().where(
            models.Alignment.id == alignment.getId())
        q.execute()

    def removeVariantCalling(self, variantCalling):
        """
        Removes the specified outcome from this repository.
        """
        q = models.VariantCalling.delete().where(
            models.VariantCalling.id == variantCalling.getId())
        q.execute()

    def removeFusionDetection(self, fusionDetection):
        """
        Removes the specified complication from this repository.
        """
        q = models.FusionDetection.delete().where(
            models.FusionDetection.id == fusionDetection.getId())
        q.execute()

    def removeExpressionAnalysis(self, expressionAnalysis):
        """
        Removes the specified tumourboard from this repository.
        """
        q = models.ExpressionAnalysis.delete().where(
            models.ExpressionAnalysis.id == expressionAnalysis.getId())
        q.execute()

    def _readReadGroupTable(self):
        for readGroupRecord in models.Readgroup.select():
            readGroupSet = self.getReadGroupSet(
                readGroupRecord.readgroupsetid.id)
            readGroup = reads.HtslibReadGroup(
                readGroupSet, readGroupRecord.name)
            # TODO set the reference set.
            readGroup.populateFromRow(readGroupRecord)
            assert readGroup.getId() == readGroupRecord.id
            # Insert the readGroupSet into the memory-based object model.
            readGroupSet.addReadGroup(readGroup)

    def _createReadGroupSetTable(self):
        self.database.create_table(models.Readgroupset)

    def insertReadGroupSet(self, readGroupSet):
        """
        Inserts a the specified readGroupSet into this repository.
        """
        programsJson = json.dumps(
            [protocol.toJsonDict(program) for program in
             readGroupSet.getPrograms()])
        statsJson = json.dumps(protocol.toJsonDict(readGroupSet.getStats()))
        try:
            models.Readgroupset.create(
                id=readGroupSet.getId(),
                datasetid=readGroupSet.getParentContainer().getId(),
                referencesetid=readGroupSet.getReferenceSet().getId(),
                name=readGroupSet.getLocalId(),
                patientId=readGroupSet.getPatientId(),
                sampleId=readGroupSet.getSampleId(),
                programs=programsJson,
                stats=statsJson,
                dataurl=readGroupSet.getDataUrl(),
                indexfile=readGroupSet.getIndexFile(),
                attributes=json.dumps(readGroupSet.getAttributes()))
            for readGroup in readGroupSet.getReadGroups():
                self.insertReadGroup(readGroup)
        except Exception as e:
            raise exceptions.RepoManagerException(e)

    def removeReferenceSet(self, referenceSet):
        """
        Removes the specified referenceSet from this repository. This performs
        a cascading removal of all references within this referenceSet.
        However, it does not remove any of the ReadGroupSets or items that
        refer to this ReferenceSet. These must be deleted before the
        referenceSet can be removed.
        """
        try:
            q = models.Reference.delete().where(
                models.Reference.referencesetid == referenceSet.getId())
            q.execute()
            q = models.Referenceset.delete().where(
                models.Referenceset.id == referenceSet.getId())
            q.execute()
        except Exception:
            msg = ("Unable to delete reference set.  "
                   "There are objects currently in the registry which are "
                   "aligned against it.  Remove these objects before removing "
                   "the reference set.")
            raise exceptions.RepoManagerException(msg)

    def _readReadGroupSetTable(self):
        for readGroupSetRecord in models.Readgroupset.select():
            dataset = self.getDataset(readGroupSetRecord.datasetid.id)
            readGroupSet = reads.HtslibReadGroupSet(
                dataset, readGroupSetRecord.name)
            referenceSet = self.getReferenceSet(
                readGroupSetRecord.referencesetid.id)
            readGroupSet.setReferenceSet(referenceSet)
            readGroupSet.populateFromRow(readGroupSetRecord)
            assert readGroupSet.getId() == readGroupSetRecord.id
            # Insert the readGroupSet into the memory-based object model.
            dataset.addReadGroupSet(readGroupSet)

    def _createVariantAnnotationSetTable(self):
        self.database.create_table(models.Variantannotationset)

    def insertVariantAnnotationSet(self, variantAnnotationSet):
        """
        Inserts a the specified variantAnnotationSet into this repository.
        """
        analysisJson = json.dumps(
            protocol.toJsonDict(variantAnnotationSet.getAnalysis()))
        try:
            models.Variantannotationset.create(
                id=variantAnnotationSet.getId(),
                variantsetid=variantAnnotationSet.getParentContainer().getId(),
                ontologyid=variantAnnotationSet.getOntology().getId(),
                name=variantAnnotationSet.getLocalId(),
                analysis=analysisJson,
                annotationtype=variantAnnotationSet.getAnnotationType(),
                created=variantAnnotationSet.getCreationTime(),
                updated=variantAnnotationSet.getUpdatedTime(),
                attributes=json.dumps(variantAnnotationSet.getAttributes()))
        except Exception as e:
            raise exceptions.RepoManagerException(e)

    def _readVariantAnnotationSetTable(self):
        for annotationSetRecord in models.Variantannotationset.select():
            variantSet = self.getVariantSet(
                annotationSetRecord.variantsetid.id)
            ontology = self.getOntology(annotationSetRecord.ontologyid.id)
            variantAnnotationSet = variants.HtslibVariantAnnotationSet(
                variantSet, annotationSetRecord.name)
            variantAnnotationSet.setOntology(ontology)
            variantAnnotationSet.populateFromRow(annotationSetRecord)
            assert variantAnnotationSet.getId() == annotationSetRecord.id
            # Insert the variantAnnotationSet into the memory-based model.
            variantSet.addVariantAnnotationSet(variantAnnotationSet)

    def _createCallSetTable(self):
        self.database.create_table(models.Callset)

    def insertCallSet(self, callSet):
        """
        Inserts a the specified callSet into this repository.
        """
        try:
            models.Callset.create(
                id=callSet.getId(),
                name=callSet.getLocalId(),
                variantsetid=callSet.getParentContainer().getId(),
                biosampleid=callSet.getBiosampleId(),
                attributes=json.dumps(callSet.getAttributes()))
        except Exception as e:
            raise exceptions.RepoManagerException(e)

    def _readCallSetTable(self):
        for callSetRecord in models.Callset.select():
            variantSet = self.getVariantSet(callSetRecord.variantsetid.id)
            callSet = variants.CallSet(variantSet, callSetRecord.name)
            callSet.populateFromRow(callSetRecord)
            assert callSet.getId() == callSetRecord.id
            # Insert the callSet into the memory-based object model.
            variantSet.addCallSet(callSet)

    def _createVariantSetTable(self):
        self.database.create_table(models.Variantset)

    def insertVariantSet(self, variantSet):
        """
        Inserts a the specified variantSet into this repository.
        """
        # We cheat a little here with the VariantSetMetadata, and encode these
        # within the table as a JSON dump. These should really be stored in
        # their own table
        metadataJson = json.dumps(
            [protocol.toJsonDict(metadata) for metadata in
             variantSet.getMetadata()])
        urlMapJson = json.dumps(variantSet.getReferenceToDataUrlIndexMap())
        try:
            models.Variantset.create(
                id=variantSet.getId(),
                datasetid=variantSet.getParentContainer().getId(),
                referencesetid=variantSet.getReferenceSet().getId(),
                name=variantSet.getLocalId(),
                created=datetime.datetime.now(),
                updated=datetime.datetime.now(),
                metadata=metadataJson,
                dataurlindexmap=urlMapJson,
                patientId = variantSet.getPatientId(),
                sampleId = variantSet.getSampleId(),
                attributes=json.dumps(variantSet.getAttributes()))
        except Exception as e:
            raise exceptions.RepoManagerException(e)
        for callSet in variantSet.getCallSets():
            self.insertCallSet(callSet)

    def _readVariantSetTable(self):
        for variantSetRecord in models.Variantset.select():
            dataset = self.getDataset(variantSetRecord.datasetid.id)
            referenceSet = self.getReferenceSet(
                variantSetRecord.referencesetid.id)
            variantSet = variants.HtslibVariantSet(
                dataset, variantSetRecord.name)
            variantSet.setReferenceSet(referenceSet)
            variantSet.populateFromRow(variantSetRecord)
            assert variantSet.getId() == variantSetRecord.id
            # Insert the variantSet into the memory-based object model.
            dataset.addVariantSet(variantSet)

    def _createFeatureSetTable(self):
        self.database.create_table(models.Featureset)

    def insertFeatureSet(self, featureSet):
        """
        Inserts a the specified featureSet into this repository.
        """
        # TODO add support for info and sourceUri fields.
        try:
            models.Featureset.create(
                id=featureSet.getId(),
                datasetid=featureSet.getParentContainer().getId(),
                referencesetid=featureSet.getReferenceSet().getId(),
                ontologyid=featureSet.getOntology().getId(),
                name=featureSet.getLocalId(),
                dataurl=featureSet.getDataUrl(),
                attributes=json.dumps(featureSet.getAttributes()))
        except Exception as e:
            raise exceptions.RepoManagerException(e)

    def _readFeatureSetTable(self):
        for featureSetRecord in models.Featureset.select():
            dataset = self.getDataset(featureSetRecord.datasetid.id)
            # FIXME this should be handled elsewhere
            if 'cgd' in featureSetRecord.name:
                featureSet = \
                    g2pFeatureset \
                    .PhenotypeAssociationFeatureSet(
                        dataset, featureSetRecord.name)
            else:
                featureSet = sequence_annotations.Gff3DbFeatureSet(
                    dataset, featureSetRecord.name)
            featureSet.setReferenceSet(
                self.getReferenceSet(
                    featureSetRecord.referencesetid.id))
            featureSet.setOntology(
                self.getOntology(featureSetRecord.ontologyid.id))
            featureSet.populateFromRow(featureSetRecord)
            assert featureSet.getId() == featureSetRecord.id
            dataset.addFeatureSet(featureSet)

    def _createContinuousSetTable(self):
        self.database.create_table(models.ContinuousSet)

    def insertContinuousSet(self, continuousSet):
        """
        Inserts a the specified continuousSet into this repository.
        """
        # TODO add support for info and sourceUri fields.
        try:
            models.ContinuousSet.create(
                id=continuousSet.getId(),
                datasetid=continuousSet.getParentContainer().getId(),
                referencesetid=continuousSet.getReferenceSet().getId(),
                name=continuousSet.getLocalId(),
                dataurl=continuousSet.getDataUrl(),
                attributes=json.dumps(continuousSet.getAttributes()))
        except Exception as e:
            raise exceptions.RepoManagerException(e)

    def _readContinuousSetTable(self):
        for continuousSetRecord in models.ContinuousSet.select():
            dataset = self.getDataset(continuousSetRecord.datasetid.id)
            continuousSet = continuous.FileContinuousSet(
                dataset, continuousSetRecord.name)
            continuousSet.setReferenceSet(
                self.getReferenceSet(
                    continuousSetRecord.referencesetid.id))
            continuousSet.populateFromRow(continuousSetRecord)
            assert continuousSet.getId() == continuousSetRecord.id
            dataset.addContinuousSet(continuousSet)

    def _createBiosampleTable(self):
        self.database.create_table(models.Biosample)

    def _createExperimentTable(self):
        self.database.create_table(models.Experiment)

    def insertBiosample(self, biosample):
        """
        Inserts the specified Biosample into this repository.
        """
        try:
            models.Biosample.create(
                id=biosample.getId(),
                datasetid=biosample.getParentContainer().getId(),
                name=biosample.getLocalId(),
                description=biosample.getDescription(),
                disease=json.dumps(biosample.getDisease()),
                created=biosample.getCreated(),
                updated=biosample.getUpdated(),
                individualid=biosample.getIndividualId(),
                attributes=json.dumps(biosample.getAttributes()),
                individualAgeAtCollection=json.dumps(
                    biosample.getIndividualAgeAtCollection()),
                estimated_tumor_content = biosample.getEstimatedTumorContent(),
                normal_sample_source = biosample.getNormalSampleSource(),
                biopsy_data = biosample.getBiopsyData(),
                tumor_biopsy_anatomical_site = biosample.getTumorBiopsyAnatomicalSite(),
                biopsy_type = biosample.getBiopsyType(),
                sample_shipment_date = biosample.getSampleShipmentDate(),
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                biosample.getLocalId(),
                biosample.getParentContainer().getLocalId())

    def _readBiosampleTable(self):
        for biosampleRecord in models.Biosample.select():
            dataset = self.getDataset(biosampleRecord.datasetid.id)
            biosample = biodata.Biosample(
                dataset, biosampleRecord.name)
            biosample.populateFromRow(biosampleRecord)
            assert biosample.getId() == biosampleRecord.id
            dataset.addBiosample(biosample)

    def insertExperiment(self, experiment):
        """
        Inserts the specified Experiment into this repository.
        """
        try:
            models.Experiment.create(
                id=experiment.getId(),
                name=experiment.getName(),
                description=experiment.getDescription(),
                created=experiment.getCreated(),
                updated=experiment.getUpdated(),
                run_time=experiment.getRunTime(),
                molecule=experiment.getMolecule(),
                strategy=experiment.getStrategy(),
                selection=experiment.getSelection(),
                library=experiment.getLibrary(),
                libraryLayout=experiment.getLibraryLayout(),
                instrumentModel=experiment.getInstrumentModel(),
                instrumentData_file=experiment.getInstrumentDataFile(),
                sequencingCenter=experiment.getSequencingCenter(),
                platformUnit=experiment.getPlatformUnit(),
                attributes=json.dumps(experiment.getAttributes()),
                datasetId=experiment.getParentContainer().getId(),
                biosample_id = experiment.getBiosampleId(),
                dna_library_construction_method = experiment.getDnaLibraryConstructionMethod(),
                wgs_sequencing_completion_date = experiment.getWgsSequencingCompletionDate(),
                rna_library_construction_method = experiment.getRnaLibraryConstructionMethod(),
                rna_sequencing_completion_date = experiment.getRnaSequencingCompletionDate(),
                panel_completion_date = experiment.getPanelCompletionDate(),
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                experiment.getLocalId(), None)

    def _readExperimentTable(self):
        for experimentRecord in models.Experiment.select():
            dataset = self.getDataset(experimentRecord.datasetid.id)
            experiment = biodata.Experiment(dataset, experimentRecord.name)
            experiment.populateFromRow(experimentRecord)
            assert experiment.getId() == experimentRecord.id
            self.addExperiment(experiment)

    def _createAnalysisTable(self):
        self.database.create_table(models.Analysis)

    def insertAnalysis(self, analysis):
        """
        Inserts the specified Analysis into this repository.
        """
        try:
            models.Analysis.create(
                id=analysis.getId(),
                name=analysis.getName(),
                description=analysis.getDescription(),
                created=analysis.getCreated(),
                updated=analysis.getUpdated(),
                type=analysis.getAnalysisType(),
                software=analysis.getSoftware(),
                attributes=json.dumps(analysis.getAttributes()),
                datasetId=analysis.getParentContainer().getId(),
                experiment_id = analysis.getExperimentId(),
                other_analysis_descriptor = analysis.getOtherAnalysisDescriptor(),
                other_analysis_completition_date = analysis.getOtherAnalysisCompletitionDate(),
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                analysis.getLocalId(), None)

    def _readAnalysisTable(self):
        for analysisRecord in models.Analysis.select():
            dataset = self.getDataset(analysisRecord.datasetid.id)
            analysis = biodata.Analysis(dataset, analysisRecord.name)
            analysis.populateFromRow(analysisRecord)
            assert analysis.getId() == analysisRecord.id
            self.addAnalysis(analysis)

    def _createPatientTable(self):
        self.database.create_table(models.Patient)

    def insertPatient(self, patient):
        """
        Inserts the specified patient into this repository.
        """
        try:
            models.Patient.create(
                # Common fields
                id=patient.getId(),
                datasetId=patient.getParentContainer().getId(),
                created=patient.getCreated(),
                updated=patient.getUpdated(),
                name=patient.getLocalId(),
                description=patient.getDescription(),
                attributes=json.dumps(patient.getAttributes()),
                # Unique fields
                patientId = patient.getPatientId(),
                patientIdTier = patient.getPatientIdTier(),
                otherIds = patient.getOtherIds(),
                otherIdsTier = patient.getOtherIdsTier(),
                dateOfBirth = patient.getDateOfBirth(),
                dateOfBirthTier = patient.getDateOfBirthTier(),
                gender = patient.getGender(),
                genderTier = patient.getGenderTier(),
                ethnicity = patient.getEthnicity(),
                ethnicityTier = patient.getEthnicityTier(),
                race = patient.getRace(),
                raceTier = patient.getRaceTier(),
                provinceOfResidence = patient.getProvinceOfResidence(),
                provinceOfResidenceTier = patient.getProvinceOfResidenceTier(),
                dateOfDeath = patient.getDateOfDeath(),
                dateOfDeathTier = patient.getDateOfDeathTier(),
                causeOfDeath = patient.getCauseOfDeath(),
                causeOfDeathTier = patient.getCauseOfDeathTier(),
                autopsyTissueForResearch = patient.getAutopsyTissueForResearch(),
                autopsyTissueForResearchTier = patient.getAutopsyTissueForResearchTier(),
                priorMalignancy = patient.getPriorMalignancy(),
                priorMalignancyTier = patient.getPriorMalignancyTier(),
                dateOfPriorMalignancy = patient.getDateOfPriorMalignancy(),
                dateOfPriorMalignancyTier = patient.getDateOfPriorMalignancyTier(),
                familyHistoryAndRiskFactors = patient.getFamilyHistoryAndRiskFactors(),
                familyHistoryAndRiskFactorsTier = patient.getFamilyHistoryAndRiskFactorsTier(),
                familyHistoryOfPredispositionSyndrome = patient.getFamilyHistoryOfPredispositionSyndrome(),
                familyHistoryOfPredispositionSyndromeTier = patient.getFamilyHistoryOfPredispositionSyndromeTier(),
                detailsOfPredispositionSyndrome = patient.getDetailsOfPredispositionSyndrome(),
                detailsOfPredispositionSyndromeTier = patient.getDetailsOfPredispositionSyndromeTier(),
                geneticCancerSyndrome = patient.getGeneticCancerSyndrome(),
                geneticCancerSyndromeTier = patient.getGeneticCancerSyndromeTier(),
                otherGeneticConditionOrSignificantComorbidity = patient.getOtherGeneticConditionOrSignificantComorbidity(),
                otherGeneticConditionOrSignificantComorbidityTier = patient.getOtherGeneticConditionOrSignificantComorbidityTier(),
                occupationalOrEnvironmentalExposure = patient.getOccupationalOrEnvironmentalExposure(),
                occupationalOrEnvironmentalExposureTier = patient.getOccupationalOrEnvironmentalExposureTier(),
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                patient.getLocalId(),
                patient.getParentContainer().getLocalId())

    def _readPatientTable(self):
        """
        Read the Patient table upon load
        """
        for patientRecord in models.Patient.select():
            dataset = self.getDataset(patientRecord.datasetid.id)
            patient = clinical_metadata.Patient(
                dataset, patientRecord.name)
            patient.populateFromRow(patientRecord)
            assert patient.getId() == patientRecord.id
            dataset.addPatient(patient)

    def _createEnrollmentTable(self):
        self.database.create_table(models.Enrollment)

    def insertEnrollment(self, enrollment):
        """
        Inserts the specified enrollment into this repository.
        """
        try:
            models.Enrollment.create(
                # Common fields
                id=enrollment.getId(),
                datasetId=enrollment.getParentContainer().getId(),
                created=enrollment.getCreated(),
                updated=enrollment.getUpdated(),
                name=enrollment.getLocalId(),
                description=enrollment.getDescription(),
                attributes=json.dumps(enrollment.getAttributes()),

                # Unique fields
                patientId = enrollment.getPatientId(),
                patientIdTier = enrollment.getPatientIdTier(),
                enrollmentInstitution = enrollment.getEnrollmentInstitution(),
                enrollmentInstitutionTier = enrollment.getEnrollmentInstitutionTier(),
                enrollmentApprovalDate = enrollment.getEnrollmentApprovalDate(),
                enrollmentApprovalDateTier = enrollment.getEnrollmentApprovalDateTier(),
                crossEnrollment = enrollment.getCrossEnrollment(),
                crossEnrollmentTier = enrollment.getCrossEnrollmentTier(),
                otherPersonalizedMedicineStudyName = enrollment.getOtherPersonalizedMedicineStudyName(),
                otherPersonalizedMedicineStudyNameTier = enrollment.getOtherPersonalizedMedicineStudyNameTier(),
                otherPersonalizedMedicineStudyId = enrollment.getOtherPersonalizedMedicineStudyId(),
                otherPersonalizedMedicineStudyIdTier = enrollment.getOtherPersonalizedMedicineStudyIdTier(),
                ageAtEnrollment = enrollment.getAgeAtEnrollment(),
                ageAtEnrollmentTier = enrollment.getAgeAtEnrollmentTier(),
                eligibilityCategory = enrollment.getEligibilityCategory(),
                eligibilityCategoryTier = enrollment.getEligibilityCategoryTier(),
                statusAtEnrollment = enrollment.getStatusAtEnrollment(),
                statusAtEnrollmentTier = enrollment.getStatusAtEnrollmentTier(),
                primaryOncologistName = enrollment.getPrimaryOncologistName(),
                primaryOncologistNameTier = enrollment.getPrimaryOncologistNameTier(),
                primaryOncologistContact = enrollment.getPrimaryOncologistContact(),
                primaryOncologistContactTier = enrollment.getPrimaryOncologistContactTier(),
                referringPhysicianName = enrollment.getReferringPhysicianName(),
                referringPhysicianNameTier = enrollment.getReferringPhysicianNameTier(),
                referringPhysicianContact = enrollment.getReferringPhysicianContact(),
                referringPhysicianContactTier = enrollment.getReferringPhysicianContactTier(),
                summaryOfIdRequest = enrollment.getSummaryOfIdRequest(),
                summaryOfIdRequestTier = enrollment.getSummaryOfIdRequestTier(),
                treatingCentreName = enrollment.getTreatingCentreName(),
                treatingCentreNameTier = enrollment.getTreatingCentreNameTier(),
                treatingCentreProvince = enrollment.getTreatingCentreProvince(),
                treatingCentreProvinceTier = enrollment.getTreatingCentreProvinceTier(),
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                enrollment.getLocalId(),
                enrollment.getParentContainer().getLocalId())

    def _readEnrollmentTable(self):
        """
        Read the Enrollment table upon load
        """
        for enrollmentRecord in models.Enrollment.select():
            dataset = self.getDataset(enrollmentRecord.datasetid.id)
            enrollment = clinical_metadata.Enrollment(
                dataset, enrollmentRecord.name)
            enrollment.populateFromRow(enrollmentRecord)
            assert enrollment.getId() == enrollmentRecord.id
            dataset.addEnrollment(enrollment)

    def _createConsentTable(self):
        self.database.create_table(models.Consent)

    def insertConsent(self, consent):
        """
        Inserts the specified consent into this repository.
        """
        try:
            models.Consent.create(
                # Common fields
                id=consent.getId(),
                datasetId=consent.getParentContainer().getId(),
                created=consent.getCreated(),
                updated=consent.getUpdated(),
                name=consent.getLocalId(),
                description=consent.getDescription(),
                attributes=json.dumps(consent.getAttributes()),

                # Unique fields
                patientId = consent.getPatientId(),
                patientIdTier = consent.getPatientIdTier(),
                consentId = consent.getConsentId(),
                consentIdTier = consent.getConsentIdTier(),
                consentDate = consent.getConsentDate(),
                consentDateTier = consent.getConsentDateTier(),
                consentVersion = consent.getConsentVersion(),
                consentVersionTier = consent.getConsentVersionTier(),
                patientConsentedTo = consent.getPatientConsentedTo(),
                patientConsentedToTier = consent.getPatientConsentedToTier(),
                reasonForRejection = consent.getReasonForRejection(),
                reasonForRejectionTier = consent.getReasonForRejectionTier(),
                wasAssentObtained = consent.getWasAssentObtained(),
                wasAssentObtainedTier = consent.getWasAssentObtainedTier(),
                dateOfAssent = consent.getDateOfAssent(),
                dateOfAssentTier = consent.getDateOfAssentTier(),
                assentFormVersion = consent.getAssentFormVersion(),
                assentFormVersionTier = consent.getAssentFormVersionTier(),
                ifAssentNotObtainedWhyNot = consent.getIfAssentNotObtainedWhyNot(),
                ifAssentNotObtainedWhyNotTier = consent.getIfAssentNotObtainedWhyNotTier(),
                reconsentDate = consent.getReconsentDate(),
                reconsentDateTier = consent.getReconsentDateTier(),
                reconsentVersion = consent.getReconsentVersion(),
                reconsentVersionTier = consent.getReconsentVersionTier(),
                consentingCoordinatorName = consent.getConsentingCoordinatorName(),
                consentingCoordinatorNameTier = consent.getConsentingCoordinatorNameTier(),
                previouslyConsented = consent.getPreviouslyConsented(),
                previouslyConsentedTier = consent.getPreviouslyConsentedTier(),
                nameOfOtherBiobank = consent.getNameOfOtherBiobank(),
                nameOfOtherBiobankTier = consent.getNameOfOtherBiobankTier(),
                hasConsentBeenWithdrawn = consent.getHasConsentBeenWithdrawn(),
                hasConsentBeenWithdrawnTier = consent.getHasConsentBeenWithdrawnTier(),
                dateOfConsentWithdrawal = consent.getDateOfConsentWithdrawal(),
                dateOfConsentWithdrawalTier = consent.getDateOfConsentWithdrawalTier(),
                typeOfConsentWithdrawal = consent.getTypeOfConsentWithdrawal(),
                typeOfConsentWithdrawalTier = consent.getTypeOfConsentWithdrawalTier(),
                reasonForConsentWithdrawal = consent.getReasonForConsentWithdrawal(),
                reasonForConsentWithdrawalTier = consent.getReasonForConsentWithdrawalTier(),
                consentFormComplete = consent.getConsentFormComplete(),
                consentFormCompleteTier = consent.getConsentFormCompleteTier(),
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                consent.getLocalId(),
                consent.getParentContainer().getLocalId())

    def _readConsentTable(self):
        """
        Read the Consent table upon load
        """
        for consentRecord in models.Consent.select():
            dataset = self.getDataset(consentRecord.datasetid.id)
            consent = clinical_metadata.Consent(
                dataset, consentRecord.name)
            consent.populateFromRow(consentRecord)
            assert consent.getId() == consentRecord.id
            dataset.addConsent(consent)

    def _createDiagnosisTable(self):
        self.database.create_table(models.Diagnosis)

    def insertDiagnosis(self, diagnosis):
        """
        Inserts the specified diagnosis into this repository.
        """
        try:
            models.Diagnosis.create(
                # Common fields
                id=diagnosis.getId(),
                datasetId=diagnosis.getParentContainer().getId(),
                created=diagnosis.getCreated(),
                updated=diagnosis.getUpdated(),
                name=diagnosis.getLocalId(),
                description=diagnosis.getDescription(),
                attributes=json.dumps(diagnosis.getAttributes()),

                # Unique fields
                patientId = diagnosis.getPatientId(),
                patientIdTier = diagnosis.getPatientIdTier(),
                diagnosisId = diagnosis.getDiagnosisId(),
                diagnosisIdTier = diagnosis.getDiagnosisIdTier(),
                diagnosisDate = diagnosis.getDiagnosisDate(),
                diagnosisDateTier = diagnosis.getDiagnosisDateTier(),
                ageAtDiagnosis = diagnosis.getAgeAtDiagnosis(),
                ageAtDiagnosisTier = diagnosis.getAgeAtDiagnosisTier(),
                cancerType = diagnosis.getCancerType(),
                cancerTypeTier = diagnosis.getCancerTypeTier(),
                classification = diagnosis.getClassification(),
                classificationTier = diagnosis.getClassificationTier(),
                cancerSite = diagnosis.getCancerSite(),
                cancerSiteTier = diagnosis.getCancerSiteTier(),
                histology = diagnosis.getHistology(),
                histologyTier = diagnosis.getHistologyTier(),
                methodOfDefinitiveDiagnosis = diagnosis.getMethodOfDefinitiveDiagnosis(),
                methodOfDefinitiveDiagnosisTier = diagnosis.getMethodOfDefinitiveDiagnosisTier(),
                sampleType = diagnosis.getSampleType(),
                sampleTypeTier = diagnosis.getSampleTypeTier(),
                sampleSite = diagnosis.getSampleSite(),
                sampleSiteTier = diagnosis.getSampleSiteTier(),
                tumorGrade = diagnosis.getTumorGrade(),
                tumorGradeTier = diagnosis.getTumorGradeTier(),
                gradingSystemUsed = diagnosis.getGradingSystemUsed(),
                gradingSystemUsedTier = diagnosis.getGradingSystemUsedTier(),
                sitesOfMetastases = diagnosis.getSitesOfMetastases(),
                sitesOfMetastasesTier = diagnosis.getSitesOfMetastasesTier(),
                stagingSystem = diagnosis.getStagingSystem(),
                stagingSystemTier = diagnosis.getStagingSystemTier(),
                versionOrEditionOfTheStagingSystem = diagnosis.getVersionOrEditionOfTheStagingSystem(),
                versionOrEditionOfTheStagingSystemTier = diagnosis.getVersionOrEditionOfTheStagingSystemTier(),
                specificTumorStageAtDiagnosis = diagnosis.getSpecificTumorStageAtDiagnosis(),
                specificTumorStageAtDiagnosisTier = diagnosis.getSpecificTumorStageAtDiagnosisTier(),
                prognosticBiomarkers = diagnosis.getPrognosticBiomarkers(),
                prognosticBiomarkersTier = diagnosis.getPrognosticBiomarkersTier(),
                biomarkerQuantification = diagnosis.getBiomarkerQuantification(),
                biomarkerQuantificationTier = diagnosis.getBiomarkerQuantificationTier(),
                additionalMolecularTesting = diagnosis.getAdditionalMolecularTesting(),
                additionalMolecularTestingTier = diagnosis.getAdditionalMolecularTestingTier(),
                additionalTestType = diagnosis.getAdditionalTestType(),
                additionalTestTypeTier = diagnosis.getAdditionalTestTypeTier(),
                laboratoryName = diagnosis.getLaboratoryName(),
                laboratoryNameTier = diagnosis.getLaboratoryNameTier(),
                laboratoryAddress = diagnosis.getLaboratoryAddress(),
                laboratoryAddressTier = diagnosis.getLaboratoryAddressTier(),
                siteOfMetastases = diagnosis.getSiteOfMetastases(),
                siteOfMetastasesTier = diagnosis.getSiteOfMetastasesTier(),
                stagingSystemVersion = diagnosis.getStagingSystemVersion(),
                stagingSystemVersionTier = diagnosis.getStagingSystemVersionTier(),
                specificStage = diagnosis.getSpecificStage(),
                specificStageTier = diagnosis.getSpecificStageTier(),
                cancerSpecificBiomarkers = diagnosis.getCancerSpecificBiomarkers(),
                cancerSpecificBiomarkersTier = diagnosis.getCancerSpecificBiomarkersTier(),
                additionalMolecularDiagnosticTestingPerformed = diagnosis.getAdditionalMolecularDiagnosticTestingPerformed(),
                additionalMolecularDiagnosticTestingPerformedTier = diagnosis.getAdditionalMolecularDiagnosticTestingPerformedTier(),
                additionalTest = diagnosis.getAdditionalTest(),
                additionalTestTier = diagnosis.getAdditionalTestTier(),
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                diagnosis.getLocalId(),
                diagnosis.getParentContainer().getLocalId())

    def _readDiagnosisTable(self):
        """
        Read the Diagnosis table upon load
        """
        for diagnosisRecord in models.Diagnosis.select():
            dataset = self.getDataset(diagnosisRecord.datasetid.id)
            diagnosis = clinical_metadata.Diagnosis(
                dataset, diagnosisRecord.name)
            diagnosis.populateFromRow(diagnosisRecord)
            assert diagnosis.getId() == diagnosisRecord.id
            dataset.addDiagnosis(diagnosis)

    def _createSampleTable(self):
        self.database.create_table(models.Sample)

    def insertSample(self, sample):
        """
        Inserts the specified sample into this repository.
        """
        try:
            models.Sample.create(
                # Common fields
                id=sample.getId(),
                datasetId=sample.getParentContainer().getId(),
                created=sample.getCreated(),
                updated=sample.getUpdated(),
                name=sample.getLocalId(),
                description=sample.getDescription(),
                attributes=json.dumps(sample.getAttributes()),

                # Unique fields
                patientId = sample.getPatientId(),
                patientIdTier = sample.getPatientIdTier(),
                sampleId = sample.getSampleId(),
                sampleIdTier = sample.getSampleIdTier(),
                diagnosisId = sample.getDiagnosisId(),
                diagnosisIdTier = sample.getDiagnosisIdTier(),
                localBiobankId = sample.getLocalBiobankId(),
                localBiobankIdTier = sample.getLocalBiobankIdTier(),
                collectionDate = sample.getCollectionDate(),
                collectionDateTier = sample.getCollectionDateTier(),
                collectionHospital = sample.getCollectionHospital(),
                collectionHospitalTier = sample.getCollectionHospitalTier(),
                sampleType = sample.getSampleType(),
                sampleTypeTier = sample.getSampleTypeTier(),
                tissueDiseaseState = sample.getTissueDiseaseState(),
                tissueDiseaseStateTier = sample.getTissueDiseaseStateTier(),
                anatomicSiteTheSampleObtainedFrom = sample.getAnatomicSiteTheSampleObtainedFrom(),
                anatomicSiteTheSampleObtainedFromTier = sample.getAnatomicSiteTheSampleObtainedFromTier(),
                cancerType = sample.getCancerType(),
                cancerTypeTier = sample.getCancerTypeTier(),
                cancerSubtype = sample.getCancerSubtype(),
                cancerSubtypeTier = sample.getCancerSubtypeTier(),
                pathologyReportId = sample.getPathologyReportId(),
                pathologyReportIdTier = sample.getPathologyReportIdTier(),
                morphologicalCode = sample.getMorphologicalCode(),
                morphologicalCodeTier = sample.getMorphologicalCodeTier(),
                topologicalCode = sample.getTopologicalCode(),
                topologicalCodeTier = sample.getTopologicalCodeTier(),
                shippingDate = sample.getShippingDate(),
                shippingDateTier = sample.getShippingDateTier(),
                receivedDate = sample.getReceivedDate(),
                receivedDateTier = sample.getReceivedDateTier(),
                qualityControlPerformed = sample.getQualityControlPerformed(),
                qualityControlPerformedTier = sample.getQualityControlPerformedTier(),
                estimatedTumorContent = sample.getEstimatedTumorContent(),
                estimatedTumorContentTier = sample.getEstimatedTumorContentTier(),
                quantity = sample.getQuantity(),
                quantityTier = sample.getQuantityTier(),
                units = sample.getUnits(),
                unitsTier = sample.getUnitsTier(),
                associatedBiobank = sample.getAssociatedBiobank(),
                associatedBiobankTier = sample.getAssociatedBiobankTier(),
                otherBiobank = sample.getOtherBiobank(),
                otherBiobankTier = sample.getOtherBiobankTier(),
                sopFollowed = sample.getSopFollowed(),
                sopFollowedTier = sample.getSopFollowedTier(),
                ifNotExplainAnyDeviation = sample.getIfNotExplainAnyDeviation(),
                ifNotExplainAnyDeviationTier = sample.getIfNotExplainAnyDeviationTier(),
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                sample.getLocalId(),
                sample.getParentContainer().getLocalId())

    def _readSampleTable(self):
        """
        Read the Sample table upon load
        """
        for sampleRecord in models.Sample.select():
            dataset = self.getDataset(sampleRecord.datasetid.id)
            sample = clinical_metadata.Sample(
                dataset, sampleRecord.name)
            sample.populateFromRow(sampleRecord)
            assert sample.getId() == sampleRecord.id
            dataset.addSample(sample)

    def _createTreatmentTable(self):
        self.database.create_table(models.Treatment)

    def insertTreatment(self, treatment):
        """
        Inserts the specified treatment into this repository.
        """
        try:
            models.Treatment.create(
                # Common fields
                id=treatment.getId(),
                datasetId=treatment.getParentContainer().getId(),
                created=treatment.getCreated(),
                updated=treatment.getUpdated(),
                name=treatment.getLocalId(),
                description=treatment.getDescription(),
                attributes=json.dumps(treatment.getAttributes()),

                # Unique fields
                patientId = treatment.getPatientId(),
                patientIdTier = treatment.getPatientIdTier(),
                courseNumber = treatment.getCourseNumber(),
                courseNumberTier = treatment.getCourseNumberTier(),
                therapeuticModality = treatment.getTherapeuticModality(),
                therapeuticModalityTier = treatment.getTherapeuticModalityTier(),
                treatmentPlanType = treatment.getTreatmentPlanType(),
                treatmentPlanTypeTier = treatment.getTreatmentPlanTypeTier(),
                treatmentIntent = treatment.getTreatmentIntent(),
                treatmentIntentTier = treatment.getTreatmentIntentTier(),
                startDate = treatment.getStartDate(),
                startDateTier = treatment.getStartDateTier(),
                stopDate = treatment.getStopDate(),
                stopDateTier = treatment.getStopDateTier(),
                reasonForEndingTheTreatment = treatment.getReasonForEndingTheTreatment(),
                reasonForEndingTheTreatmentTier = treatment.getReasonForEndingTheTreatmentTier(),
                responseToTreatment = treatment.getResponseToTreatment(),
                responseToTreatmentTier = treatment.getResponseToTreatmentTier(),
                responseCriteriaUsed = treatment.getResponseCriteriaUsed(),
                responseCriteriaUsedTier = treatment.getResponseCriteriaUsedTier(),
                dateOfRecurrenceOrProgressionAfterThisTreatment = treatment.getDateOfRecurrenceOrProgressionAfterThisTreatment(),
                dateOfRecurrenceOrProgressionAfterThisTreatmentTier = treatment.getDateOfRecurrenceOrProgressionAfterThisTreatmentTier(),
                unexpectedOrUnusualToxicityDuringTreatment = treatment.getUnexpectedOrUnusualToxicityDuringTreatment(),
                unexpectedOrUnusualToxicityDuringTreatmentTier = treatment.getUnexpectedOrUnusualToxicityDuringTreatmentTier()
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                treatment.getLocalId(),
                treatment.getParentContainer().getLocalId())

    def _readTreatmentTable(self):
        """
        Read the Treatment table upon load
        """
        for treatmentRecord in models.Treatment.select():
            dataset = self.getDataset(treatmentRecord.datasetid.id)
            treatment = clinical_metadata.Treatment(
                dataset, treatmentRecord.name)
            treatment.populateFromRow(treatmentRecord)
            assert treatment.getId() == treatmentRecord.id
            dataset.addTreatment(treatment)

    def _createOutcomeTable(self):
        self.database.create_table(models.Outcome)

    def insertOutcome(self, outcome):
        """
        Inserts the specified outcome into this repository.
        """
        try:
            models.Outcome.create(
                # Common fields
                id=outcome.getId(),
                datasetId=outcome.getParentContainer().getId(),
                created=outcome.getCreated(),
                updated=outcome.getUpdated(),
                name=outcome.getLocalId(),
                description=outcome.getDescription(),
                attributes=json.dumps(outcome.getAttributes()),

                # Unique fields
                patientId = outcome.getPatientId(),
                patientIdTier = outcome.getPatientIdTier(),
                physicalExamId = outcome.getPhysicalExamId(),
                physicalExamIdTier = outcome.getPhysicalExamIdTier(),
                dateOfAssessment = outcome.getDateOfAssessment(),
                dateOfAssessmentTier = outcome.getDateOfAssessmentTier(),
                diseaseResponseOrStatus = outcome.getDiseaseResponseOrStatus(),
                diseaseResponseOrStatusTier = outcome.getDiseaseResponseOrStatusTier(),
                otherResponseClassification = outcome.getOtherResponseClassification(),
                otherResponseClassificationTier = outcome.getOtherResponseClassificationTier(),
                minimalResidualDiseaseAssessment = outcome.getMinimalResidualDiseaseAssessment(),
                minimalResidualDiseaseAssessmentTier = outcome.getMinimalResidualDiseaseAssessmentTier(),
                methodOfResponseEvaluation = outcome.getMethodOfResponseEvaluation(),
                methodOfResponseEvaluationTier = outcome.getMethodOfResponseEvaluationTier(),
                responseCriteriaUsed = outcome.getResponseCriteriaUsed(),
                responseCriteriaUsedTier = outcome.getResponseCriteriaUsedTier(),
                summaryStage = outcome.getSummaryStage(),
                summaryStageTier = outcome.getSummaryStageTier(),
                sitesOfAnyProgressionOrRecurrence = outcome.getSitesOfAnyProgressionOrRecurrence(),
                sitesOfAnyProgressionOrRecurrenceTier = outcome.getSitesOfAnyProgressionOrRecurrenceTier(),
                vitalStatus = outcome.getVitalStatus(),
                vitalStatusTier = outcome.getVitalStatusTier(),
                height = outcome.getHeight(),
                heightTier = outcome.getHeightTier(),
                weight = outcome.getWeight(),
                weightTier = outcome.getWeightTier(),
                heightUnits = outcome.getHeightUnits(),
                heightUnitsTier = outcome.getHeightUnitsTier(),
                weightUnits = outcome.getWeightUnits(),
                weightUnitsTier = outcome.getWeightUnitsTier(),
                performanceStatus = outcome.getPerformanceStatus(),
                performanceStatusTier = outcome.getPerformanceStatusTier(),
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                outcome.getLocalId(),
                outcome.getParentContainer().getLocalId())

    def _readOutcomeTable(self):
        """
        Read the Outcome table upon load
        """
        for outcomeRecord in models.Outcome.select():
            dataset = self.getDataset(outcomeRecord.datasetid.id)
            outcome = clinical_metadata.Outcome(
                dataset, outcomeRecord.name)
            outcome.populateFromRow(outcomeRecord)
            assert outcome.getId() == outcomeRecord.id
            dataset.addOutcome(outcome)

    def _createComplicationTable(self):
        self.database.create_table(models.Complication)

    def insertComplication(self, complication):
        """
        Inserts the specified complication into this repository.
        """
        try:
            models.Complication.create(
                # Common fields
                id=complication.getId(),
                datasetId=complication.getParentContainer().getId(),
                created=complication.getCreated(),
                updated=complication.getUpdated(),
                name=complication.getLocalId(),
                description=complication.getDescription(),
                attributes=json.dumps(complication.getAttributes()),

                # Unique fields
                patientId = complication.getPatientId(),
                patientIdTier = complication.getPatientIdTier(),
                date = complication.getDate(),
                dateTier = complication.getDateTier(),
                lateComplicationOfTherapyDeveloped = complication.getLateComplicationOfTherapyDeveloped(),
                lateComplicationOfTherapyDevelopedTier = complication.getLateComplicationOfTherapyDevelopedTier(),
                lateToxicityDetail = complication.getLateToxicityDetail(),
                lateToxicityDetailTier = complication.getLateToxicityDetailTier(),
                suspectedTreatmentInducedNeoplasmDeveloped = complication.getSuspectedTreatmentInducedNeoplasmDeveloped(),
                suspectedTreatmentInducedNeoplasmDevelopedTier = complication.getSuspectedTreatmentInducedNeoplasmDevelopedTier(),
                treatmentInducedNeoplasmDetails = complication.getTreatmentInducedNeoplasmDetails(),
                treatmentInducedNeoplasmDetailsTier = complication.getTreatmentInducedNeoplasmDetailsTier(),
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                complication.getLocalId(),
                complication.getParentContainer().getLocalId())

    def _readComplicationTable(self):
        """
        Read the Complication table upon load
        """
        for complicationRecord in models.Complication.select():
            dataset = self.getDataset(complicationRecord.datasetid.id)
            complication = clinical_metadata.Complication(
                dataset, complicationRecord.name)
            complication.populateFromRow(complicationRecord)
            assert complication.getId() == complicationRecord.id
            dataset.addComplication(complication)

    def _createTumourboardTable(self):
        self.database.create_table(models.Tumourboard)

    def insertTumourboard(self, tumourboard):
        """
        Inserts the specified tumourboard into this repository.
        """
        try:
            models.Tumourboard.create(
                # Common fields
                id=tumourboard.getId(),
                datasetId=tumourboard.getParentContainer().getId(),
                created=tumourboard.getCreated(),
                updated=tumourboard.getUpdated(),
                name=tumourboard.getLocalId(),
                description=tumourboard.getDescription(),
                attributes=json.dumps(tumourboard.getAttributes()),

                # Unique fields
                patientId = tumourboard.getPatientId(),
                patientIdTier = tumourboard.getPatientIdTier(),
                dateOfMolecularTumorBoard = tumourboard.getDateOfMolecularTumorBoard(),
                dateOfMolecularTumorBoardTier = tumourboard.getDateOfMolecularTumorBoardTier(),
                typeOfSampleAnalyzed = tumourboard.getTypeOfSampleAnalyzed(),
                typeOfSampleAnalyzedTier = tumourboard.getTypeOfSampleAnalyzedTier(),
                typeOfTumourSampleAnalyzed = tumourboard.getTypeOfTumourSampleAnalyzed(),
                typeOfTumourSampleAnalyzedTier = tumourboard.getTypeOfTumourSampleAnalyzedTier(),
                analysesDiscussed = tumourboard.getAnalysesDiscussed(),
                analysesDiscussedTier = tumourboard.getAnalysesDiscussedTier(),
                somaticSampleType = tumourboard.getSomaticSampleType(),
                somaticSampleTypeTier = tumourboard.getSomaticSampleTypeTier(),
                normalExpressionComparator = tumourboard.getNormalExpressionComparator(),
                normalExpressionComparatorTier = tumourboard.getNormalExpressionComparatorTier(),
                diseaseExpressionComparator = tumourboard.getDiseaseExpressionComparator(),
                diseaseExpressionComparatorTier = tumourboard.getDiseaseExpressionComparatorTier(),
                hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer = tumourboard.getHasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancer(),
                hasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancerTier = tumourboard.getHasAGermlineVariantBeenIdentifiedByProfilingThatMayPredisposeToCancerTier(),
                actionableTargetFound = tumourboard.getActionableTargetFound(),
                actionableTargetFoundTier = tumourboard.getActionableTargetFoundTier(),
                molecularTumorBoardRecommendation = tumourboard.getMolecularTumorBoardRecommendation(),
                molecularTumorBoardRecommendationTier = tumourboard.getMolecularTumorBoardRecommendationTier(),
                germlineDnaSampleId = tumourboard.getGermlineDnaSampleId(),
                germlineDnaSampleIdTier = tumourboard.getGermlineDnaSampleIdTier(),
                tumorDnaSampleId = tumourboard.getTumorDnaSampleId(),
                tumorDnaSampleIdTier = tumourboard.getTumorDnaSampleIdTier(),
                tumorRnaSampleId = tumourboard.getTumorRnaSampleId(),
                tumorRnaSampleIdTier = tumourboard.getTumorRnaSampleIdTier(),
                germlineSnvDiscussed = tumourboard.getGermlineSnvDiscussed(),
                germlineSnvDiscussedTier = tumourboard.getGermlineSnvDiscussedTier(),
                somaticSnvDiscussed = tumourboard.getSomaticSnvDiscussed(),
                somaticSnvDiscussedTier = tumourboard.getSomaticSnvDiscussedTier(),
                cnvsDiscussed = tumourboard.getCnvsDiscussed(),
                cnvsDiscussedTier = tumourboard.getCnvsDiscussedTier(),
                structuralVariantDiscussed = tumourboard.getStructuralVariantDiscussed(),
                structuralVariantDiscussedTier = tumourboard.getStructuralVariantDiscussedTier(),
                classificationOfVariants = tumourboard.getClassificationOfVariants(),
                classificationOfVariantsTier = tumourboard.getClassificationOfVariantsTier(),
                clinicalValidationProgress = tumourboard.getClinicalValidationProgress(),
                clinicalValidationProgressTier = tumourboard.getClinicalValidationProgressTier(),
                typeOfValidation = tumourboard.getTypeOfValidation(),
                typeOfValidationTier = tumourboard.getTypeOfValidationTier(),
                agentOrDrugClass = tumourboard.getAgentOrDrugClass(),
                agentOrDrugClassTier = tumourboard.getAgentOrDrugClassTier(),
                levelOfEvidenceForExpressionTargetAgentMatch = tumourboard.getLevelOfEvidenceForExpressionTargetAgentMatch(),
                levelOfEvidenceForExpressionTargetAgentMatchTier = tumourboard.getLevelOfEvidenceForExpressionTargetAgentMatchTier(),
                didTreatmentPlanChangeBasedOnProfilingResult = tumourboard.getDidTreatmentPlanChangeBasedOnProfilingResult(),
                didTreatmentPlanChangeBasedOnProfilingResultTier = tumourboard.getDidTreatmentPlanChangeBasedOnProfilingResultTier(),
                howTreatmentHasAlteredBasedOnProfiling = tumourboard.getHowTreatmentHasAlteredBasedOnProfiling(),
                howTreatmentHasAlteredBasedOnProfilingTier = tumourboard.getHowTreatmentHasAlteredBasedOnProfilingTier(),
                reasonTreatmentPlanDidNotChangeBasedOnProfiling = tumourboard.getReasonTreatmentPlanDidNotChangeBasedOnProfiling(),
                reasonTreatmentPlanDidNotChangeBasedOnProfilingTier = tumourboard.getReasonTreatmentPlanDidNotChangeBasedOnProfilingTier(),
                detailsOfTreatmentPlanImpact = tumourboard.getDetailsOfTreatmentPlanImpact(),
                detailsOfTreatmentPlanImpactTier = tumourboard.getDetailsOfTreatmentPlanImpactTier(),
                patientOrFamilyInformedOfGermlineVariant = tumourboard.getPatientOrFamilyInformedOfGermlineVariant(),
                patientOrFamilyInformedOfGermlineVariantTier = tumourboard.getPatientOrFamilyInformedOfGermlineVariantTier(),
                patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling = tumourboard.getPatientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfiling(),
                patientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfilingTier = tumourboard.getPatientHasBeenReferredToAHereditaryCancerProgramBasedOnThisMolecularProfilingTier(),
                summaryReport = tumourboard.getSummaryReport(),
                summaryReportTier = tumourboard.getSummaryReportTier(),
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                tumourboard.getLocalId(),
                tumourboard.getParentContainer().getLocalId())

    def _readTumourboardTable(self):
        """
        Read the Tumourboard table upon load
        """
        for tumourboardRecord in models.Tumourboard.select():
            dataset = self.getDataset(tumourboardRecord.datasetid.id)
            tumourboard = clinical_metadata.Tumourboard(
                dataset, tumourboardRecord.name)
            tumourboard.populateFromRow(tumourboardRecord)
            assert tumourboard.getId() == tumourboardRecord.id
            dataset.addTumourboard(tumourboard)

    def _createChemotherapyTable(self):
        self.database.create_table(models.Chemotherapy)

    def insertChemotherapy(self, chemotherapy):
        """
        Inserts the specified chemotherapy into this repository.
        """
        try:
            models.Chemotherapy.create(
                # Common fields
                id=chemotherapy.getId(),
                datasetId=chemotherapy.getParentContainer().getId(),
                created=chemotherapy.getCreated(),
                updated=chemotherapy.getUpdated(),
                name=chemotherapy.getLocalId(),
                description=chemotherapy.getDescription(),
                attributes=json.dumps(chemotherapy.getAttributes()),

                # Unique fields
                patientId=chemotherapy.getPatientId(),
                patientIdTier=chemotherapy.getPatientIdTier(),
                courseNumber=chemotherapy.getCourseNumber(),
                courseNumberTier=chemotherapy.getCourseNumberTier(),
                startDate=chemotherapy.getStartDate(),
                startDateTier=chemotherapy.getStartDateTier(),
                stopDate=chemotherapy.getStopDate(),
                stopDateTier=chemotherapy.getStopDateTier(),
                systematicTherapyAgentName=chemotherapy.getSystematicTherapyAgentName(),
                systematicTherapyAgentNameTier=chemotherapy.getSystematicTherapyAgentNameTier(),
                route=chemotherapy.getRoute(),
                routeTier=chemotherapy.getRouteTier(),
                dose=chemotherapy.getDose(),
                doseTier=chemotherapy.getDoseTier(),
                doseFrequency=chemotherapy.getDoseFrequency(),
                doseFrequencyTier=chemotherapy.getDoseFrequencyTier(),
                doseUnit=chemotherapy.getDoseUnit(),
                doseUnitTier=chemotherapy.getDoseUnitTier(),
                daysPerCycle=chemotherapy.getDaysPerCycle(),
                daysPerCycleTier=chemotherapy.getDaysPerCycleTier(),
                numberOfCycle=chemotherapy.getNumberOfCycle(),
                numberOfCycleTier=chemotherapy.getNumberOfCycleTier(),
                treatmentIntent=chemotherapy.getTreatmentIntent(),
                treatmentIntentTier=chemotherapy.getTreatmentIntentTier(),
                treatingCentreName=chemotherapy.getTreatingCentreName(),
                treatingCentreNameTier=chemotherapy.getTreatingCentreNameTier(),
                type=chemotherapy.getType(),
                typeTier=chemotherapy.getTypeTier(),
                protocolCode=chemotherapy.getProtocolCode(),
                protocolCodeTier=chemotherapy.getProtocolCodeTier(),
                recordingDate=chemotherapy.getRecordingDate(),
                recordingDateTier=chemotherapy.getRecordingDateTier(),
                treatmentPlanId=chemotherapy.getTreatmentPlanId(),
                treatmentPlanIdTier=chemotherapy.getTreatmentPlanIdTier(),
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                chemotherapy.getLocalId(),
                chemotherapy.getParentContainer().getLocalId())

    def _readChemotherapyTable(self):
        """
        Read the Chemotherapy table upon load
        """
        for chemotherapyRecord in models.Chemotherapy.select():
            dataset = self.getDataset(chemotherapyRecord.datasetid.id)
            chemotherapy = clinical_metadata.Chemotherapy(
                dataset, chemotherapyRecord.name)
            chemotherapy.populateFromRow(chemotherapyRecord)
            assert chemotherapy.getId() == chemotherapyRecord.id
            dataset.addChemotherapy(chemotherapy)

    def _createRadiotherapyTable(self):
        self.database.create_table(models.Radiotherapy)

    def insertRadiotherapy(self, radiotherapy):
        """
        Inserts the specified radiotherapy into this repository.
        """
        try:
            models.Radiotherapy.create(
                # Common fields
                id=radiotherapy.getId(),
                datasetId=radiotherapy.getParentContainer().getId(),
                created=radiotherapy.getCreated(),
                updated=radiotherapy.getUpdated(),
                name=radiotherapy.getLocalId(),
                description=radiotherapy.getDescription(),
                attributes=json.dumps(radiotherapy.getAttributes()),

                # Unique fields
                patientId=radiotherapy.getPatientId(),
                patientIdTier=radiotherapy.getPatientIdTier(),
                courseNumber=radiotherapy.getCourseNumber(),
                courseNumberTier=radiotherapy.getCourseNumberTier(),
                startDate=radiotherapy.getStartDate(),
                startDateTier=radiotherapy.getStartDateTier(),
                stopDate=radiotherapy.getStopDate(),
                stopDateTier=radiotherapy.getStopDateTier(),
                therapeuticModality=radiotherapy.getTherapeuticModality(),
                therapeuticModalityTier=radiotherapy.getTherapeuticModalityTier(),
                baseline=radiotherapy.getBaseline(),
                baselineTier=radiotherapy.getBaselineTier(),
                testResult=radiotherapy.getTestResult(),
                testResultTier=radiotherapy.getTestResultTier(),
                testResultStd=radiotherapy.getTestResultStd(),
                testResultStdTier=radiotherapy.getTestResultStdTier(),
                treatingCentreName=radiotherapy.getTreatingCentreName(),
                treatingCentreNameTier=radiotherapy.getTreatingCentreNameTier(),
                startIntervalRad=radiotherapy.getStartIntervalRad(),
                startIntervalRadTier=radiotherapy.getStartIntervalRadTier(),
                startIntervalRadRaw=radiotherapy.getStartIntervalRadRaw(),
                startIntervalRadRawTier=radiotherapy.getStartIntervalRadRawTier(),
                recordingDate=radiotherapy.getRecordingDate(),
                recordingDateTier=radiotherapy.getRecordingDateTier(),
                adjacentFields=radiotherapy.getAdjacentFields(),
                adjacentFieldsTier=radiotherapy.getAdjacentFieldsTier(),
                adjacentFractions=radiotherapy.getAdjacentFractions(),
                adjacentFractionsTier=radiotherapy.getAdjacentFractionsTier(),
                complete=radiotherapy.getComplete(),
                completeTier=radiotherapy.getCompleteTier(),
                brachytherapyDose=radiotherapy.getBrachytherapyDose(),
                brachytherapyDoseTier=radiotherapy.getBrachytherapyDoseTier(),
                radiotherapyDose=radiotherapy.getRadiotherapyDose(),
                radiotherapyDoseTier=radiotherapy.getRadiotherapyDoseTier(),
                siteNumber=radiotherapy.getSiteNumber(),
                siteNumberTier=radiotherapy.getSiteNumberTier(),
                technique=radiotherapy.getTechnique(),
                techniqueTier=radiotherapy.getTechniqueTier(),
                treatedRegion=radiotherapy.getTreatedRegion(),
                treatedRegionTier=radiotherapy.getTreatedRegionTier(),
                treatmentPlanId=radiotherapy.getTreatmentPlanId(),
                treatmentPlanIdTier=radiotherapy.getTreatmentPlanIdTier(),
                radiationType=radiotherapy.getRadiationType(),
                radiationTypeTier=radiotherapy.getRadiationTypeTier(),
                radiationSite=radiotherapy.getRadiationSite(),
                radiationSiteTier=radiotherapy.getRadiationSiteTier(),
                totalDose=radiotherapy.getTotalDose(),
                totalDoseTier=radiotherapy.getTotalDoseTier(),
                boostSite=radiotherapy.getBoostSite(),
                boostSiteTier=radiotherapy.getBoostSiteTier(),
                boostDose=radiotherapy.getBoostDose(),
                boostDoseTier=radiotherapy.getBoostDoseTier()

            )
        except Exception:
            raise exceptions.DuplicateNameException(
                radiotherapy.getLocalId(),
                radiotherapy.getParentContainer().getLocalId())

    def _readRadiotherapyTable(self):
        """
        Read the Radiotherapy table upon load
        """
        for radiotherapyRecord in models.Radiotherapy.select():
            dataset = self.getDataset(radiotherapyRecord.datasetid.id)
            radiotherapy = clinical_metadata.Radiotherapy(
                dataset, radiotherapyRecord.name)
            radiotherapy.populateFromRow(radiotherapyRecord)
            assert radiotherapy.getId() == radiotherapyRecord.id
            dataset.addRadiotherapy(radiotherapy)

    def _createSurgeryTable(self):
        self.database.create_table(models.Surgery)

    def insertSurgery(self, surgery):
        """
        Inserts the specified surgery into this repository.
        """
        try:
            models.Surgery.create(
                # Common fields
                id=surgery.getId(),
                datasetId=surgery.getParentContainer().getId(),
                created=surgery.getCreated(),
                updated=surgery.getUpdated(),
                name=surgery.getLocalId(),
                description=surgery.getDescription(),
                attributes=json.dumps(surgery.getAttributes()),

                # Unique fields
                patientId=surgery.getPatientId(),
                patientIdTier=surgery.getPatientIdTier(),
                startDate=surgery.getStartDate(),
                startDateTier=surgery.getStartDateTier(),
                stopDate=surgery.getStopDate(),
                stopDateTier=surgery.getStopDateTier(),
                sampleId=surgery.getSampleId(),
                sampleIdTier=surgery.getSampleIdTier(),
                collectionTimePoint=surgery.getCollectionTimePoint(),
                collectionTimePointTier=surgery.getCollectionTimePointTier(),
                diagnosisDate=surgery.getDiagnosisDate(),
                diagnosisDateTier=surgery.getDiagnosisDateTier(),
                site=surgery.getSite(),
                siteTier=surgery.getSiteTier(),
                type=surgery.getType(),
                typeTier=surgery.getTypeTier(),
                recordingDate=surgery.getRecordingDate(),
                recordingDateTier=surgery.getRecordingDateTier(),
                treatmentPlanId=surgery.getTreatmentPlanId(),
                treatmentPlanIdTier=surgery.getTreatmentPlanIdTier(),
                courseNumber=surgery.getCourseNumber(),
                courseNumberTier=surgery.getCourseNumberTier()

            )
        except Exception:
            raise exceptions.DuplicateNameException(
                surgery.getLocalId(),
                surgery.getParentContainer().getLocalId())

    def _readSurgeryTable(self):
        """
        Read the Surgery table upon load
        """
        for surgeryRecord in models.Surgery.select():
            dataset = self.getDataset(surgeryRecord.datasetid.id)
            surgery = clinical_metadata.Surgery(
                dataset, surgeryRecord.name)
            surgery.populateFromRow(surgeryRecord)
            assert surgery.getId() == surgeryRecord.id
            dataset.addSurgery(surgery)

    def _createImmunotherapyTable(self):
        self.database.create_table(models.Immunotherapy)

    def insertImmunotherapy(self, immunotherapy):
        """
        Inserts the specified immunotherapy into this repository.
        """
        try:
            models.Immunotherapy.create(
                # Common fields
                id=immunotherapy.getId(),
                datasetId=immunotherapy.getParentContainer().getId(),
                created=immunotherapy.getCreated(),
                updated=immunotherapy.getUpdated(),
                name=immunotherapy.getLocalId(),
                description=immunotherapy.getDescription(),
                attributes=json.dumps(immunotherapy.getAttributes()),

                # Unique fields
                patientId=immunotherapy.getPatientId(),
                patientIdTier=immunotherapy.getPatientIdTier(),
                startDate=immunotherapy.getStartDate(),
                startDateTier=immunotherapy.getStartDateTier(),
                immunotherapyType=immunotherapy.getImmunotherapyType(),
                immunotherapyTypeTier=immunotherapy.getImmunotherapyTypeTier(),
                immunotherapyTarget=immunotherapy.getImmunotherapyTarget(),
                immunotherapyTargetTier=immunotherapy.getImmunotherapyTargetTier(),
                immunotherapyDetail=immunotherapy.getImmunotherapyDetail(),
                immunotherapyDetailTier=immunotherapy.getImmunotherapyDetailTier(),
                treatmentPlanId=immunotherapy.getTreatmentPlanId(),
                treatmentPlanIdTier=immunotherapy.getTreatmentPlanIdTier(),
                courseNumber=immunotherapy.getCourseNumber(),
                courseNumberTier=immunotherapy.getCourseNumberTier()

            )
        except Exception:
            raise exceptions.DuplicateNameException(
                immunotherapy.getLocalId(),
                immunotherapy.getParentContainer().getLocalId())

    def _readImmunotherapyTable(self):
        """
        Read the Immunotherapy table upon load
        """
        for immunotherapyRecord in models.Immunotherapy.select():
            dataset = self.getDataset(immunotherapyRecord.datasetid.id)
            immunotherapy = clinical_metadata.Immunotherapy(
                dataset, immunotherapyRecord.name)
            immunotherapy.populateFromRow(immunotherapyRecord)
            assert immunotherapy.getId() == immunotherapyRecord.id
            dataset.addImmunotherapy(immunotherapy)

    def _createCelltransplantTable(self):
        self.database.create_table(models.Celltransplant)

    def insertCelltransplant(self, celltransplant):
        """
        Inserts the specified celltransplant into this repository.
        """
        try:
            models.Celltransplant.create(
                # Common fields
                id=celltransplant.getId(),
                datasetId=celltransplant.getParentContainer().getId(),
                created=celltransplant.getCreated(),
                updated=celltransplant.getUpdated(),
                name=celltransplant.getLocalId(),
                description=celltransplant.getDescription(),
                attributes=json.dumps(celltransplant.getAttributes()),

                # Unique fields
                patientId=celltransplant.getPatientId(),
                patientIdTier=celltransplant.getPatientIdTier(),
                startDate=celltransplant.getStartDate(),
                startDateTier=celltransplant.getStartDateTier(),
                cellSource=celltransplant.getCellSource(),
                cellSourceTier=celltransplant.getCellSourceTier(),
                donorType=celltransplant.getDonorType(),
                donorTypeTier=celltransplant.getDonorTypeTier(),
                treatmentPlanId=celltransplant.getTreatmentPlanId(),
                treatmentPlanIdTier=celltransplant.getTreatmentPlanIdTier(),
                courseNumber=celltransplant.getCourseNumber(),
                courseNumberTier=celltransplant.getCourseNumberTier()

            )
        except Exception:
            raise exceptions.DuplicateNameException(
                celltransplant.getLocalId(),
                celltransplant.getParentContainer().getLocalId())

    def _readCelltransplantTable(self):
        """
        Read the Celltransplant table upon load
        """
        for celltransplantRecord in models.Celltransplant.select():
            dataset = self.getDataset(celltransplantRecord.datasetid.id)
            celltransplant = clinical_metadata.Celltransplant(
                dataset, celltransplantRecord.name)
            celltransplant.populateFromRow(celltransplantRecord)
            assert celltransplant.getId() == celltransplantRecord.id
            dataset.addCelltransplant(celltransplant)

    def _createSlideTable(self):
        self.database.create_table(models.Slide)

    def insertSlide(self, slide):
        """
        Inserts the specified slide into this repository.
        """
        try:
            models.Slide.create(
                # Common fields
                id=slide.getId(),
                datasetId=slide.getParentContainer().getId(),
                created=slide.getCreated(),
                updated=slide.getUpdated(),
                name=slide.getLocalId(),
                description=slide.getDescription(),
                attributes=json.dumps(slide.getAttributes()),

                # Unique fields
                patientId=slide.getPatientId(),
                patientIdTier=slide.getPatientIdTier(),
                sampleId=slide.getSampleId(),
                sampleIdTier=slide.getSampleIdTier(),
                slideId=slide.getSlideId(),
                slideIdTier=slide.getSlideIdTier(),
                slideOtherId=slide.getSlideOtherId(),
                slideOtherIdTier=slide.getSlideOtherIdTier(),
                lymphocyteInfiltrationPercent=slide.getLymphocyteInfiltrationPercent(),
                lymphocyteInfiltrationPercentTier=slide.getLymphocyteInfiltrationPercentTier(),
                tumorNucleiPercent=slide.getTumorNucleiPercent(),
                tumorNucleiPercentTier=slide.getTumorNucleiPercentTier(),
                monocyteInfiltrationPercent=slide.getMonocyteInfiltrationPercent(),
                monocyteInfiltrationPercentTier=slide.getMonocyteInfiltrationPercentTier(),
                normalCellsPercent=slide.getNormalCellsPercent(),
                normalCellsPercentTier=slide.getNormalCellsPercentTier(),
                tumorCellsPercent=slide.getTumorCellsPercent(),
                tumorCellsPercentTier=slide.getTumorCellsPercentTier(),
                stromalCellsPercent=slide.getStromalCellsPercent(),
                stromalCellsPercentTier=slide.getStromalCellsPercentTier(),
                eosinophilInfiltrationPercent=slide.getEosinophilInfiltrationPercent(),
                eosinophilInfiltrationPercentTier=slide.getEosinophilInfiltrationPercentTier(),
                neutrophilInfiltrationPercent=slide.getNeutrophilInfiltrationPercent(),
                neutrophilInfiltrationPercentTier=slide.getNeutrophilInfiltrationPercentTier(),
                granulocyteInfiltrationPercent=slide.getGranulocyteInfiltrationPercent(),
                granulocyteInfiltrationPercentTier=slide.getGranulocyteInfiltrationPercentTier(),
                necrosisPercent=slide.getNecrosisPercent(),
                necrosisPercentTier=slide.getNecrosisPercentTier(),
                inflammatoryInfiltrationPercent=slide.getInflammatoryInfiltrationPercent(),
                inflammatoryInfiltrationPercentTier=slide.getInflammatoryInfiltrationPercentTier(),
                proliferatingCellsNumber=slide.getProliferatingCellsNumber(),
                proliferatingCellsNumberTier=slide.getProliferatingCellsNumberTier(),
                sectionLocation=slide.getSectionLocation(),
                sectionLocationTier=slide.getSectionLocationTier(),

            )
        except Exception:
            raise exceptions.DuplicateNameException(
                slide.getLocalId(),
                slide.getParentContainer().getLocalId())

    def _readSlideTable(self):
        """
        Read the Slide table upon load
        """
        for slideRecord in models.Slide.select():
            dataset = self.getDataset(slideRecord.datasetid.id)
            slide = clinical_metadata.Slide(
                dataset, slideRecord.name)
            slide.populateFromRow(slideRecord)
            assert slide.getId() == slideRecord.id
            dataset.addSlide(slide)

    def _createStudyTable(self):
        self.database.create_table(models.Study)

    def insertStudy(self, study):
        """
        Inserts the specified study into this repository.
        """
        try:
            models.Study.create(
                # Common fields
                id=study.getId(),
                datasetId=study.getParentContainer().getId(),
                created=study.getCreated(),
                updated=study.getUpdated(),
                name=study.getLocalId(),
                description=study.getDescription(),
                attributes=json.dumps(study.getAttributes()),

                # Unique fields
                patientId=study.getPatientId(),
                patientIdTier=study.getPatientIdTier(),
                startDate=study.getStartDate(),
                startDateTier=study.getStartDateTier(),
                endDate=study.getEndDate(),
                endDateTier=study.getEndDateTier(),
                status=study.getStatus(),
                statusTier=study.getStatusTier(),
                recordingDate=study.getRecordingDate(),
                recordingDateTier=study.getRecordingDateTier(),

            )
        except Exception:
            raise exceptions.DuplicateNameException(
                study.getLocalId(),
                study.getParentContainer().getLocalId())

    def _readStudyTable(self):
        """
        Read the Study table upon load
        """
        for studyRecord in models.Study.select():
            dataset = self.getDataset(studyRecord.datasetid.id)
            study = clinical_metadata.Study(
                dataset, studyRecord.name)
            study.populateFromRow(studyRecord)
            assert study.getId() == studyRecord.id
            dataset.addStudy(study)

    def _createLabtestTable(self):
        self.database.create_table(models.Labtest)

    def insertLabtest(self, labtest):
        """
        Inserts the specified labtest into this repository.
        """
        try:
            models.Labtest.create(
                # Common fields
                id=labtest.getId(),
                datasetId=labtest.getParentContainer().getId(),
                created=labtest.getCreated(),
                updated=labtest.getUpdated(),
                name=labtest.getLocalId(),
                description=labtest.getDescription(),
                attributes=json.dumps(labtest.getAttributes()),

                # Unique fields
                patientId=labtest.getPatientId(),
                patientIdTier=labtest.getPatientIdTier(),
                startDate=labtest.getStartDate(),
                startDateTier=labtest.getStartDateTier(),
                collectionDate=labtest.getCollectionDate(),
                collectionDateTier=labtest.getCollectionDateTier(),
                endDate=labtest.getEndDate(),
                endDateTier=labtest.getEndDateTier(),
                eventType=labtest.getEventType(),
                eventTypeTier=labtest.getEventTypeTier(),
                testResults=labtest.getTestResults(),
                testResultsTier=labtest.getTestResultsTier(),
                timePoint=labtest.getTimePoint(),
                timePointTier=labtest.getTimePointTier(),
                recordingDate=labtest.getRecordingDate(),
                recordingDateTier=labtest.getRecordingDateTier(),

            )
        except Exception:
            raise exceptions.DuplicateNameException(
                labtest.getLocalId(),
                labtest.getParentContainer().getLocalId())

    def _readLabtestTable(self):
        """
        Read the Labtest table upon load
        """
        for labtestRecord in models.Labtest.select():
            dataset = self.getDataset(labtestRecord.datasetid.id)
            labtest = clinical_metadata.Labtest(
                dataset, labtestRecord.name)
            labtest.populateFromRow(labtestRecord)
            assert labtest.getId() == labtestRecord.id
            dataset.addLabtest(labtest)

    def _createExtractionTable(self):
        self.database.create_table(models.Extraction)

    def insertExtraction(self, extraction):
        """
        Inserts the specified patient into this repository.
        """
        try:
            models.Extraction.create(
                # Common fields
                id=extraction.getId(),
                datasetId=extraction.getParentContainer().getId(),
                created=extraction.getCreated(),
                updated=extraction.getUpdated(),
                name=extraction.getLocalId(),
                description=extraction.getDescription(),
                attributes=json.dumps(extraction.getAttributes()),
                # Unique fields
                extractionId=extraction.getExtractionId(),
                extractionIdTier=extraction.getExtractionIdTier(),
                sampleId=extraction.getSampleId(),
                sampleIdTier=extraction.getSampleIdTier(),
                rnaBlood=extraction.getRnaBlood(),
                rnaBloodTier=extraction.getRnaBloodTier(),
                dnaBlood=extraction.getDnaBlood(),
                dnaBloodTier=extraction.getDnaBloodTier(),
                rnaTissue=extraction.getRnaTissue(),
                rnaTissueTier=extraction.getRnaTissueTier(),
                dnaTissue=extraction.getDnaTissue(),
                dnaTissueTier=extraction.getDnaTissueTier(),
                site=extraction.getSite(),
                siteTier=extraction.getSiteTier()
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                extraction.getLocalId(),
                extraction.getParentContainer().getLocalId())

    def _readExtractionTable(self):
        """
        Read the Extraction table upon load
        """
        for extractionRecord in models.Extraction.select():
            dataset = self.getDataset(extractionRecord.datasetid.id)
            extraction = pipeline_metadata.Extraction(
                dataset, extractionRecord.name)
            extraction.populateFromRow(extractionRecord)
            assert extraction.getId() == extractionRecord.id
            dataset.addExtraction(extraction)

    def _createSequencingTable(self):
        self.database.create_table(models.Sequencing)

    def insertSequencing(self, sequencing):
        """
        Inserts the specified patient into this repository.
        """
        try:
            models.Sequencing.create(
                # Common fields
                id=sequencing.getId(),
                datasetId=sequencing.getParentContainer().getId(),
                created=sequencing.getCreated(),
                updated=sequencing.getUpdated(),
                name=sequencing.getLocalId(),
                description=sequencing.getDescription(),
                attributes=json.dumps(sequencing.getAttributes()),
                # Unique fields
                sequencingId=sequencing.getSequencingId(),
                sequencingIdTier=sequencing.getSequencingIdTier(),
                sampleId=sequencing.getSampleId(),
                sampleIdTier=sequencing.getSampleIdTier(),
                dnaLibraryKit=sequencing.getDnaLibraryKit(),
                dnaLibraryKitTier=sequencing.getDnaLibraryKitTier(),
                dnaSeqPlatform=sequencing.getDnaSeqPlatform(),
                dnaSeqPlatformTier=sequencing.getDnaSeqPlatformTier(),
                dnaReadLength=sequencing.getDnaReadLength(),
                dnaReadLengthTier=sequencing.getDnaReadLengthTier(),
                rnaLibraryKit=sequencing.getRnaLibraryKit(),
                rnaLibraryKitTier=sequencing.getRnaLibraryKitTier(),
                rnaSeqPlatform=sequencing.getRnaSeqPlatform(),
                rnaSeqPlatformTier=sequencing.getRnaSeqPlatformTier(),
                rnaReadLength=sequencing.getRnaReadLength(),
                rnaReadLengthTier=sequencing.getRnaReadLengthTier(),
                pcrCycles=sequencing.getPcrCycles(),
                pcrCyclesTier=sequencing.getPcrCyclesTier(),
                extractionId=sequencing.getExtractionId(),
                extractionIdTier=sequencing.getExtractionIdTier(),
                site=sequencing.getSite(),
                siteTier=sequencing.getSiteTier()
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                sequencing.getLocalId(),
                sequencing.getParentContainer().getLocalId())

    def _readSequencingTable(self):
        """
        Read the Sequencing table upon load
        """
        for sequencingRecord in models.Sequencing.select():
            dataset = self.getDataset(sequencingRecord.datasetid.id)
            sequencing = pipeline_metadata.Sequencing(
                dataset, sequencingRecord.name)
            sequencing.populateFromRow(sequencingRecord)
            assert sequencing.getId() == sequencingRecord.id
            dataset.addSequencing(sequencing)

    def _createAlignmentTable(self):
        self.database.create_table(models.Alignment)

    def insertAlignment(self, alignment):
        """
        Inserts the specified patient into this repository.
        """
        try:
            models.Alignment.create(
                # Common fields
                id=alignment.getId(),
                datasetId=alignment.getParentContainer().getId(),
                created=alignment.getCreated(),
                updated=alignment.getUpdated(),
                name=alignment.getLocalId(),
                description=alignment.getDescription(),
                attributes=json.dumps(alignment.getAttributes()),
                # Unique fields
                alignmentId=alignment.getAlignmentId(),
                alignmentIdTier=alignment.getAlignmentIdTier(),
                sampleId=alignment.getSampleId(),
                sampleIdTier=alignment.getSampleIdTier(),
                alignmentTool=alignment.getAlignmentTool(),
                alignmentToolTier=alignment.getAlignmentToolTier(),
                mergeTool=alignment.getMergeTool(),
                mergeToolTier=alignment.getMergeToolTier(),
                inHousePipeline=alignment.getInHousePipeline(),
                inHousePipelineTier=alignment.getInHousePipelineTier(),
                markDuplicates=alignment.getMarkDuplicates(),
                markDuplicatesTier=alignment.getMarkDuplicatesTier(),
                realignerTarget=alignment.getRealignerTarget(),
                realignerTargetTier=alignment.getRealignerTargetTier(),
                indelRealigner=alignment.getIndelRealigner(),
                indelRealignerTier=alignment.getIndelRealignerTier(),
                coverage=alignment.getCoverage(),
                coverageTier=alignment.getCoverageTier(),
                baseRecalibrator=alignment.getBaseRecalibrator(),
                baseRecalibratorTier=alignment.getBaseRecalibratorTier(),
                printReads=alignment.getPrintReads(),
                printReadsTier=alignment.getPrintReadsTier(),
                idxStats=alignment.getIdxStats(),
                idxStatsTier=alignment.getIdxStatsTier(),
                flagStat=alignment.getFlagStat(),
                flagStatTier=alignment.getFlagStatTier(),
                insertSizeMetrics=alignment.getInsertSizeMetrics(),
                insertSizeMetricsTier=alignment.getInsertSizeMetricsTier(),
                fastqc=alignment.getFastqc(),
                fastqcTier=alignment.getFastqcTier(),
                reference=alignment.getReference(),
                referenceTier=alignment.getReferenceTier(),
                sequencingId=alignment.getSequencingId(),
                sequencingIdTier=alignment.getSequencingIdTier(),
                site=alignment.getSite(),
                siteTier=alignment.getSiteTier()
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                alignment.getLocalId(),
                alignment.getParentContainer().getLocalId())

    def _readAlignmentTable(self):
        """
        Read the Alignment table upon load
        """
        for alignmentRecord in models.Alignment.select():
            dataset = self.getDataset(alignmentRecord.datasetid.id)
            alignment = pipeline_metadata.Alignment(
                dataset, alignmentRecord.name)
            alignment.populateFromRow(alignmentRecord)
            assert alignment.getId() == alignmentRecord.id
            dataset.addAlignment(alignment)

    def _createVariantCallingTable(self):
        self.database.create_table(models.VariantCalling)

    def insertVariantCalling(self, variantCalling):
        """
        Inserts the specified patient into this repository.
        """
        try:
            models.VariantCalling.create(
                # Common fields
                id=variantCalling.getId(),
                datasetId=variantCalling.getParentContainer().getId(),
                created=variantCalling.getCreated(),
                updated=variantCalling.getUpdated(),
                name=variantCalling.getLocalId(),
                description=variantCalling.getDescription(),
                attributes=json.dumps(variantCalling.getAttributes()),
                # Unique fields
                variantCallingId=variantCalling.getVariantCallingId(),
                variantCallingIdTier=variantCalling.getVariantCallingIdTier(),
                sampleId=variantCalling.getSampleId(),
                sampleIdTier=variantCalling.getSampleIdTier(),
                variantCaller=variantCalling.getVariantCaller(),
                variantCallerTier=variantCalling.getVariantCallerTier(),
                tabulate=variantCalling.getTabulate(),
                tabulateTier=variantCalling.getTabulateTier(),
                inHousePipeline=variantCalling.getInHousePipeline(),
                inHousePipelineTier=variantCalling.getInHousePipelineTier(),
                annotation=variantCalling.getAnnotation(),
                annotationTier=variantCalling.getAnnotationTier(),
                mergeTool=variantCalling.getMergeTool(),
                mergeToolTier=variantCalling.getMergeToolTier(),
                rdaToTab=variantCalling.getRdaToTab(),
                rdaToTabTier=variantCalling.getRdaToTabTier(),
                delly=variantCalling.getDelly(),
                dellyTier=variantCalling.getDellyTier(),
                postFilter=variantCalling.getPostFilter(),
                postFilterTier=variantCalling.getPostFilterTier(),
                clipFilter=variantCalling.getClipFilter(),
                clipFilterTier=variantCalling.getClipFilterTier(),
                cosmic=variantCalling.getCosmic(),
                cosmicTier=variantCalling.getCosmicTier(),
                dbSnp=variantCalling.getDbSnp(),
                dbSnpTier=variantCalling.getDbSnpTier(),
                alignmentId=variantCalling.getAlignmentId(),
                alignmentIdTier=variantCalling.getAlignmentIdTier(),
                site=variantCalling.getSite(),
                siteTier=variantCalling.getSiteTier()

            )
        except Exception:
            raise exceptions.DuplicateNameException(
                variantCalling.getLocalId(),
                variantCalling.getParentContainer().getLocalId())

    def _readVariantCallingTable(self):
        """
        Read the VariantCalling table upon load
        """
        for variantCallingRecord in models.VariantCalling.select():
            dataset = self.getDataset(variantCallingRecord.datasetid.id)
            variantCalling = pipeline_metadata.VariantCalling(
                dataset, variantCallingRecord.name)
            variantCalling.populateFromRow(variantCallingRecord)
            assert variantCalling.getId() == variantCallingRecord.id
            dataset.addVariantCalling(variantCalling)

    def _createFusionDetectionTable(self):
        self.database.create_table(models.FusionDetection)

    def insertFusionDetection(self, fusionDetection):
        """
        Inserts the specified patient into this repository.
        """
        try:
            models.FusionDetection.create(
                # Common fields
                id=fusionDetection.getId(),
                datasetId=fusionDetection.getParentContainer().getId(),
                created=fusionDetection.getCreated(),
                updated=fusionDetection.getUpdated(),
                name=fusionDetection.getLocalId(),
                description=fusionDetection.getDescription(),
                attributes=json.dumps(fusionDetection.getAttributes()),
                # Unique fields
                fusionDetectionId=fusionDetection.getFusionDetectionId(),
                fusionDetectionIdTier=fusionDetection.getFusionDetectionIdTier(),
                sampleId=fusionDetection.getSampleId(),
                sampleIdTier=fusionDetection.getSampleIdTier(),
                inHousePipeline=fusionDetection.getInHousePipeline(),
                inHousePipelineTier=fusionDetection.getInHousePipelineTier(),
                svDetection=fusionDetection.getSvDetection(),
                svDetectionTier=fusionDetection.getSvDetectionTier(),
                fusionDetection=fusionDetection.getFusionDetection(),
                fusionDetectionTier=fusionDetection.getFusionDetectionTier(),
                realignment=fusionDetection.getRealignment(),
                realignmentTier=fusionDetection.getRealignmentTier(),
                annotation=fusionDetection.getAnnotation(),
                annotationTier=fusionDetection.getAnnotationTier(),
                genomeReference=fusionDetection.getGenomeReference(),
                genomeReferenceTier=fusionDetection.getGenomeReferenceTier(),
                geneModels=fusionDetection.getGeneModels(),
                geneModelsTier=fusionDetection.getGeneModelsTier(),
                alignmentId=fusionDetection.getAlignmentId(),
                alignmentIdTier=fusionDetection.getAlignmentIdTier(),
                site=fusionDetection.getSite(),
                siteTier=fusionDetection.getSiteTier()
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                fusionDetection.getLocalId(),
                fusionDetection.getParentContainer().getLocalId())

    def _readFusionDetectionTable(self):
        """
        Read the FusionDetection table upon load
        """
        for fusionDetectionRecord in models.FusionDetection.select():
            dataset = self.getDataset(fusionDetectionRecord.datasetid.id)
            fusionDetection = pipeline_metadata.FusionDetection(
                dataset, fusionDetectionRecord.name)
            fusionDetection.populateFromRow(fusionDetectionRecord)
            assert fusionDetection.getId() == fusionDetectionRecord.id
            dataset.addFusionDetection(fusionDetection)

    def _createExpressionAnalysisTable(self):
        self.database.create_table(models.ExpressionAnalysis)

    def insertExpressionAnalysis(self, expressionAnalysis):
        """
        Inserts the specified patient into this repository.
        """
        try:
            models.ExpressionAnalysis.create(
                # Common fields
                id=expressionAnalysis.getId(),
                datasetId=expressionAnalysis.getParentContainer().getId(),
                created=expressionAnalysis.getCreated(),
                updated=expressionAnalysis.getUpdated(),
                name=expressionAnalysis.getLocalId(),
                description=expressionAnalysis.getDescription(),
                attributes=json.dumps(expressionAnalysis.getAttributes()),
                # Unique fields
                expressionAnalysisId=expressionAnalysis.getExpressionAnalysisId(),
                expressionAnalysisIdTier=expressionAnalysis.getExpressionAnalysisIdTier(),
                sampleId=expressionAnalysis.getSampleId(),
                sampleIdTier=expressionAnalysis.getSampleIdTier(),
                readLength=expressionAnalysis.getReadLength(),
                readLengthTier=expressionAnalysis.getReadLengthTier(),
                reference=expressionAnalysis.getReference(),
                referenceTier=expressionAnalysis.getReferenceTier(),
                alignmentTool=expressionAnalysis.getAlignmentTool(),
                alignmentToolTier=expressionAnalysis.getAlignmentToolTier(),
                bamHandling=expressionAnalysis.getBamHandling(),
                bamHandlingTier=expressionAnalysis.getBamHandlingTier(),
                expressionEstimation=expressionAnalysis.getExpressionEstimation(),
                expressionEstimationTier=expressionAnalysis.getExpressionEstimationTier(),
                sequencingId=expressionAnalysis.getSequencingId(),
                sequencingIdTier=expressionAnalysis.getSequencingIdTier(),
                site=expressionAnalysis.getSite(),
                siteTier=expressionAnalysis.getSiteTier()
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                expressionAnalysis.getLocalId(),
                expressionAnalysis.getParentContainer().getLocalId())

    def _readExpressionAnalysisTable(self):
        """
        Read the ExpressionAnalysis table upon load
        """
        for expressionAnalysisRecord in models.ExpressionAnalysis.select():
            dataset = self.getDataset(expressionAnalysisRecord.datasetid.id)
            expressionAnalysis = pipeline_metadata.ExpressionAnalysis(
                dataset, expressionAnalysisRecord.name)
            expressionAnalysis.populateFromRow(expressionAnalysisRecord)
            assert expressionAnalysis.getId() == expressionAnalysisRecord.id
            dataset.addExpressionAnalysis(expressionAnalysis)

    def _createIndividualTable(self):
        self.database.create_table(models.Individual)

    def insertIndividual(self, individual):
        """
        Inserts the specified individual into this repository.
        """
        try:
            models.Individual.create(
                id=individual.getId(),
                datasetId=individual.getParentContainer().getId(),
                name=individual.getLocalId(),
                description=individual.getDescription(),
                created=individual.getCreated(),
                updated=individual.getUpdated(),
                species=json.dumps(individual.getSpecies()),
                sex=json.dumps(individual.getSex()),
                attributes=json.dumps(individual.getAttributes()),
                patient_id = individual.getPatientId(),
                regional_profiling_centre = individual.getRegionalProfilingCentre(),
                diagnosis = individual.getDiagnosis(),
                pathology_type = individual.getPathologyType(),
                enrollment_approval_date = individual.getEnrollmentApprovalDate(),
                enrollment_approval_initials = individual.getEnrollmentApprovalInitials(),
                date_of_upload_to_sFTP = individual.getDateOfUploadToSftp(),
                tumor_board_presentation_date_and_analyses = individual.getTumorBoardPresentationDateAndAnalyses(),
                comments = individual.getComments(),
            )
        except Exception:
            raise exceptions.DuplicateNameException(
                individual.getLocalId(),
                individual.getParentContainer().getLocalId())

    def _readIndividualTable(self):
        for individualRecord in models.Individual.select():
            dataset = self.getDataset(individualRecord.datasetid.id)
            individual = biodata.Individual(
                dataset, individualRecord.name)
            individual.populateFromRow(individualRecord)
            assert individual.getId() == individualRecord.id
            dataset.addIndividual(individual)

    def _createPhenotypeAssociationSetTable(self):
        self.database.create_table(models.Phenotypeassociationset)

    def _createRnaQuantificationSetTable(self):
        self.database.create_table(models.Rnaquantificationset)

    def insertPhenotypeAssociationSet(self, phenotypeAssociationSet):
        """
        Inserts the specified phenotype annotation set into this repository.
        """
        datasetId = phenotypeAssociationSet.getParentContainer().getId()
        attributes = json.dumps(phenotypeAssociationSet.getAttributes())
        try:
            models.Phenotypeassociationset.create(
                id=phenotypeAssociationSet.getId(),
                name=phenotypeAssociationSet.getLocalId(),
                datasetid=datasetId,
                dataurl=phenotypeAssociationSet._dataUrl,
                attributes=attributes)
        except Exception:
            raise exceptions.DuplicateNameException(
                phenotypeAssociationSet.getParentContainer().getId())

    def _readPhenotypeAssociationSetTable(self):
        for associationSetRecord in models.Phenotypeassociationset.select():
            dataset = self.getDataset(associationSetRecord.datasetid.id)
            phenotypeAssociationSet = \
                genotype_phenotype.RdfPhenotypeAssociationSet(
                    dataset,
                    associationSetRecord.name,
                    associationSetRecord.dataurl)
            dataset.addPhenotypeAssociationSet(phenotypeAssociationSet)

    def insertRnaQuantificationSet(self, rnaQuantificationSet):
        """
        Inserts a the specified rnaQuantificationSet into this repository.
        """
        try:
            models.Rnaquantificationset.create(
                id=rnaQuantificationSet.getId(),
                datasetid=rnaQuantificationSet.getParentContainer().getId(),
                referencesetid=rnaQuantificationSet.getReferenceSet().getId(),
                name=rnaQuantificationSet.getLocalId(),
                dataurl=rnaQuantificationSet.getDataUrl(),
                attributes=json.dumps(rnaQuantificationSet.getAttributes()))
        except Exception:
            raise exceptions.DuplicateNameException(
                rnaQuantificationSet.getLocalId(),
                rnaQuantificationSet.getParentContainer().getLocalId())

    def _readRnaQuantificationSetTable(self):
        for quantificationSetRecord in models.Rnaquantificationset.select():
            dataset = self.getDataset(quantificationSetRecord.datasetid.id)
            referenceSet = self.getReferenceSet(
                quantificationSetRecord.referencesetid.id)
            rnaQuantificationSet = \
                rna_quantification.SqliteRnaQuantificationSet(
                    dataset, quantificationSetRecord.name)
            rnaQuantificationSet.setReferenceSet(referenceSet)
            rnaQuantificationSet.populateFromRow(quantificationSetRecord)
            assert rnaQuantificationSet.getId() == quantificationSetRecord.id
            dataset.addRnaQuantificationSet(rnaQuantificationSet)

    def removeRnaQuantificationSet(self, rnaQuantificationSet):
        """
        Removes the specified rnaQuantificationSet from this repository. This
        performs a cascading removal of all items within this
        rnaQuantificationSet.
        """
        q = models.Rnaquantificationset.delete().where(
            models.Rnaquantificationset.id == rnaQuantificationSet.getId())
        q.execute()

    def insertPeer(self, peer):
        """
        Accepts a peer datamodel object and adds it to the registry.
        """
        try:
            models.Peer.create(
                url=peer.getUrl(),
                attributes=json.dumps(peer.getAttributes()))
        except Exception as e:
            raise exceptions.RepoManagerException(e)

    def removePeer(self, url):
        """
        Remove peers by URL.
        """
        q = models.Peer.delete().where(
            models.Peer.url == url)
        q.execute()

    def removePeers(self):
        """
        Remove all peers from the Peers table.
        """
        try:
            q = models.Peer.delete()
            q.execute()
        except Exception as e:
            raise exceptions.RepoManagerException(e)

    def _createNetworkTables(self):
        """"""
        self.database.create_table(models.Peer)
        self.database.create_table(models.Announcement)

    def initialise(self):
        """
        Initialise this data repository, creating any necessary directories
        and file paths.
        """
        self._checkWriteMode()
        self._createSystemTable()
        self._createNetworkTables()
        self._createOntologyTable()
        self._createReferenceSetTable()
        self._createReferenceTable()
        self._createDatasetTable()
        self._createReadGroupSetTable()
        self._createReadGroupTable()
        self._createCallSetTable()
        self._createVariantSetTable()
        self._createVariantAnnotationSetTable()
        self._createFeatureSetTable()
        self._createContinuousSetTable()
        self._createBiosampleTable()
        self._createExperimentTable()
        self._createAnalysisTable()
        self._createIndividualTable()
        self._createPhenotypeAssociationSetTable()
        self._createRnaQuantificationSetTable()
        self._createPatientTable()
        self._createEnrollmentTable()
        self._createConsentTable()
        self._createDiagnosisTable()
        self._createSampleTable()
        self._createTreatmentTable()
        self._createOutcomeTable()
        self._createComplicationTable()
        self._createTumourboardTable()
        self._createChemotherapyTable()
        self._createRadiotherapyTable()
        self._createSurgeryTable()
        self._createImmunotherapyTable()
        self._createCelltransplantTable()
        self._createSlideTable()
        self._createStudyTable()
        self._createLabtestTable()
        self._createExtractionTable()
        self._createSequencingTable()
        self._createAlignmentTable()
        self._createVariantCallingTable()
        self._createFusionDetectionTable()
        self._createExpressionAnalysisTable()

    def exists(self):
        """
        Checks that this data repository exists in the file system and has the
        required structure.
        """
        # TODO should this invoke a full load operation or just check the DB
        # exists?
        return os.path.exists(self._dbFilename)

    def assertExists(self):
        if not self.exists():
            raise exceptions.RepoNotFoundException(self._dbFilename)

    def delete(self):
        """
        Delete this data repository by recursively removing all directories.
        This will delete ALL data stored within the repository!!
        """
        os.unlink(self._dbFilename)

    def load(self):
        """
        Loads this data repository into memory.
        """
        self._readSystemTable()
        self._readOntologyTable()
        self._readReferenceSetTable()
        self._readReferenceTable()
        self._readDatasetTable()
        self._readExperimentTable()
        self._readAnalysisTable()
        self._readReadGroupSetTable()
        self._readReadGroupTable()
        self._readVariantSetTable()
        self._readCallSetTable()
        self._readVariantAnnotationSetTable()
        self._readFeatureSetTable()
        self._readContinuousSetTable()
        self._readBiosampleTable()
        self._readIndividualTable()
        self._readPhenotypeAssociationSetTable()
        self._readRnaQuantificationSetTable()
        self._readPatientTable()
        self._readEnrollmentTable()
        self._readConsentTable()
        self._readDiagnosisTable()
        self._readSampleTable()
        self._readTreatmentTable()
        self._readOutcomeTable()
        self._readComplicationTable()
        self._readTumourboardTable()
        self._readChemotherapyTable()
        self._readRadiotherapyTable()
        self._readSurgeryTable()
        self._readImmunotherapyTable()
        self._readCelltransplantTable()
        self._readSlideTable()
        self._readStudyTable()
        self._readLabtestTable()
        self._readExtractionTable()
        self._readSequencingTable()
        self._readAlignmentTable()
        self._readVariantCallingTable()
        self._readFusionDetectionTable()
        self._readExpressionAnalysisTable()
