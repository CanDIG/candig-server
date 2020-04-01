"""
Tests for the repo manager tool
"""

import os
import glob
import shutil
import tempfile
import subprocess
import unittest

import candig.server.exceptions as exceptions
import candig.server.datarepo as datarepo
import candig.server.cli.repomanager as cli_repomanager
import candig.server.datamodel as datamodel
import tests.paths as paths


class TestGetNameFromPath(unittest.TestCase):
    """
    Tests the method for deriving the default name of objects from file
    paths.
    """
    def testError(self):
        self.assertRaises(ValueError, cli_repomanager.getNameFromPath, "")

    def testLocalDirectory(self):
        self.assertEqual(
            cli_repomanager.getNameFromPath("no_extension"), "no_extension")
        self.assertEqual(cli_repomanager.getNameFromPath("x.y"), "x")
        self.assertEqual(cli_repomanager.getNameFromPath("x.y.z"), "x")

    def testFullPaths(self):
        self.assertEqual(
            cli_repomanager.getNameFromPath("/no_ext"), "no_ext")
        self.assertEqual(cli_repomanager.getNameFromPath("/x.y"), "x")
        self.assertEqual(cli_repomanager.getNameFromPath("/x.y.z"), "x")
        self.assertEqual(
            cli_repomanager.getNameFromPath("/a/no_ext"), "no_ext")
        self.assertEqual(cli_repomanager.getNameFromPath("/a/x.y"), "x")
        self.assertEqual(cli_repomanager.getNameFromPath("/a/x.y.z"), "x")

    def testUrls(self):
        self.assertEqual(
            cli_repomanager.getNameFromPath("file:///no_ext"), "no_ext")
        self.assertEqual(
            cli_repomanager.getNameFromPath("http://example.com/x.y"), "x")
        self.assertEqual(
            cli_repomanager.getNameFromPath("ftp://x.y.z"), "x")

    def testDirectoryName(self):
        self.assertEqual(cli_repomanager.getNameFromPath("/a/xy"), "xy")
        self.assertEqual(cli_repomanager.getNameFromPath("/a/xy/"), "xy")
        self.assertEqual(cli_repomanager.getNameFromPath("xy/"), "xy")
        self.assertEqual(cli_repomanager.getNameFromPath("xy"), "xy")


class AbstractRepoManagerTest(unittest.TestCase):
    """
    Base class for repo manager tests
    """
    def setUp(self):
        fd, self._repoPath = tempfile.mkstemp(prefix="candig_repoman_test")
        os.unlink(self._repoPath)

    def runCommand(self, cmd):
        cli_repomanager.RepoManager.runCommand(cmd.split())

    def tearDown(self):
        os.unlink(self._repoPath)

    def readRepo(self):
        repo = datarepo.SqlDataRepository(self._repoPath)
        repo.open(datarepo.MODE_READ)
        return repo

    def init(self):
        self.runCommand("init {}".format(self._repoPath))

    def addOntology(self):
        self._ontologyName = paths.ontologyName
        cmd = "add-ontology {} {}".format(self._repoPath, paths.ontologyPath)
        self.runCommand(cmd)

    def addDataset(self, datasetName=None):
        if datasetName is None:
            datasetName = "test_dataset"
            self._datasetName = datasetName
        cmd = "add-dataset {} {}".format(self._repoPath, datasetName)
        self.runCommand(cmd)

    def addReferenceSet(self):
        self._referenceSetName = "test_rs"
        fastaFile = paths.faPath
        self.runCommand("add-referenceset {} {} --name={}".format(
            self._repoPath, fastaFile, self._referenceSetName))

    def addReadGroupSet(self):
        bamFile = paths.bamPath
        self._readGroupSetName = "test_rgs"
        cmd = (
            "add-readgroupset {} {} patient1 sample1 {} --referenceSetName={} "
            "--name={}").format(
            self._repoPath, self._datasetName, bamFile,
            self._referenceSetName, self._readGroupSetName)
        self.runCommand(cmd)

    def addVariantSet(self):
        vcfDir = paths.vcfDirPath
        self._variantSetName = "test_vs"
        cmd = (
            "add-variantset {} {} patient1 sample1 {} --referenceSetName={} "
            "--name={}").format(
            self._repoPath, self._datasetName, vcfDir,
            self._referenceSetName, self._variantSetName)
        self.runCommand(cmd)

    def addFeatureSet(self):
        featuresPath = paths.featuresPath
        self._featureSetName = paths.featureSetName
        cmd = (
            "add-featureset {} {} {} --referenceSetName={} "
            "--ontologyName={}").format(
            self._repoPath, self._datasetName, featuresPath,
            self._referenceSetName, self._ontologyName)
        self.runCommand(cmd)

    def addContinuousSet(self):
        continuousPath = paths.continuousPath
        self._continuousSetName = paths.continuousSetName
        cmd = (
            "add-continuousset {} {} {} --referenceSetName={} ").format(
            self._repoPath, self._datasetName, continuousPath,
            self._referenceSetName)
        self.runCommand(cmd)

    def addPhenotypeAssociationSet(self):
        phenotypeAssociationSetPath = paths.phenotypeAssociationSetPath
        self._phenotypeAssociationSetName = "test_phenotypeAssociationSet"
        cmd = (
            "add-phenotypeassociationset {} {} {} -n {}").format(
                self._repoPath,
                self._datasetName,
                phenotypeAssociationSetPath,
                self._phenotypeAssociationSetName)
        self.runCommand(cmd)

    def addRnaQuantificationSet(self):
        self._rnaQuantificationSetPath = paths.rnaQuantificationSetDbPath
        cmd = (
            "add-rnaquantificationset {} {} {} -R {} -n {}").format(
                self._repoPath,
                self._datasetName,
                paths.rnaQuantificationSetDbPath,
                self._referenceSetName,
                "rnaseq")
        self.runCommand(cmd)

    def getFeatureSet(self):
        repo = self.readRepo()
        dataset = repo.getDatasetByName(self._datasetName)
        featureSet = dataset.getFeatureSetByName(self._featureSetName)
        return featureSet

    def getContinuousSet(self):
        repo = self.readRepo()
        dataset = repo.getDatasetByName(self._datasetName)
        continuousSet = dataset.getContinuousSetByName(self._continuousSetName)
        return continuousSet


class TestAddRnaQuantificationSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestAddRnaQuantificationSet, self).setUp()
        self.init()
        self.addDataset()
        self.addReferenceSet()

    def testDefaults(self):
        name = "rnaseq"
        self.runCommand(
            "add-rnaquantificationset {} {} {} -R {} --name {}".format(
                self._repoPath,
                self._datasetName,
                paths.rnaQuantificationSetDbPath,
                self._referenceSetName,
                name))
        repo = self.readRepo()
        dataset = repo.getDatasetByName(self._datasetName)
        rnaQuantificationSet = dataset.getRnaQuantificationSetByName(name)
        self.assertEqual(rnaQuantificationSet.getLocalId(), name)


class TestRemoveRnaQuantificationSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestRemoveRnaQuantificationSet, self).setUp()
        self.init()
        self.addDataset()
        self.addReferenceSet()

    def testDefaults(self):
        name = "rnaseq"
        cmd = (
            "add-rnaquantificationset {} {} {} -R {} -n {}").format(
                self._repoPath,
                self._datasetName,
                paths.rnaQuantificationSetDbPath,
                self._referenceSetName,
                name)
        self.runCommand(cmd)
        self.runCommand("remove-rnaquantificationset {} {} {} -f".format(
            self._repoPath,
            self._datasetName,
            name))
        repo = self.readRepo()
        dataset = repo.getDatasetByName(self._datasetName)
        self.assertRaises(
            exceptions.RnaQuantificationSetNameNotFoundException,
            dataset.getRnaQuantificationSetByName,
            name)


class TestAddFeatureSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestAddFeatureSet, self).setUp()
        self.init()
        self.addDataset()
        self.addOntology()
        self.addReferenceSet()

    def testAddFeatureSet(self):
        self.addFeatureSet()
        featureSet = self.getFeatureSet()
        self.assertEqual(featureSet.getLocalId(), self._featureSetName)
        self.assertEqual(
            featureSet._parentContainer.getLocalId(), self._datasetName)
        self.assertEqual(
            featureSet.getReferenceSet().getLocalId(),
            self._referenceSetName)
        # TODO not clear these fields get populated now
        # self.assertEqual(featureSet.getInfo(), "TODO")
        # self.assertEqual(featureSet.getSourceUrl(), "TODO")

    def testAddFeatureSetNoReferenceSet(self):
        featuresPath = paths.featuresPath
        cmd = "add-featureset {} {} {} --ontologyName={}".format(
            self._repoPath, self._datasetName, featuresPath,
            self._ontologyName)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)

    def testAddFeatureSetBadReferenceSet(self):
        featuresPath = paths.featuresPath
        cmd = (
            "add-featureset {} {} {} --referenceSetName=notafefset "
            "--ontologyName={}").format(
            self._repoPath, self._datasetName, featuresPath,
            self._ontologyName)
        self.assertRaises(
            exceptions.ReferenceSetNameNotFoundException,
            self.runCommand, cmd)

    def testAddFeatureSetNoOntology(self):
        featuresPath = paths.featuresPath
        cmd = "add-featureset {} {} {} --referenceSetName={} ".format(
            self._repoPath, self._datasetName, featuresPath,
            self._referenceSetName)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)

    def testAddFeatureSetBadOntology(self):
        featuresPath = paths.featuresPath
        cmd = "add-featureset {} {} {} --referenceSetName={} ".format(
            self._repoPath, self._datasetName, featuresPath,
            self._referenceSetName)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)


class TestRemoveFeatureSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestRemoveFeatureSet, self).setUp()
        self.init()
        self.addDataset()
        self.addOntology()
        self.addReferenceSet()
        self.addFeatureSet()

    def testRemoveFeatureSet(self):
        featureSet = self.getFeatureSet()
        cmd = "remove-featureset {} {} {} -f".format(
            self._repoPath, self._datasetName, featureSet.getLocalId())
        self.runCommand(cmd)
        with self.assertRaises(exceptions.FeatureSetNameNotFoundException):
            self.getFeatureSet()


class TestAddContinuousSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestAddContinuousSet, self).setUp()
        self.init()
        self.addDataset()
        self.addReferenceSet()

    def testAddContinuousSet(self):
        self.addContinuousSet()
        continuousSet = self.getContinuousSet()
        self.assertEqual(continuousSet.getLocalId(), self._continuousSetName)
        self.assertEqual(
            continuousSet._parentContainer.getLocalId(), self._datasetName)
        self.assertEqual(
            continuousSet.getReferenceSet().getLocalId(),
            self._referenceSetName)
        # self.assertEqual(
        #         continuousSet.getSourceUri(), self._sourceUri)

    def testAddContinuousSetNoReferenceSet(self):
        continuousPath = paths.continuousPath
        cmd = "add-continuousset {} {} {}".format(
            self._repoPath, self._datasetName, continuousPath)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)

    def testAddContinuousSetBadReferenceSet(self):
        continuousPath = paths.continuousPath
        cmd = (
            "add-continuousset {} {} {} --referenceSetName=notafefset"
        ).format(self._repoPath, self._datasetName, continuousPath)
        self.assertRaises(
            exceptions.ReferenceSetNameNotFoundException,
            self.runCommand, cmd)


class TestRemoveContinuousSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestRemoveContinuousSet, self).setUp()
        self.init()
        self.addDataset()
        self.addReferenceSet()
        self.addContinuousSet()

    def testRemoveContinuousSet(self):
        continuousSet = self.getContinuousSet()
        cmd = "remove-continuousset {} {} {} -f".format(
            self._repoPath, self._datasetName, continuousSet.getLocalId())
        self.runCommand(cmd)
        with self.assertRaises(exceptions.ContinuousSetNameNotFoundException):
            self.getContinuousSet()


class TestAddDataset(AbstractRepoManagerTest):

    def setUp(self):
        super(TestAddDataset, self).setUp()
        self.init()

    def testDefaults(self):
        name = "test_dataset"
        self.runCommand("add-dataset {} {}".format(self._repoPath, name))
        repo = self.readRepo()
        dataset = repo.getDatasetByName(name)
        self.assertEqual(dataset.getLocalId(), name)

    def testSameName(self):
        name = "test_dataset"
        cmd = "add-dataset {} {}".format(self._repoPath, name)
        self.runCommand(cmd)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)


class TestAddPhenotypeAssociationSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestAddPhenotypeAssociationSet, self).setUp()
        self.init()

    def testDefaults(self):
        self.addDataset()
        self.addPhenotypeAssociationSet()

    def testSameName(self):
        self.addDataset()
        self.addPhenotypeAssociationSet()
        with self.assertRaises(exceptions.RepoManagerException):
            self.addPhenotypeAssociationSet()


class TestRemovePhenotypeAssociationSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestRemovePhenotypeAssociationSet, self).setUp()
        self.init()

    def _assertPhenotypeAssociationSetRemoved(self):
        repo = self.readRepo()
        dataset = repo.getDatasetByName(self._datasetName)
        with self.assertRaises(
                exceptions.PhenotypeAssociationSetNotFoundException):
            dataset.getPhenotypeAssociationSetByName(
                self._phenotypeAssociationSetName)

    def _removePhenotypeAssociationSet(self):
        cmdString = "remove-phenotypeassociationset {} {} {} -f"
        self.runCommand(cmdString.format(
            self._repoPath, self._datasetName,
            self._phenotypeAssociationSetName))

    def testDefaults(self):
        self.addDataset()
        self.addPhenotypeAssociationSet()
        self._removePhenotypeAssociationSet()
        self._assertPhenotypeAssociationSetRemoved()

    def testDuplicateDelete(self):
        self.addDataset()
        self.addPhenotypeAssociationSet()
        self._removePhenotypeAssociationSet()
        self._assertPhenotypeAssociationSetRemoved()
        with self.assertRaises(
                exceptions.PhenotypeAssociationSetNotFoundException):
            self._removePhenotypeAssociationSet()


class TestAddReferenceSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestAddReferenceSet, self).setUp()
        self.init()

    def testDefaults(self):
        fastaFile = paths.ncbi37FaPath
        name = os.path.split(fastaFile)[1].split(".")[0]
        self.runCommand("add-referenceset {} {}".format(
            self._repoPath, fastaFile))
        repo = self.readRepo()
        referenceSet = repo.getReferenceSetByName(name)
        self.assertEqual(referenceSet.getLocalId(), name)
        self.assertEqual(referenceSet.getDataUrl(), os.path.abspath(fastaFile))
        # TODO check that the default values for all fields are set correctly.

    def testWithName(self):
        name = "test_reference_set"
        fastaFile = paths.ncbi37FaPath
        cmd = "add-referenceset {} {} --name={}".format(
            self._repoPath, fastaFile, name)
        self.runCommand(cmd)
        repo = self.readRepo()
        referenceSet = repo.getReferenceSetByName(name)
        self.assertEqual(referenceSet.getLocalId(), name)
        self.assertEqual(referenceSet.getDataUrl(), os.path.abspath(fastaFile))

    def testWithSameName(self):
        fastaFile = paths.ncbi37FaPath
        # Default name
        cmd = "add-referenceset {} {}".format(self._repoPath, fastaFile)
        self.runCommand(cmd)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)
        # Specified name
        cmd = "add-referenceset {} {} --name=testname".format(
            self._repoPath, fastaFile)
        self.runCommand(cmd)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)


class TestAddOntology(AbstractRepoManagerTest):

    def setUp(self):
        super(TestAddOntology, self).setUp()
        self.init()

    def testDefaults(self):
        ontologyFile = paths.ontologyPath
        name = os.path.split(ontologyFile)[1].split(".")[0]
        self.runCommand("add-ontology {} {}".format(
            self._repoPath, ontologyFile))
        repo = self.readRepo()
        ontology = repo.getOntologyByName(name)
        self.assertEqual(ontology.getName(), name)
        self.assertEqual(ontology.getDataUrl(), os.path.abspath(ontologyFile))

    def testWithName(self):
        ontologyFile = paths.ontologyPath
        name = "test_name"
        self.runCommand("add-ontology {} {} --name={}".format(
            self._repoPath, ontologyFile, name))
        repo = self.readRepo()
        ontology = repo.getOntologyByName(name)
        self.assertEqual(ontology.getName(), name)
        self.assertEqual(ontology.getDataUrl(), os.path.abspath(ontologyFile))

    def testWithSameName(self):
        ontologyFile = paths.ontologyPath
        # Default name
        cmd = "add-ontology {} {}".format(self._repoPath, ontologyFile)
        self.runCommand(cmd)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)
        # Specified name
        cmd = "add-ontology {} {} --name=testname".format(
            self._repoPath, ontologyFile)
        self.runCommand(cmd)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)

    def testMissingFile(self):
        cmd = "add-ontology {} {}".format(self._repoPath, "/no/such/file")
        self.assertRaises(
            exceptions.FileOpenFailedException, self.runCommand, cmd)

    def testNonOboTextFile(self):
        cmd = "add-ontology {} {}".format(
            self._repoPath, paths.landingMessageHtml)
        self.assertRaises(
            exceptions.OntologyFileFormatException, self.runCommand, cmd)

    def testNonOboBinaryFile(self):
        cmd = "add-ontology {} {}".format(self._repoPath, paths.bamPath)
        self.assertRaises(
            exceptions.OntologyFileFormatException, self.runCommand, cmd)


class TestRemoveDataset(AbstractRepoManagerTest):

    def setUp(self):
        super(TestRemoveDataset, self).setUp()
        self.init()
        self.addDataset()
        self.addReferenceSet()

    def assertDatasetRemoved(self):
        repo = self.readRepo()
        self.assertRaises(
            exceptions.DatasetNameNotFoundException,
            repo.getDatasetByName, self._datasetName)

    def testEmptyDatasetForce(self):
        self.runCommand("remove-dataset {} {} -f".format(
            self._repoPath, self._datasetName))
        self.assertDatasetRemoved()

    def testContainsReadGroupSet(self):
        self.addReadGroupSet()
        self.runCommand("remove-dataset {} {} -f".format(
            self._repoPath, self._datasetName))
        self.assertDatasetRemoved()


class TestRemoveReadGroupSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestRemoveReadGroupSet, self).setUp()
        self.init()
        self.addDataset()
        self.addReferenceSet()
        self.addReadGroupSet()

    def assertReadGroupSetRemoved(self):
        repo = self.readRepo()
        dataset = repo.getDatasetByName(self._datasetName)
        self.assertRaises(
            exceptions.ReadGroupSetNameNotFoundException,
            dataset.getReadGroupSetByName, self._readGroupSetName)

    def testWithForce(self):
        self.runCommand("remove-readgroupset {} {} {} -f".format(
            self._repoPath, self._datasetName, self._readGroupSetName))
        self.assertReadGroupSetRemoved()


class TestRemoveVariantSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestRemoveVariantSet, self).setUp()
        self.init()
        self.addDataset()
        self.addReferenceSet()
        self.addVariantSet()

    def assertVariantSetRemoved(self):
        repo = self.readRepo()
        dataset = repo.getDatasetByName(self._datasetName)
        self.assertRaises(
            exceptions.VariantSetNameNotFoundException,
            dataset.getVariantSetByName, self._variantSetName)

    def testWithForce(self):
        self.runCommand("remove-variantset {} {} {} -f".format(
            self._repoPath, self._datasetName, self._variantSetName))
        self.assertVariantSetRemoved()

    # TODO test when we have a variant set with the same name in
    # a different dataset. This should be unaffected.


class TestRemoveReferenceSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestRemoveReferenceSet, self).setUp()
        self.init()
        self.addReferenceSet()

    def assertReferenceSetRemoved(self):
        repo = self.readRepo()
        self.assertRaises(
            exceptions.ReferenceSetNameNotFoundException,
            repo.getReferenceSetByName, self._referenceSetName)

    def testDefaults(self):
        self.runCommand("remove-referenceset {} {} -f".format(
            self._repoPath, self._referenceSetName))
        self.assertReferenceSetRemoved()


class TestVerify(AbstractRepoManagerTest):

    def setUp(self):
        super(TestVerify, self).setUp()

    def testVerify(self):
        self.init()
        self.addDataset()
        self.addOntology()
        self.addReferenceSet()
        self.addReadGroupSet()
        self.addFeatureSet()
        self.addContinuousSet()
        self.addVariantSet()
        self.addRnaQuantificationSet()
        cmd = "verify {}".format(self._repoPath)
        self.runCommand(cmd)


class TestRemoveOntology(AbstractRepoManagerTest):

    def setUp(self):
        super(TestRemoveOntology, self).setUp()
        self.init()
        self.addOntology()

    def assertOntologyRemoved(self):
        repo = self.readRepo()
        self.assertRaises(
            exceptions.OntologyNameNotFoundException,
            repo.getOntologyByName, self._ontologyName)

    def testDefaults(self):
        self.runCommand("remove-ontology {} {} -f".format(
            self._repoPath, self._ontologyName))
        self.assertOntologyRemoved()


class TestAddReadGroupSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestAddReadGroupSet, self).setUp()
        self.init()
        self.addDataset()
        self.addReferenceSet()

    def verifyReadGroupSet(self, name, dataUrl, indexFile):
        repo = self.readRepo()
        dataset = repo.getDatasetByName(self._datasetName)
        referenceSet = repo.getReferenceSetByName(self._referenceSetName)
        readGroupSet = dataset.getReadGroupSetByName(name)
        self.assertEqual(readGroupSet.getLocalId(), name)
        self.assertEqual(readGroupSet.getReferenceSet(), referenceSet)
        self.assertEqual(readGroupSet.getDataUrl(), os.path.abspath(dataUrl))
        self.assertEqual(
            readGroupSet.getIndexFile(), os.path.abspath(indexFile))

    def testDefaultsLocalFile(self):
        bamFile = paths.bamPath
        name = os.path.split(bamFile)[1].split(".")[0]
        cmd = "add-readgroupset {} {} patient1 sample1 {} --referenceSetName={}".format(
            self._repoPath, self._datasetName, bamFile,
            self._referenceSetName)
        self.runCommand(cmd)
        self.verifyReadGroupSet(name, bamFile, bamFile + ".bai")

    def testLocalFileWithIndex(self):
        bamFile = paths.bamPath
        name = os.path.split(bamFile)[1].split(".")[0]
        with tempfile.NamedTemporaryFile() as temp:
            indexFile = temp.name
            shutil.copyfile(bamFile + ".bai", indexFile)
            cmd = (
                "add-readgroupset {} {} patient1 sample1 {} -I {} "
                "--referenceSetName={}").format(
                    self._repoPath, self._datasetName, bamFile,
                    indexFile, self._referenceSetName)
            self.runCommand(cmd)
            self.verifyReadGroupSet(name, bamFile, indexFile)

    def testLocalFileWithName(self):
        bamFile = paths.bamPath
        name = "test_rgs"
        cmd = (
            "add-readgroupset {} {} patient1 sample1 {} --referenceSetName={} "
            "--name={}").format(
            self._repoPath, self._datasetName, bamFile,
            self._referenceSetName, name)
        self.runCommand(cmd)
        self.verifyReadGroupSet(name, bamFile, bamFile + ".bai")

    def testAddReadGroupSetWithSameName(self):
        # Default name
        bamFile = paths.bamPath
        name = os.path.split(bamFile)[1].split(".")[0]
        cmd = "add-readgroupset {} {} patient1 sample1 {} --referenceSetName={}".format(
            self._repoPath, self._datasetName, bamFile,
            self._referenceSetName)
        self.runCommand(cmd)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)
        # Specified name
        name = "test_rgs"
        cmd = (
            "add-readgroupset {} {} patient1 sample1 {} --referenceSetName={} "
            "--name={}").format(
            self._repoPath, self._datasetName, bamFile,
            self._referenceSetName, name)
        self.runCommand(cmd)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)

    def testUrlWithMissingIndex(self):
        bamFile = "http://example.com/example.bam"
        cmd = "add-readgroupset {} {} patient1 sample1 {} --referenceSetName={}".format(
            self._repoPath, self._datasetName, bamFile,
            self._referenceSetName)
        self.assertRaises(
            exceptions.MissingIndexException, self.runCommand, cmd)

    def testMissingDataset(self):
        bamFile = paths.bamPath
        cmd = "add-readgroupset {} {} patient1 sample1 {} --referenceSetName={}".format(
            self._repoPath, "not_a_dataset_name", bamFile,
            self._referenceSetName)
        self.assertRaises(
            exceptions.DatasetNameNotFoundException, self.runCommand, cmd)

    def testMissingReferenceSet(self):
        bamFile = paths.bamPath
        cmd = "add-readgroupset {} {} patient1 sample1 {} --referenceSetName={}".format(
            self._repoPath, self._datasetName, bamFile,
            "not_a_referenceset_name")
        self.assertRaises(
            exceptions.ReferenceSetNameNotFoundException, self.runCommand, cmd)


class TestAddVariantSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestAddVariantSet, self).setUp()
        self.init()
        self.addDataset()
        self.addReferenceSet()
        self.vcfDir = paths.vcfDirPath
        self.vcfFiles = glob.glob(os.path.join(paths.vcfDirPath, "*.vcf.gz"))
        self.indexFiles = [vcfFile + ".tbi" for vcfFile in self.vcfFiles]

    def verifyVariantSet(self, name, dataUrls, indexFiles):
        repo = self.readRepo()
        dataset = repo.getDatasetByName(self._datasetName)
        referenceSet = repo.getReferenceSetByName(self._referenceSetName)
        variantSet = dataset.getVariantSetByName(name)
        self.assertEqual(variantSet.getLocalId(), name)
        self.assertEqual(variantSet.getReferenceSet(), referenceSet)
        dataUrls = [os.path.abspath(x) for x in dataUrls]
        indexFiles = [os.path.abspath(x) for x in indexFiles]
        pairs = sorted(zip(dataUrls, indexFiles))
        self.assertEqual(pairs, sorted(variantSet.getDataUrlIndexPairs()))

    def testDefaultsLocalFiles(self):
        dataFiles = self.vcfFiles
        name = "test_name"
        cmd = "add-variantset {} {} patient1 sample1 {} --name={} --referenceSetName={}".format(
            self._repoPath, self._datasetName, " ".join(dataFiles),
            name, self._referenceSetName)
        self.runCommand(cmd)
        self.verifyVariantSet(name, dataFiles, self.indexFiles)

    def testDefaultsLocalDirectory(self):
        vcfDir = self.vcfDir
        name = os.path.split(vcfDir)[1]
        cmd = "add-variantset {} {} patient1 sample1 {} --referenceSetName={}".format(
            self._repoPath, self._datasetName, vcfDir,
            self._referenceSetName)
        self.runCommand(cmd)
        self.verifyVariantSet(name, self.vcfFiles, self.indexFiles)

    def testLocalFilesWithIndexes(self):
        dataFiles = self.vcfFiles
        tempdir = tempfile.mkdtemp(prefix="ga4gh_test_add_variantset")
        name = "test_name"
        try:
            indexFiles = []
            for indexFile in self.indexFiles:
                indexFileCopy = os.path.join(
                    tempdir, os.path.split(indexFile)[1])
                shutil.copyfile(indexFile, indexFileCopy)
                indexFiles.append(indexFileCopy)
            cmd = (
                "add-variantset {} {} patient1 sample1 {} -I {} --name={} "
                "--referenceSetName={}".format(
                    self._repoPath, self._datasetName, " ".join(dataFiles),
                    " ".join(indexFiles), name, self._referenceSetName))
            self.runCommand(cmd)
            self.verifyVariantSet(name, dataFiles, indexFiles)
        finally:
            shutil.rmtree(tempdir)

    def testAddVariantSetWithSameName(self):
        # Default name
        vcfDir = self.vcfDir
        name = os.path.split(vcfDir)[1]
        cmd = "add-variantset {} {} patient1 sample1 {} --referenceSetName={}".format(
            self._repoPath, self._datasetName, vcfDir,
            self._referenceSetName)
        self.runCommand(cmd)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)
        # Specified name
        name = "test_vs"
        cmd = (
            "add-variantset {} {} patient1 sample1 {} --referenceSetName={} "
            "--name={}").format(
            self._repoPath, self._datasetName, vcfDir,
            self._referenceSetName, name)
        self.runCommand(cmd)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)

    def testUrlWithMissingIndex(self):
        dataFile = "http://example.com/example.vcf.gz"
        cmd = "add-variantset {} {} patient1 sample1 {} --referenceSetName={}".format(
            self._repoPath, self._datasetName, dataFile,
            self._referenceSetName)
        self.assertRaises(
            exceptions.MissingIndexException, self.runCommand, cmd)

    def testMissingDataset(self):
        cmd = "add-variantset {} {} patient1 sample1 {} --referenceSetName={}".format(
            self._repoPath, "not_a_dataset_name", self.vcfDir,
            self._referenceSetName)
        self.assertRaises(
            exceptions.DatasetNameNotFoundException, self.runCommand, cmd)

    def testMissingReferenceSet(self):
        cmd = "add-variantset {} {} patient1 sample1 {} --referenceSetName={}".format(
            self._repoPath, self._datasetName, self.vcfDir,
            "not_a_referenceset_name")
        self.assertRaises(
            exceptions.ReferenceSetNameNotFoundException, self.runCommand, cmd)

    # TODO add more tests for to verify that errors are correctly thrown
    # when incorrect indexes are passed, mixtures of directories and URLS
    # for the dataFiles argument, and other common error cases in the UI.


class TestAddAnnotatedVariantSet(AbstractRepoManagerTest):

    def setUp(self):
        super(TestAddAnnotatedVariantSet, self).setUp()
        self.init()
        self.addDataset()
        self.addReferenceSet()
        self.addOntology()
        self.vcfDir = paths.annotatedVcfPath

    def testNoAnnotations(self):
        name = "test_vs_no_annotations"
        cmd = "add-variantset {} {} patient1 sample1 {} -R {} -n {}".format(
            self._repoPath, self._datasetName, self.vcfDir,
            self._referenceSetName, name)
        self.runCommand(cmd)
        repo = self.readRepo()
        dataset = repo.getDatasetByName(self._datasetName)
        variantSet = dataset.getVariantSetByName(name)
        self.assertEqual(len(variantSet.getVariantAnnotationSets()), 0)

    def testAnnotations(self):
        name = "test_vs_annotations"
        cmd = "add-variantset {} {} patient1 sample1 {} -R {} -n {} -aO {}".format(
            self._repoPath, self._datasetName, self.vcfDir,
            self._referenceSetName, name, self._ontologyName)
        self.runCommand(cmd)
        repo = self.readRepo()
        dataset = repo.getDatasetByName(self._datasetName)
        variantSet = dataset.getVariantSetByName(name)
        self.assertEqual(len(variantSet.getVariantAnnotationSets()), 1)

    def testAnnotationsNoOntology(self):
        name = "test_vs_annotations"
        cmd = "add-variantset {} {} patient1 sample1 {} -R {} -n {} -a".format(
            self._repoPath, self._datasetName, self.vcfDir,
            self._referenceSetName, name)
        self.assertRaises(
            exceptions.RepoManagerException, self.runCommand, cmd)

    def testAnnotationsBadOntology(self):
        name = "test_vs_annotations"
        cmd = "add-variantset {} {} patient1 sample1 {} -R {} -n {} -aO {}".format(
            self._repoPath, self._datasetName, self.vcfDir,
            self._referenceSetName, name, "not_an_ontology")
        self.assertRaises(
            exceptions.OntologyNameNotFoundException, self.runCommand, cmd)


class TestDuplicateNameDelete(AbstractRepoManagerTest):
    """
    If two objects exist with the same name in different datasets,
    ensure that only one is deleted on a delete call
    """
    def setUp(self):
        super(TestDuplicateNameDelete, self).setUp()
        self.init()
        self.dataset1Name = "dataset1"
        self.dataset2Name = "dataset2"
        self.addDataset(self.dataset1Name)
        self.addDataset(self.dataset2Name)
        self.addOntology()
        self.addReferenceSet()

    def readDatasets(self):
        repo = self.readRepo()
        self.dataset1 = repo.getDatasetByName(self.dataset1Name)
        self.dataset2 = repo.getDatasetByName(self.dataset2Name)

    def testReadGroupSetDelete(self):
        readGroupSetName = "test_rgs"
        cmdString = (
            "add-readgroupset {} {} patient1 sample1 {} --referenceSetName={} "
            "--name={}")
        addReadGroupSetCmd1 = cmdString.format(
            self._repoPath, self.dataset1Name, paths.bamPath,
            self._referenceSetName, readGroupSetName)
        self.runCommand(addReadGroupSetCmd1)
        addReadGroupSetCmd2 = cmdString.format(
            self._repoPath, self.dataset2Name, paths.bamPath,
            self._referenceSetName, readGroupSetName)
        self.runCommand(addReadGroupSetCmd2)
        removeCmd = "remove-readgroupset {} {} {} -f".format(
            self._repoPath, self.dataset1Name, readGroupSetName)
        self.runCommand(removeCmd)
        self.readDatasets()
        self.assertEqual(len(self.dataset1.getReadGroupSets()), 0)
        self.assertEqual(len(self.dataset2.getReadGroupSets()), 1)

    def testVariantSetDelete(self):
        vcfDir = paths.vcfDirPath
        variantSetName = "test_vs"
        cmdString = "add-variantset {} {} patient1 sample1 {} --referenceSetName={} --name={}"
        addVariantSetCmd1 = cmdString.format(
            self._repoPath, self.dataset1Name, vcfDir,
            self._referenceSetName, variantSetName)
        self.runCommand(addVariantSetCmd1)
        addVariantSetCmd2 = cmdString.format(
            self._repoPath, self.dataset2Name, vcfDir,
            self._referenceSetName, variantSetName)
        self.runCommand(addVariantSetCmd2)
        removeCmd = "remove-variantset {} {} {} -f".format(
            self._repoPath, self.dataset1Name, variantSetName)
        self.runCommand(removeCmd)
        self.readDatasets()
        self.assertEqual(len(self.dataset1.getVariantSets()), 0)
        self.assertEqual(len(self.dataset2.getVariantSets()), 1)

    def testFeatureSetDelete(self):
        cmdString = "add-featureset {} {} {} -R {} -O {}"
        addFeatureSetCmd1 = cmdString.format(
            self._repoPath, self.dataset1Name, paths.featuresPath,
            self._referenceSetName, self._ontologyName)
        self.runCommand(addFeatureSetCmd1)
        addFeatureSetCmd2 = cmdString.format(
            self._repoPath, self.dataset2Name, paths.featuresPath,
            self._referenceSetName, self._ontologyName)
        self.runCommand(addFeatureSetCmd2)
        removeCmd = "remove-featureset {} {} {} -f".format(
            self._repoPath, self.dataset1Name, paths.featureSetName)
        self.runCommand(removeCmd)
        self.readDatasets()
        self.assertEqual(len(self.dataset1.getFeatureSets()), 0)
        self.assertEqual(len(self.dataset2.getFeatureSets()), 1)

    def testContinuousSetDelete(self):
        cmdString = "add-continuousset {} {} {} -R {}"
        addContinuousSetCmd1 = cmdString.format(
            self._repoPath, self.dataset1Name, paths.continuousPath,
            self._referenceSetName)
        self.runCommand(addContinuousSetCmd1)
        addContinuousSetCmd2 = cmdString.format(
            self._repoPath, self.dataset2Name, paths.continuousPath,
            self._referenceSetName)
        self.runCommand(addContinuousSetCmd2)
        removeCmd = "remove-continuousset {} {} {} -f".format(
            self._repoPath, self.dataset1Name, paths.continuousSetName)
        self.runCommand(removeCmd)
        self.readDatasets()
        self.assertEqual(len(self.dataset1.getContinuousSets()), 0)


class TestInvalidVariantIndexFile(AbstractRepoManagerTest):
    """
    Test that the repo manager throws exceptions when invalid index
    files are provided for vcf files.
    """
    def setUp(self):
        super(TestInvalidVariantIndexFile, self).setUp()
        self.init()
        self.addDataset()
        self.addReferenceSet()

    def _testWithIndexPath(self, indexPath):
        cmd = (
            "add-variantset {} {} patient1 sample1 {} --referenceSetName={} -I {}").format(
                self._repoPath, self._datasetName, paths.vcfPath1,
                self._referenceSetName, indexPath)
        with self.assertRaises(exceptions.NotIndexedException):
            self.runCommand(cmd)

    def testNonexistentIndexFile(self):
        indexPath = '/path/does/not/exist'
        self._testWithIndexPath(indexPath)

    def testIndexFileNotAnIndexFile(self):
        indexPath = paths.vcfPath2  # not an index file
        self._testWithIndexPath(indexPath)

    @unittest.skip("Skipping until we can detect incorrect indexes")
    def testWrongIndexFile(self):
        indexPath = paths.vcfIndexPath2  # incorrect index
        self._testWithIndexPath(indexPath)


class TestInvalidReadGroupSetIndexFile(AbstractRepoManagerTest):
    """
    Test that the repo manager throws exceptions when invalid index
    files are provided for bam files.
    """
    @classmethod
    def setUpClass(cls):
        # clear the file handle cache because if the data file we are
        # testing with an invalid index is already in the cache, the
        # index will not be opened during the test; without this line
        # the below tests will succeed when the test class is run but
        # fail when the file's tests are run
        datamodel.fileHandleCache = datamodel.PysamFileHandleCache()

    def setUp(self):
        super(TestInvalidReadGroupSetIndexFile, self).setUp()
        self.init()
        self.addDataset()
        self.addReferenceSet()

    def _testWithIndexPath(self, indexPath):
        cmd = (
            "add-readgroupset {} {} patient1 sample1 {} --referenceSetName={} "
            "-I {}").format(
                self._repoPath, self._datasetName, paths.bamPath,
                self._referenceSetName, indexPath)
        self.runCommand(cmd)

    def testNonexistentIndexFile(self):
        indexPath = '/path/does/not/exist'
        with self.assertRaises(exceptions.FileOpenFailedException):
            self._testWithIndexPath(indexPath)

    def testIndexFileNotAnIndexFile(self):
        indexPath = paths.bamPath2  # not an index file
        with self.assertRaises(exceptions.DataException):
            self._testWithIndexPath(indexPath)

    @unittest.skip("Skipping until we can detect incorrect indexes")
    def testWrongIndexFile(self):
        indexPath = paths.bamIndexPath2  # incorrect index
        self._testWithIndexPath(indexPath)


class TestValidAddDataSetDuo(AbstractRepoManagerTest):
    """
    This class tests valid inputs for method "addDatasetDuo"
    on class "RepoManager"
    """

    def _addDatasetDuo(self, file_path):
        """
        This is a helper method that executes "add-dataset-duo"
        command and returns the updated dataset
        """
        self.runCommand(
            "add-dataset-duo {} {} {}".format(
                self._repoPath,
                self._datasetName,
                file_path))
        repo = self.readRepo()
        return repo.getDatasetByName(self._datasetName)

    def _removeDatasetDuo(self):
        """
        This is a helper method that executes "remove-dataset-duo"
        command and returns the updated dataset
        """
        self.runCommand(
            "remove-dataset-duo -f {} {}".format(
                self._repoPath,
                self._datasetName))
        repo = self.readRepo()
        return repo.getDatasetByName(self._datasetName)

    def setUp(self):
        """
        Sets up the class
        """
        super(TestValidAddDataSetDuo, self).setUp()
        self.init()
        self.addDataset()

    def testValidDuoDataset(self):
        """
        This is a valid input, as the "paths.testValidDuoJson" file
        contains valid json format and DUO info
        """
        dataset = self._addDatasetDuo(paths.testValidDuoJson)
        self.assertEqual(dataset._info[0]['id'], "DUO:0000018")
        self.assertEqual(dataset._info[1]['id'], "DUO:0000024")
        self.assertEqual(dataset._info[1]['modifier'], "2022-01-01")
        dataset = self._removeDatasetDuo()
        self.assertEqual(len(dataset._info), 0)


class TestInvalidAddDataSetDuo(AbstractRepoManagerTest):
    """
    This class tests invalid inputs for method "addDatasetDuo"
    on class "RepoManager"
    """

    def _addDatasetDuo(self, file_path):
        """
        This is a helper method that executes "add-dataset-duo"
        command and returns the updated dataset
        """
        self.runCommand(
            "add-dataset-duo {} {} {}".format(
                self._repoPath,
                self._datasetName,
                file_path))
        repo = self.readRepo()
        return repo.getDatasetByName(self._datasetName)

    def setUp(self):
        """
        Sets up the class
        """
        super(TestInvalidAddDataSetDuo, self).setUp()
        self.init()
        self.addDataset()

    def testInvalidDuoDataset(self):
        """
        This is an invalid input, as "paths.testInvalidDuoJson" file
        contains invalid DUO information
        """
        dataset = self._addDatasetDuo(paths.testInvalidDuoJson)
        with self.assertRaises(IndexError):
            dataset._info[0]['id']

    def testInvalidFileType(self):
        """
        This is an invalid input, as "paths.landingMessageHtml" file
        is not a valid json file
        """
        with self.assertRaises(exceptions.JsonFileOpenException):
            self._addDatasetDuo(paths.landingMessageHtml)

    def testDuoFileNotFound(self):
        """
        This is an invalid input, as "no_file.txt" file
        does not exist
        """
        with self.assertRaises(exceptions.JsonFileOpenException):
            self._addDatasetDuo("no_file.txt")


class TestValidAddRemovePeer(AbstractRepoManagerTest):
    """
    This class tests valid inputs for method "addPeer"
    on class "RepoManager"
    """
    def setUp(self):
        """
        Sets up the class
        """
        super(TestValidAddRemovePeer, self).setUp()
        self.init()
        self.addDataset()

    def _addPeer(self, peer_url):
        """
        This is a helper method that executes "add-peer"
        command and returns a list of peers
        """
        self.runCommand("add-peer {} {}".format(
            self._repoPath,
            peer_url
        ))
        repo = self.readRepo()
        return [x.getUrl() for x in repo.getPeers()]

    def _removePeer(self, peer_url):
        """
        This is a helper method that executes "add-peer"
        command and returns a list of peers
        """
        self.runCommand("remove-peer -f {} {}".format(
            self._repoPath,
            peer_url
        ))
        repo = self.readRepo()
        return [x.getUrl() for x in repo.getPeers()]

    def testAddPeer1(self):
        """
        This is valid input, as "peerUrl" is a valid
        peer
        """
        peers = self._addPeer(paths.peerUrl)
        self.assertIn(paths.peerUrl, peers)
        peers = self._removePeer(paths.peerUrl)
        self.assertNotIn(paths.peerUrl, peers)

    def testAddPeer2(self):
        """
        This is valid input, as "peerUrlNoTraillingPath" is a valid
        peer
        """
        peers = self._addPeer(paths.peerUrlNoTraillingPath)
        self.assertIn(paths.peerUrlNoTraillingPath + "/", peers)
        peers = self._removePeer(paths.peerUrl)
        self.assertNotIn(paths.peerUrlNoTraillingPath + "/", peers)


class TestInvalidAddRemovePeer(AbstractRepoManagerTest):
    """
    This class tests invalid inputs for method "addPeer"
    on class "RepoManager"
    """
    def setUp(self):
        """
        Sets up the class
        """
        super(TestInvalidAddRemovePeer, self).setUp()
        self.init()
        self.addDataset()

    def _addPeer(self, peer_url):
        """
        This is a helper method that executes "add-peer"
        command and returns a list of peers
        """
        self.runCommand("add-peer {} {}".format(
            self._repoPath,
            peer_url
        ))
        repo = self.readRepo()
        return [x.getUrl() for x in repo.getPeers()]

    def _removePeer(self, peer_url):
        """
        This is a helper method that executes "add-peer"
        command and returns a list of peers
        """
        self.runCommand("remove-peer -f {} {}".format(
            self._repoPath,
            peer_url
        ))
        repo = self.readRepo()
        return [x.getUrl() for x in repo.getPeers()]

    def testAddInvalidPeer1(self):
        """
        This is an invalid input, as "invalidPeerUrl" is not 
        a valid URL
        """
        with self.assertRaises(exceptions.RepoManagerException):
            self._addPeer(paths.invalidPeerUrl)

    def testAddInvalidPeer2(self):
        """
        This is an invalid input, as "emptyPeerUlr" is empty
        """
        with self.assertRaises(SystemExit):
            self._addPeer(paths.emptyPeerUlr)

    def testAddValidPeerTwice(self):
        """
        This input is invalid, as the same peer is added twice
        """
        with self.assertRaises(exceptions.RepoManagerException):
            self._addPeer(paths.peerUrl)
            self._addPeer(paths.peerUrl)

    def testRemoveInvalidPeer(self):
        """
        This input is invalid, as it is removing an invalid
        peer
        """
        self._addPeer(paths.peerUrl)
        with self.assertRaises(exceptions.PeerNotFoundException):
            self._removePeer(paths.invalidPeerUrl)

    def testRemoveEmptyPeer(self):
        """
        This input is invalid, as it is using an empty
        peer
        """
        with self.assertRaises(SystemExit):
            self._removePeer(paths.emptyPeerUlr)


class TestValidRemoveFromDataset(AbstractRepoManagerTest):
    """
    This class tests valid inputs for methods from class "Repomanager".
    The following methods are being tested here:
    - removePatient
    - removeEnrolment
    - removeSample
    - removeChemotherapy
    - removeImmunotherapy
    - removeTreatment
    - removeDiagnosis
    - removeTumourboard
    - removeOutcome
    - removeComplication
    - removeConsent
    - removeCellTransplant
    - removeSurgery
    - removeStudy
    - removeSlide
    - removeLabtest
    """
    def setUp(self):
        """
        Sets up the class
        """
        super(TestValidRemoveFromDataset, self).setUp()
        self.init()
        self.addDataset()        
        FNULL = open(os.devnull, 'w')
        subprocess.call(['ingest', self._repoPath, 'dataset1', 
                        paths.sampleClinMetadata], stdout=FNULL, 
                        stderr=subprocess.STDOUT)

        # When adding to this dictionary, please follow below schema:
        # {table_name: (id, exception class that is expected)}
        self.dataDict = {
            "patient": (
                "PATIENT_49845",
                exceptions.ClinicalLocalIdNotFoundException),
            "enrollment": (
                "PATIENT_49845_02/01/2005",
                exceptions.ClinicalLocalIdNotFoundException),
            "sample": (
                "PATIENT_49845_SAMPLE_58628", 
                exceptions.SampleNotFoundException),
            "chemotherapy": (
                "PATIENT_49845_PATIENT_49845_44159_LEUCOVORIN",
                exceptions.ChemotherapyNotFoundException),
            "immunotherapy": (
                "PATIENT_49845_PATIENT_49845_44159_2014-09-22",
                exceptions.ImmunotherapyNotFoundException),
            "treatment": (
                "PATIENT_49845_06/25/2004",
                exceptions.TreatmentNotFoundException),
            "diagnosis": (
                "PATIENT_49845_11/08/2008",
                exceptions.DiagnosisNotFoundException),
            "tumourboard": (
                "PATIENT_49845_07/09/2014",
                exceptions.TumourboardNotFoundException),
            "outcome": (
                "PATIENT_49845_08/22/2012",
                exceptions.OutcomeNotFoundException),
            "complication": (
                "PATIENT_49845_10/18/2006",
                exceptions.ComplicationNotFoundException),
            "consent": (
                "PATIENT_49845_03/06/2007", 
                exceptions.ConsentNotFoundException),
            "celltransplant": (
                "PATIENT_49845_PATIENT_49845_44159_2016-01-02",
                exceptions.CelltransplantNotFoundException),
            "surgery": (
                "PATIENT_49845_PATIENT_49845_44159_2016-06-15_SAMPLE_58628",
                exceptions.SurgeryNotFoundException),
            "study": (
                "PATIENT_49845_2014-04-17",
                exceptions.StudyNotFoundException),
            "slide": (
                "PATIENT_49845_48236",
                exceptions.SlideNotFoundException),
            "labtest": (
                "PATIENT_49845_2016-07-20",
                exceptions.LabtestNotFoundException),
        }

    def _getDataset(self):
        """
        This is a helper method that returns the updated dataset
        """
        return self.readRepo().getDatasetByName("dataset1")

    def _executeRemoveCommand(self, table, value):
        """
        This is a helper method that executes a "remove" command and 
        returns updated dataset.
        Args:
            table: Table you want to run "remove" command
            value: Value you want to delete from table
        """
        self.runCommand("remove-{} -f {} dataset1 {}".format(
            table, 
            self._repoPath,
            value
        ))
        return self._getDataset()

    def _removeDataFromTable(self, table, value, exception_):
        """
        This helper method verifies if "value" is being removed
        from "table". Please note, This method will fail if "value"
        is not present in "table" before running "remove" comand.
        """
        capital_table = table.title()
        
        try:
            getattr(self._getDataset(), 
                    "get{}ByName".format(capital_table))(value)
        except exception_:
            self.fail("{} name {} should be present in dataset. "
                      "Aborting test!".format(capital_table, value))        
        with self.assertRaises(exception_):            
            getattr(self._executeRemoveCommand(table, value), 
                    "get{}ByName".format(capital_table))(value)

    def testRemoveMethods(self):
        """
        This method loops throught "dataDict" dict and test each of them.
        When there is a new "remove" method to be tested and there 
        is a method that follows the format "get{}ByName", the data
        must be added to "dataDict" dictionary
        """
        for table, tuple_ in self.dataDict.items():
            self._removeDataFromTable(table, *tuple_)
           

class TestInvalidRemoveFromDataset(AbstractRepoManagerTest):
    """
    This class tests invalid inputs for methods from class "Repomanager".
    The following methods are being tested here:
    - removePatient
    - removeEnrolment
    - removeSample
    - removeChemotherapy
    - removeImmunotherapy
    - removeTreatment
    - removeDiagnosis
    - removeTumourboard
    - removeOutcome
    - removeComplication
    - removeConsent
    - removeCellTransplant
    - removeSurgery
    - removeStudy
    - removeSlide
    - removeLabtest
    """
    def setUp(self):
        """
        Sets up the class
        """
        super(TestInvalidRemoveFromDataset, self).setUp()
        self.init()
        self.addDataset()

        FNULL = open(os.devnull, 'w')
        subprocess.call(['ingest', self._repoPath, 'dataset1', 
                        paths.sampleClinMetadata], 
                        stdout=FNULL, stderr=subprocess.STDOUT)
        # When adding to this dictionary, please follow below schema:
        # {table_name: ([invalid values], exception class that is expected)}
        self.invalidDataDict = {
            "patient": (
                ["INVALID_PATIENT", ""], 
                exceptions.ClinicalLocalIdNotFoundException),
            "enrollment": (
                ["INVALID_ENROLLMENT", ""],
                exceptions.ClinicalLocalIdNotFoundException),
            "sample": (
                ["INVALID_SAMPLE", ""],
                exceptions.SampleNotFoundException),
            "chemotherapy": (
                ["INVALID_CHEMO", ""],
                exceptions.ChemotherapyNotFoundException),
            "immunotherapy": (
                ["INVALID_IMMUN", ""],
                exceptions.ImmunotherapyNotFoundException),
            "treatment": (
                ["INVALID_TREATMENT", ""],
                exceptions.TreatmentNotFoundException),
            "diagnosis": (
                ["INVALID_DIAGNOSIS", ""],
                exceptions.DiagnosisNotFoundException),
            "tumourboard": (
                ["INVALID_TUMOURBOARD", ""],
                exceptions.TumourboardNotFoundException),
            "outcome": (
                ["INVALID_OUTCOME", ""],
                exceptions.OutcomeNotFoundException),
            "complication": (
                ["INVALID_COMPLICATION", ""],
                exceptions.ComplicationNotFoundException),
            "consent": (
                ["INVALID_CONSENT", ""],
                exceptions.ConsentNotFoundException),
            "celltransplant": (
                ["INVALID_CELLTRANSPLANT", ""],
                exceptions.CelltransplantNotFoundException),
            "surgery": (
                ["INVALID_SURGERY", ""],
                exceptions.SurgeryNotFoundException),
            "study": (
                ["INVALID_STUDY", ""],
                exceptions.StudyNotFoundException),
            "slide": (
                ["INVALID_SLIDE", ""],
                exceptions.SlideNotFoundException),
            "labtest": (
                ["INVALID_LABTEST", ""],
                exceptions.LabtestNotFoundException),
        }

    def _getDataset(self):
        """
        This is a helper method that returns the updated dataset
        """
        return self.readRepo().getDatasetByName("dataset1")

    def _executeRemoveCommand(self, table, value):
        """
        This is a helper method that executes a "remove" command and 
        return updated dataset.
        Args:
            table: Table you want to run "remove" command
            value: Value you want to delete from table
        """
        self.runCommand("remove-{} -f {} dataset1 {}".format(
            table, 
            self._repoPath,
            value
        ))
        return self._getDataset()

    def testRemoveInvalidData(self):
        """
        This method loops through "invalidDataDict" dict and test 
        each of them.
        When there is a new "remove" method to be tested and there 
        is a method that follows the format "get{}ByName", the data
        must be added to "invalidDataDict" dictionary following the format
        """
        for table, data in self.invalidDataDict.items():
            invalid_data, exception_ = data
            for value in invalid_data:
                with self.assertRaises((SystemExit, exception_)):
                    self._executeRemoveCommand(table, value)