"""
Tests the cli
"""

import unittest
import shlex

import candig.server.cli.server as cli_server
import candig.server.cli.repomanager as cli_repomanager

import candig.schemas.protocol as protocol


class TestServerArguments(unittest.TestCase):
    """
    Tests that the server can parse expected arguments
    """
    def testParseArguments(self):
        cliInput = """--port 7777 --host 123.4.5.6 --config MockConfigName
        --config-file /path/to/config --tls --dont-use-reloader"""
        parser = cli_server.getServerParser()
        args = parser.parse_args(cliInput.split())
        self.assertEqual(args.port, 7777)
        self.assertEqual(args.host, "123.4.5.6")
        self.assertEqual(args.config, "MockConfigName")
        self.assertEqual(args.config_file, "/path/to/config")
        self.assertTrue(args.tls)
        self.assertTrue(args.dont_use_reloader)


class TestRepoManagerCli(unittest.TestCase):

    def setUp(self):
        self.parser = cli_repomanager.RepoManager.getParser()
        self.registryPath = 'a/repo/path'
        self.datasetName = "datasetName"
        self.filePath = 'a/file/path'
        self.dirPath = 'a/dir/path/'
        self.individualName = "test"
        self.biosampleName = "test"
        self.individual = protocol.toJson(
            protocol.Individual(
                name="test",
                created="2016-05-19T21:00:19Z",
                updated="2016-05-19T21:00:19Z"))
        self.biosample = protocol.toJson(
            protocol.Biosample(
                name="test",
                created="2016-05-19T21:00:19Z",
                updated="2016-05-19T21:00:19Z"))

    def testInit(self):
        cliInput = "init {}".format(self.registryPath)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.runner, "init")

    def testVerify(self):
        cliInput = "verify {}".format(self.registryPath)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.runner, "verify")

    def testList(self):
        cliInput = "list {}".format(self.registryPath)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.runner, "list")

    def testAddDataset(self):
        cliInput = "add-dataset {} {}".format(
            self.registryPath, self.datasetName)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.runner, "addDataset")

    def testRemoveDataset(self):
        cliInput = "remove-dataset {} {} -f".format(
            self.registryPath, self.datasetName)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.runner, "removeDataset")
        self.assertEqual(args.force, True)

    def testAddReferenceSet(self):
        description = "description"
        cliInput = (
            "add-referenceset {} {} --description={} "
            "--species NCBITAXONID-JSON "
            "--isDerived True "
            "--assemblyId ASSEMBLYID "
            "--sourceAccessions SOURCEACCESSIONS "
            "--sourceUri SOURCEURI ").format(
            self.registryPath, self.filePath, description)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.filePath, self.filePath)
        self.assertEqual(args.description, description)
        self.assertEqual(args.species, "NCBITAXONID-JSON")
        self.assertEqual(args.isDerived, True)
        self.assertEqual(args.assemblyId, "ASSEMBLYID")
        self.assertEqual(args.sourceAccessions, "SOURCEACCESSIONS")
        self.assertEqual(args.sourceUri, "SOURCEURI")
        self.assertEqual(args.runner, "addReferenceSet")

    def testRemoveReferenceSet(self):
        referenceSetName = "referenceSetName"
        cliInput = "remove-referenceset {} {} -f".format(
            self.registryPath, referenceSetName)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.referenceSetName, referenceSetName)
        self.assertEqual(args.runner, "removeReferenceSet")
        self.assertEqual(args.force, True)

    def testAddReadGroupSet(self):
        cliInput = "add-readgroupset {} {} patient1 sample1 {} ".format(
            self.registryPath, self.datasetName, self.filePath)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.dataFile, self.filePath)
        self.assertEqual(args.indexFile, None)
        self.assertEqual(args.runner, "addReadGroupSet")

    def testAddReadGroupSetWithIndexFile(self):
        indexPath = self.filePath + ".bai"
        cliInput = "add-readgroupset {} {} patient1 sample1 {} -I {}".format(
            self.registryPath, self.datasetName, self.filePath,
            indexPath)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.dataFile, self.filePath)
        self.assertEqual(args.indexFile, indexPath)
        self.assertEqual(args.runner, "addReadGroupSet")

    def testRemoveReadGroupSet(self):
        readGroupSetName = "readGroupSetName"
        cliInput = "remove-readgroupset {} {} {} -f".format(
            self.registryPath, self.datasetName, readGroupSetName)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.readGroupSetName, readGroupSetName)
        self.assertEqual(args.runner, "removeReadGroupSet")
        self.assertEqual(args.force, True)

    def testAddVariantSet(self):
        cliInput = "add-variantset {} {} patient1 sample1 {} ".format(
            self.registryPath, self.datasetName, self.filePath)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.dataFiles, [self.filePath])
        self.assertEqual(args.indexFiles, None)
        self.assertEqual(args.runner, "addVariantSet")

    def testAddVariantSetWithIndexFiles(self):
        file1 = "file1"
        file2 = "file2"
        indexFile1 = file1 + ".tbi"
        indexFile2 = file2 + ".tbi"
        cliInput = "add-variantset {} {} patient1 sample1 {} {} -I {} {}".format(
            self.registryPath, self.datasetName, file1, file2,
            indexFile1, indexFile2)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.dataFiles, [file1, file2])
        self.assertEqual(args.indexFiles, [indexFile1, indexFile2])
        self.assertEqual(args.runner, "addVariantSet")

    def testRemoveVariantSet(self):
        variantSetName = "variantSetName"
        cliInput = "remove-variantset {} {} {}".format(
            self.registryPath, self.datasetName, variantSetName)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.variantSetName, variantSetName)
        self.assertEqual(args.runner, "removeVariantSet")
        self.assertEqual(args.force, False)

    def testAddOntology(self):
        cliInput = "add-ontology {} {}".format(
            self.registryPath, self.filePath)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.filePath, self.filePath)
        self.assertEqual(args.runner, "addOntology")

    def testRemoveOntology(self):
        ontologyName = "the_ontology_name"
        cliInput = "remove-ontology {} {}".format(
            self.registryPath, ontologyName)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.ontologyName, ontologyName)
        self.assertEqual(args.runner, "removeOntology")
        self.assertEqual(args.force, False)

    def testAddBiosample(self):
        cliInput = "add-biosample {} {} {} '{}'".format(
            self.registryPath,
            self.datasetName,
            self.biosampleName,
            self.biosample)
        args = self.parser.parse_args(shlex.split(cliInput))
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.biosampleName, self.biosampleName)
        self.assertEqual(args.biosample, self.biosample)
        self.assertEqual(args.runner, "addBiosample")

    def testRemoveBiosample(self):
        cliInput = "remove-biosample {} {} {}".format(
            self.registryPath,
            self.datasetName,
            self.biosampleName)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.biosampleName, self.biosampleName)
        self.assertEqual(args.runner, "removeBiosample")
        self.assertEqual(args.force, False)

    def testAddIndividual(self):
        cliInput = "add-individual {} {} {} '{}'".format(
            self.registryPath,
            self.datasetName,
            self.individualName,
            self.individual)
        args = self.parser.parse_args(shlex.split(cliInput))
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.individualName, self.individualName)
        self.assertEqual(args.individual, self.individual)
        self.assertEqual(args.runner, "addIndividual")

    def testRemoveIndividual(self):
        cliInput = "remove-individual {} {} {}".format(
            self.registryPath,
            self.datasetName,
            self.individualName)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.individualName, self.individualName)
        self.assertEqual(args.runner, "removeIndividual")
        self.assertEqual(args.force, False)

    def testAddPhenotypeAssociationSet(self):
        cliInput = "add-phenotypeassociationset {} {} {} -n NAME".format(
            self.registryPath,
            self.datasetName,
            self.dirPath)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.dirPath, self.dirPath)
        self.assertEqual(args.name, "NAME")

    def testRemovePhenotypeAssociationSet(self):
        cliInput = "remove-phenotypeassociationset {} {} NAME".format(
            self.registryPath, self.datasetName)
        args = self.parser.parse_args(cliInput.split())
        self.assertEqual(args.registryPath, self.registryPath)
        self.assertEqual(args.datasetName, self.datasetName)
        self.assertEqual(args.name, "NAME")
