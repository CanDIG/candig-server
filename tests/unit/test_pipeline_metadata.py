"""
Tests the pipeline meta data models
"""

import unittest

import candig.server.datamodel.datasets as datasets
import candig.server.exceptions as exceptions
import candig.server.datamodel.pipeline_metadata as pipeMetadata

import candig.schemas.protocol as protocol


class TestExtractions(unittest.TestCase):
    """
    Test the Extraction class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validExtraction = protocol.Extraction(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            extractionId="EXTRACTION_TEST",
            extractionIdTier=0,
            sampleId="n/a",
            sampleIdTier=0,
            rnaBlood="n/a",
            rnaBloodTier=0,
            dnaBlood="n/a",
            dnaBloodTier=0,
            rnaTissue="n/a",
            rnaTissueTier=0,
            dnaTissue="n/a",
            dnaTissueTier=0,
            site="Vancouver",
            siteTier=0
        )

        validExtraction.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        extraction = pipeMetadata.Extraction(
            dataset, "test")
        extraction.populateFromJson(protocol.toJson(validExtraction))
        gaExtraction = extraction.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaExtraction.created, validExtraction.created)
        self.assertEqual(gaExtraction.updated, validExtraction.updated)
        self.assertEqual(gaExtraction.extractionId, validExtraction.extractionId)
        self.assertEqual(gaExtraction.sampleId, validExtraction.sampleId)
        self.assertEqual(gaExtraction.site, validExtraction.site)
        self.assertEqual(gaExtraction.sampleIdTier, validExtraction.sampleIdTier)

        # Invalid input
        invalidExtraction = '{"bad:", "json"}'
        extraction = pipeMetadata.Extraction(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            extraction.populateFromJson,
            invalidExtraction)


class TestSequencing(unittest.TestCase):
    """
    Test the Sequencing class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validSequencing = protocol.Sequencing(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            sequencingId = "Sequencing_TEST",
            sequencingIdTier = 0,
            sampleId = "Sample_test",
            sampleIdTier = 0,
            dnaLibraryKit = "n/a",
            dnaLibraryKitTier = 0,
            dnaSeqPlatform = "n/a",
            dnaSeqPlatformTier = 0,
            dnaReadLength = "n/a",
            dnaReadLengthTier = 0,
            rnaLibraryKit = "n/a",
            rnaLibraryKitTier = 0,
            rnaSeqPlatform = "n/a",
            rnaSeqPlatformTier = 0,
            rnaReadLength = "n/a",
            rnaReadLengthTier = 0,
            pcrCycles = "n/a",
            pcrCyclesTier = 0,
            extractionId = "n/a",
            extractionIdTier = 0,
            site = "Toronto",
            siteTier = 0
        )

        validSequencing.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        sequencing = pipeMetadata.Sequencing(
            dataset, "test")
        sequencing.populateFromJson(protocol.toJson(validSequencing))
        gaSequencing = sequencing.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaSequencing.created, validSequencing.created)
        self.assertEqual(gaSequencing.updated, validSequencing.updated)
        self.assertEqual(gaSequencing.sequencingId, validSequencing.sequencingId)
        self.assertEqual(gaSequencing.sampleId, validSequencing.sampleId)
        self.assertEqual(gaSequencing.site, validSequencing.site)
        self.assertEqual(gaSequencing.sampleIdTier, validSequencing.sampleIdTier)

        # Invalid input
        invalidSequencing = '{"bad:", "json"}'
        sequencing = pipeMetadata.Sequencing(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            sequencing.populateFromJson,
            invalidSequencing)


class TestAlignment(unittest.TestCase):
    """
    Test the Alignment class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validAlignment = protocol.Alignment(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            alignmentId = "ALIGNMENT_TEST",
            alignmentIdTier = 0,
            sampleId = "n/a",
            sampleIdTier = 0,
            inHousePipeline = "n/a",
            inHousePipelineTier = 0,
            alignmentTool = "n/a",
            alignmentToolTier = 0,
            mergeTool = "n/a",
            mergeToolTier = 0,
            markDuplicates = "n/a",
            markDuplicatesTier = 0,
            realignerTarget = "n/a",
            realignerTargetTier = 0,
            indelRealigner = "n/a",
            indelRealignerTier = 0,
            baseRecalibrator = "n/a",
            baseRecalibratorTier = 0,
            printReads = "n/a",
            printReadsTier = 0,
            idxStats = "n/a",
            idxStatsTier = 0,
            flagStat = "n/a",
            flagStatTier = 0,
            coverage = "n/a",
            coverageTier = 0,
            insertSizeMetrics = "n/a",
            insertSizeMetricsTier = 0,
            fastqc = "n/a",
            fastqcTier = 0,
            reference = "n/a",
            referenceTier = 0,
            sequencingId = "n/a",
            sequencingIdTier = 0,
            site = "Montreal",
            siteTier = 0
        )

        validAlignment.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        alignment = pipeMetadata.Alignment(
            dataset, "test")
        alignment.populateFromJson(protocol.toJson(validAlignment))
        gaAlignment = alignment.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaAlignment.created, validAlignment.created)
        self.assertEqual(gaAlignment.updated, validAlignment.updated)
        self.assertEqual(gaAlignment.alignmentId, validAlignment.alignmentId)
        self.assertEqual(gaAlignment.sampleId, validAlignment.sampleId)
        self.assertEqual(gaAlignment.site, validAlignment.site)
        self.assertEqual(gaAlignment.mergeToolTier, validAlignment.mergeToolTier)

        # Invalid input
        invalidAlignment = '{"bad:", "json"}'
        alignment = pipeMetadata.Alignment(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            alignment.populateFromJson,
            invalidAlignment)


class TestVariantCalling(unittest.TestCase):
    """
    Test the VariantCalling class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validVariantCalling = protocol.VariantCalling(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            variantCallingId = "VC_TEST",
            variantCallingIdTier = 0,
            sampleId = "n/a",
            sampleIdTier = 0,
            inHousePipeline = "n/a",
            inHousePipelineTier = 0,
            tabulate = "n/a",
            tabulateTier = 0,
            annotation = "n/a",
            annotationTier = 0,
            mergeTool = "n/a",
            mergeToolTier = 0,
            rdaToTab = "n/a",
            rdaToTabTier = 0,
            delly = "n/a",
            dellyTier = 0,
            postFilter = "n/a",
            postFilterTier = 0,
            clipFilter = "n/a",
            clipFilterTier = 0,
            cosmic = "n/a",
            cosmicTier = 0,
            dbSnp = "n/a",
            dbSnpTier = 0,
            alignmentId = "n/a",
            alignmentIdTier = 0,
            site = "Vancouver",
            siteTier = 0,
        )

        validVariantCalling.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        variantCalling = pipeMetadata.VariantCalling(
            dataset, "test")
        variantCalling.populateFromJson(protocol.toJson(validVariantCalling))
        gaVariantCalling = variantCalling.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaVariantCalling.created, validVariantCalling.created)
        self.assertEqual(gaVariantCalling.updated, validVariantCalling.updated)
        self.assertEqual(gaVariantCalling.variantCallingId, validVariantCalling.variantCallingId)
        self.assertEqual(gaVariantCalling.sampleId, validVariantCalling.sampleId)
        self.assertEqual(gaVariantCalling.site, validVariantCalling.site)
        self.assertEqual(gaVariantCalling.postFilterTier, validVariantCalling.postFilterTier)

        # Invalid input
        invalidVariantCalling = '{"bad:", "json"}'
        variantCalling = pipeMetadata.VariantCalling(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            variantCalling.populateFromJson,
            invalidVariantCalling)


class TestFusionDetection(unittest.TestCase):
    """
    Test the FusionDetection class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validFusionDetection = protocol.FusionDetection(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            fusionDetectionId = "n/a",
            fusionDetectionIdTier = 0,
            sampleId = "n/a",
            sampleIdTier = 0,
            inHousePipeline = "n/a",
            inHousePipelineTier = 0,
            svDetection = "n/a",
            svDetectionTier = 0,
            fusionDetection = "n/a",
            fusionDetectionTier = 0,
            realignment = "n/a",
            realignmentTier = 0,
            annotation = "n/a",
            annotationTier = 0,
            genomeReference = "n/a",
            genomeReferenceTier = 0,
            geneModels = "n/a",
            geneModelsTier = 0,
            alignmentId = "n/a",
            alignmentIdTier = 0,
            site = "n/a",
            siteTier = 0
        )

        validFusionDetection.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        fusionDetection = pipeMetadata.FusionDetection(
            dataset, "test")
        fusionDetection.populateFromJson(protocol.toJson(validFusionDetection))
        gaFusionDetection = fusionDetection.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaFusionDetection.created, validFusionDetection.created)
        self.assertEqual(gaFusionDetection.updated, validFusionDetection.updated)
        self.assertEqual(gaFusionDetection.fusionDetectionId, validFusionDetection.fusionDetectionId)
        self.assertEqual(gaFusionDetection.sampleId, validFusionDetection.sampleId)
        self.assertEqual(gaFusionDetection.site, validFusionDetection.site)
        self.assertEqual(gaFusionDetection.fusionDetectionTier, validFusionDetection.fusionDetectionTier)

        # Invalid input
        invalidFusionDetection = '{"bad:", "json"}'
        fusionDetection = pipeMetadata.FusionDetection(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            fusionDetection.populateFromJson,
            invalidFusionDetection)


class TestExpressionAnalysis(unittest.TestCase):
    """
    Test the ExpressionAnalysis class
    """
    def testToProtocolElement(self):
        dataset = datasets.Dataset('dataset1')
        validExpressionAnalysis = protocol.ExpressionAnalysis(
            name="test",
            created="2016-05-19T21:00:19Z",
            updated="2016-05-19T21:00:19Z",
            expressionAnalysisId = "n/a",
            expressionAnalysisIdTier = 0,
            sampleId = "n/a",
            sampleIdTier = 0,
            readLength = "n/a",
            readLengthTier = 0,
            reference = "n/a",
            referenceTier = 0,
            alignmentTool = "n/a",
            alignmentToolTier = 0,
            bamHandling = "n/a",
            bamHandlingTier = 0,
            expressionEstimation = "n/a",
            expressionEstimationTier = 0,
            sequencingId = "n/a",
            sequencingIdTier = 0,
            site = "n/a",
            siteTier = 0
        )

        validExpressionAnalysis.attributes.attr['test']. \
            values.add().string_value = 'test-info'

        # pass through protocol creation
        expressionAnalysis = pipeMetadata.ExpressionAnalysis(
            dataset, "test")
        expressionAnalysis.populateFromJson(protocol.toJson(validExpressionAnalysis))
        gaExpressionAnalysis = expressionAnalysis.toProtocolElement()
        # Verify select elements exist
        self.assertEqual(gaExpressionAnalysis.created, validExpressionAnalysis.created)
        self.assertEqual(gaExpressionAnalysis.updated, validExpressionAnalysis.updated)
        self.assertEqual(gaExpressionAnalysis.expressionAnalysisId, validExpressionAnalysis.expressionAnalysisId)
        self.assertEqual(gaExpressionAnalysis.sampleId, validExpressionAnalysis.sampleId)
        self.assertEqual(gaExpressionAnalysis.site, validExpressionAnalysis.site)
        self.assertEqual(gaExpressionAnalysis.bamHandlingTier, validExpressionAnalysis.bamHandlingTier)

        # Invalid input
        invalidExpressionAnalysis = '{"bad:", "json"}'
        expressionAnalysis = pipeMetadata.ExpressionAnalysis(dataset, "test")
        # Should fail
        self.assertRaises(
            exceptions.InvalidJsonException,
            expressionAnalysis.populateFromJson,
            invalidExpressionAnalysis)