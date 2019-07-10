"""
CanDIG - 2018-08-07

Pipeline metadata objects

"""

import datetime

import candig.server.datamodel as datamodel
import candig.server.exceptions as exceptions

import candig.schemas.protocol as protocol


class Extraction(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.ExtractionCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Extraction, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._extractionId = None
        self._extractionIdTier = None
        self._sampleId = None
        self._sampleIdTier = None
        self._rnaBlood = None
        self._rnaBloodTier = None
        self._dnaBlood = None
        self._dnaBloodTier = None
        self._rnaTissue = None
        self._rnaTissueTier = None
        self._dnaTissue = None
        self._dnaTissueTier = None
        self._site = None
        self._siteTier = None

        self._objectAttr = {
            "extractionId": self.getExtractionId,
            "sampleId": self.getSampleId,
            "rnaBlood": self.getRnaBlood,
            "dnaBlood": self.getDnaBlood,
            "rnaTissue": self.getRnaTissue,
            "dnaTissue": self.getDnaTissue,
            "site": self.getSite
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getExtractionIdTier():
                record['extractionId'] = self.getExtractionId()
            if tier >= self.getSampleIdTier():
                record['sampleId'] = self.getSampleId()
            if tier >= self.getRnaBloodTier():
                record['rnaBlood'] = self.getRnaBlood()
            if tier >= self.getDnaBloodTier():
                record['dnaBlood'] = self.getDnaBlood()
            if tier >= self.getRnaTissueTier():
                record['rnaTissue'] = self.getRnaTissue()
            if tier >= self.getDnaTissueTier():
                record['dnaTissue'] = self.getDnaTissue()
            if tier >= self.getSiteTier():
                record['site'] = self.getSite()
        except TypeError:
            pass

        Extraction = protocol.Extraction(**record)
        self.serializeMetadataAttributes(Extraction)

        return Extraction

    def populateFromRow(self, ExtractionRecord):
        """
        """
        self._created = ExtractionRecord.created
        self._updated = ExtractionRecord.updated
        self._name = ExtractionRecord.name
        self._description = ExtractionRecord.description
        self.setAttributesJson(ExtractionRecord.attributes)

        # Unique fields
        self._extractionId = ExtractionRecord.extractionId
        self._extractionIdTier = ExtractionRecord.extractionIdTier
        self._sampleId = ExtractionRecord.sampleId
        self._sampleIdTier = ExtractionRecord.sampleIdTier
        self._rnaBlood = ExtractionRecord.rnaBlood
        self._rnaBloodTier = ExtractionRecord.rnaBloodTier
        self._dnaBlood = ExtractionRecord.dnaBlood
        self._dnaBloodTier = ExtractionRecord.dnaBloodTier
        self._rnaTissue = ExtractionRecord.rnaTissue
        self._rnaTissueTier = ExtractionRecord.rnaTissueTier
        self._dnaTissue = ExtractionRecord.dnaTissue
        self._dnaTissueTier = ExtractionRecord.dnaTissueTier
        self._site = ExtractionRecord.site
        self._siteTier = ExtractionRecord.siteTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Extraction)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._extractionId = parsed.extractionId
        self._extractionIdTier = parsed.extractionIdTier
        self._sampleId = parsed.sampleId
        self._sampleIdTier = parsed.sampleIdTier
        self._rnaBlood = parsed.rnaBlood
        self._rnaBloodTier = parsed.rnaBloodTier
        self._dnaBlood = parsed.dnaBlood
        self._dnaBloodTier = parsed.dnaBloodTier
        self._rnaTissue = parsed.rnaTissue
        self._rnaTissueTier = parsed.rnaTissueTier
        self._dnaTissue = parsed.dnaTissue
        self._dnaTissueTier = parsed.dnaTissueTier
        self._site = parsed.site
        self._siteTier = parsed.siteTier

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def getExtractionId(self):
        return self._extractionId

    def getExtractionIdTier(self):
        return self._extractionIdTier

    def getSampleId(self):
        return self._sampleId

    def getSampleIdTier(self):
        return self._sampleIdTier

    def getRnaBlood(self):
        return self._rnaBlood

    def getRnaBloodTier(self):
        return self._rnaBloodTier

    def getDnaBlood(self):
        return self._dnaBlood

    def getDnaBloodTier(self):
        return self._dnaBloodTier

    def getRnaTissue(self):
        return self._rnaTissue

    def getRnaTissueTier(self):
        return self._rnaTissueTier

    def getDnaTissue(self):
        return self._dnaTissue

    def getDnaTissueTier(self):
        return self._dnaTissueTier

    def getSite(self):
        return self._site

    def getSiteTier(self):
        return self._siteTier


class Sequencing(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.SequencingCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Sequencing, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._sequencingId = None
        self._sequencingIdTier = None
        self._sampleId = None
        self._sampleIdTier = None
        self._dnaLibraryKit = None
        self._dnaLibraryKitTier = None
        self._dnaSeqPlatform = None
        self._dnaSeqPlatformTier = None
        self._dnaReadLength = None
        self._dnaReadLengthTier = None
        self._rnaLibraryKit = None
        self._rnaLibraryKitTier = None
        self._rnaSeqPlatform = None
        self._rnaSeqPlatformTier = None
        self._rnaReadLength = None
        self._rnaReadLengthTier = None
        self._pcrCycles = None
        self._pcrCyclesTier = None
        self._extractionId = None
        self._extractionIdTier = None
        self._site = None
        self._siteTier = None

        self._objectAttr = {
            "sequencingId": self.getSequencingId(),
            "sampleId": self.getSampleId,
            "dnaLibraryKit": self.getDnaLibraryKit,
            "dnaSeqPlatform": self.getDnaSeqPlatform,
            "dnaReadLength": self.getDnaReadLength,
            "rnaLibraryKit": self.getRnaLibraryKit,
            "rnaSeqPlatform": self.getRnaSeqPlatform,
            "rnaReadLength": self.getRnaReadLength,
            "pcrCycles": self.getPcrCycles,
            "extractionId": self.getExtractionId,
            "site": self.getSite
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getSequencingIdTier():
                record['sequencingId'] = self.getSequencingId()
            if tier >= self.getSampleIdTier():
                record['sampleId'] = self.getSampleId()
            if tier >= self.getDnaLibraryKitTier():
                record['dnaLibraryKit'] = self.getDnaLibraryKit()
            if tier >= self.getDnaSeqPlatformTier():
                record['dnaSeqPlatform'] = self.getDnaSeqPlatform()
            if tier >= self.getDnaReadLengthTier():
                record['dnaReadLength'] = self.getDnaReadLength()
            if tier >= self.getRnaLibraryKitTier():
                record['rnaLibraryKit'] = self.getRnaLibraryKit()
            if tier >= self.getRnaSeqPlatformTier():
                record['rnaSeqPlatform'] = self.getRnaSeqPlatform()
            if tier >= self.getRnaReadLengthTier():
                record['rnaReadLength'] = self.getRnaReadLength()
            if tier >= self.getPcrCyclesTier():
                record['pcrCycles'] = self.getPcrCycles()
            if tier >= self.getExtractionIdTier():
                record['extractionId'] = self.getExtractionId()
            if tier >= self.getSiteTier():
                record['site'] = self.getSite()
        except TypeError:
            pass

        Sequencing = protocol.Sequencing(**record)
        self.serializeMetadataAttributes(Sequencing)

        return Sequencing

    def populateFromRow(self, SequencingRecord):
        """
        """
        self._created = SequencingRecord.created
        self._updated = SequencingRecord.updated
        self._name = SequencingRecord.name
        self._description = SequencingRecord.description
        self.setAttributesJson(SequencingRecord.attributes)

        # Unique fields
        self._sequencingId = SequencingRecord.sequencingId
        self._sequencingIdTier = SequencingRecord.sequencingIdTier
        self._sampleId = SequencingRecord.sampleId
        self._sampleIdTier = SequencingRecord.sampleIdTier
        self._dnaLibraryKit = SequencingRecord.dnaLibraryKit
        self._dnaLibraryKitTier = SequencingRecord.dnaLibraryKitTier
        self._dnaSeqPlatform = SequencingRecord.dnaSeqPlatform
        self._dnaSeqPlatformTier = SequencingRecord.dnaSeqPlatformTier
        self._dnaReadLength = SequencingRecord.dnaReadLength
        self._dnaReadLengthTier = SequencingRecord.dnaReadLengthTier
        self._rnaLibraryKit = SequencingRecord.rnaLibraryKit
        self._rnaLibraryKitTier = SequencingRecord.rnaLibraryKitTier
        self._rnaSeqPlatform = SequencingRecord.rnaSeqPlatform
        self._rnaSeqPlatformTier = SequencingRecord.rnaSeqPlatformTier
        self._rnaReadLength = SequencingRecord.rnaReadLength
        self._rnaReadLengthTier = SequencingRecord.rnaReadLengthTier
        self._pcrCycles = SequencingRecord.pcrCycles
        self._pcrCyclesTier = SequencingRecord.pcrCyclesTier
        self._extractionId = SequencingRecord.extractionId
        self._extractionIdTier = SequencingRecord.extractionIdTier
        self._site = SequencingRecord.site
        self._siteTier = SequencingRecord.siteTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Sequencing)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._sequencingId = parsed.sequencingId
        self._sequencingIdTier = parsed.sequencingIdTier
        self._sampleId = parsed.sampleId
        self._sampleIdTier = parsed.sampleIdTier
        self._dnaLibraryKit = parsed.dnaLibraryKit
        self._dnaLibraryKitTier = parsed.dnaLibraryKitTier
        self._dnaSeqPlatform = parsed.dnaSeqPlatform
        self._dnaSeqPlatformTier = parsed.dnaSeqPlatformTier
        self._dnaReadLength = parsed.dnaReadLength
        self._dnaReadLengthTier = parsed.dnaReadLengthTier
        self._rnaLibraryKit = parsed.rnaLibraryKit
        self._rnaLibraryKitTier = parsed.rnaLibraryKitTier
        self._rnaSeqPlatform = parsed.rnaSeqPlatform
        self._rnaSeqPlatformTier = parsed.rnaSeqPlatformTier
        self._rnaReadLength = parsed.rnaReadLength
        self._rnaReadLengthTier = parsed.rnaReadLengthTier
        self._pcrCycles = parsed.pcrCycles
        self._pcrCyclesTier = parsed.pcrCyclesTier
        self._extractionId = parsed.extractionId
        self._extractionIdTier = parsed.extractionIdTier
        self._site = parsed.site
        self._siteTier = parsed.siteTier

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def getSequencingId(self):
        return self._sequencingId

    def getSequencingIdTier(self):
        return self._sequencingIdTier

    def getSampleId(self):
        return self._sampleId

    def getSampleIdTier(self):
        return self._sampleIdTier

    def getDnaLibraryKit(self):
        return self._dnaLibraryKit

    def getDnaLibraryKitTier(self):
        return self._dnaLibraryKitTier

    def getDnaSeqPlatform(self):
        return self._dnaSeqPlatform

    def getDnaSeqPlatformTier(self):
        return self._dnaSeqPlatformTier

    def getDnaReadLength(self):
        return self._dnaReadLength

    def getDnaReadLengthTier(self):
        return self._dnaReadLengthTier

    def getRnaLibraryKit(self):
        return self._rnaLibraryKit

    def getRnaLibraryKitTier(self):
        return self._rnaLibraryKitTier

    def getRnaSeqPlatform(self):
        return self._rnaSeqPlatform

    def getRnaSeqPlatformTier(self):
        return self._rnaSeqPlatformTier

    def getRnaReadLength(self):
        return self._dnaReadLength

    def getRnaReadLengthTier(self):
        return self._dnaReadLengthTier

    def getPcrCycles(self):
        return self._pcrCycles

    def getPcrCyclesTier(self):
        return self._pcrCyclesTier

    def getExtractionId(self):
        return self._extractionId

    def getExtractionIdTier(self):
        return self._extractionIdTier

    def getSite(self):
        return self._site

    def getSiteTier(self):
        return self._siteTier


class Alignment(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.AlignmentCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(Alignment, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._alignmentId = None
        self._alignmentIdTier = None
        self._sampleId = None
        self._sampleIdTier = None
        self._inHousePipeline = None
        self._inHousePipelineTier = None
        self._alignmentTool = None
        self._alignmentToolTier = None
        self._mergeTool = None
        self._mergeToolTier = None
        self._markDuplicates = None
        self._markDuplicatesTier = None
        self._realignerTarget = None
        self._realignerTargetTier = None
        self._indelRealigner = None
        self._indelRealignerTier = None
        self._baseRecalibrator = None
        self._baseRecalibratorTier = None
        self._printReads = None
        self._printReadsTier = None
        self._idxStats = None
        self._idxStatsTier = None
        self._flagStat = None
        self._flagStatTier = None
        self._coverage = None
        self._coverageTier = None
        self._insertSizeMetrics = None
        self._insertSizeMetricsTier = None
        self._fastqc = None
        self._fastqcTier = None
        self._reference = None
        self._referenceTier = None
        self._sequencingId = None
        self._sequencingIdTier = None
        self._site = None
        self._siteTier = None

        self._objectAttr = {
            "alignmentId": self.getAlignmentId,
            "sampleId": self.getSampleId,
            "inHousePipeline": self.getInHousePipeline,
            "alignmentTool": self.getAlignmentTool,
            "mergeTool": self.getMergeTool,
            "markDuplicates": self.getMarkDuplicates,
            "realignerTarget": self.getRealignerTarget,
            "indelRealigner": self.getIndelRealigner,
            "baseRecalibrator": self.getBaseRecalibrator,
            "printReads": self.getPrintReads,
            "idxStats": self.getIdxStats,
            "flagStat": self.getFlagStat,
            "coverage": self.getCoverage,
            "insertSizeMetrics": self.getInsertSizeMetrics,
            "fastqc": self.getFastqc,
            "reference": self.getReference,
            "sequencingId": self.getSequencingId,
            "site": self.getSite
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getAlignmentIdTier():
                record['alignmentId'] = self.getAlignmentId()
            if tier >= self.getSampleIdTier():
                record['sampleId'] = self.getSampleId()
            if tier >= self.getInHousePipelineTier():
                record['inHousePipeline'] = self.getInHousePipeline()
            if tier >= self.getAlignmentToolTier():
                record['alignmentTool'] = self.getAlignmentTool()
            if tier >= self.getMergeToolTier():
                record['mergeTool'] = self.getMergeTool()
            if tier >= self.getMarkDuplicatesTier():
                record['markDuplicates'] = self.getMarkDuplicates()
            if tier >= self.getRealignerTargetTier():
                record['realignerTarget'] = self.getRealignerTarget()
            if tier >= self.getIndelRealignerTier():
                record['indelRealigner'] = self.getIndelRealigner()
            if tier >= self.getBaseRecalibratorTier():
                record['baseRecalibrator'] = self.getBaseRecalibrator()
            if tier >= self.getPrintReadsTier():
                record['printReads'] = self.getPrintReads()
            if tier >= self.getIdxStatsTier():
                record['idxStats'] = self.getIdxStats()
            if tier >= self.getFlagStatTier():
                record['flagStat'] = self.getFlagStat()
            if tier >= self.getCoverageTier():
                record['coverage'] = self.getCoverage()
            if tier >= self.getInsertSizeMetricsTier():
                record['insertSizeMetrics'] = self.getInsertSizeMetrics()
            if tier >= self.getFastqcTier():
                record['fastqc'] = self.getFastqc()
            if tier >= self.getReferenceTier():
                record['reference'] = self.getReference()
            if tier >= self.getSequencingIdTier():
                record['sequencingId'] = self.getSequencingId()
            if tier >= self.getSiteTier():
                record['site'] = self.getSite()
        except TypeError:
            pass

        Alignment = protocol.Alignment(**record)
        self.serializeMetadataAttributes(Alignment)

        return Alignment

    def populateFromRow(self, AlignmentRecord):
        """
        """
        self._created = AlignmentRecord.created
        self._updated = AlignmentRecord.updated
        self._name = AlignmentRecord.name
        self._description = AlignmentRecord.description
        self.setAttributesJson(AlignmentRecord.attributes)

        # Unique fields
        self._alignmentId = AlignmentRecord.alignmentId
        self._alignmentIdTier = AlignmentRecord.alignmentIdTier
        self._sampleId = AlignmentRecord.sampleId
        self._sampleIdTier = AlignmentRecord.sampleIdTier
        self._inHousePipeline = AlignmentRecord.inHousePipeline
        self._inHousePipelineTier = AlignmentRecord.inHousePipelineTier
        self._alignmentTool = AlignmentRecord.alignmentTool
        self._alignmentToolTier = AlignmentRecord.alignmentToolTier
        self._mergeTool = AlignmentRecord.mergeTool
        self._mergeToolTier = AlignmentRecord.mergeToolTier
        self._markDuplicates = AlignmentRecord.markDuplicates
        self._markDuplicatesTier = AlignmentRecord.markDuplicatesTier
        self._realignerTarget = AlignmentRecord.realignerTarget
        self._realignerTargetTier = AlignmentRecord.realignerTargetTier
        self._indelRealigner = AlignmentRecord.indelRealigner
        self._indelRealignerTier = AlignmentRecord.indelRealignerTier
        self._baseRecalibrator = AlignmentRecord.baseRecalibrator
        self._baseRecalibratorTier = AlignmentRecord.baseRecalibratorTier
        self._printReads = AlignmentRecord.printReads
        self._printReadsTier = AlignmentRecord.printReadsTier
        self._idxStats = AlignmentRecord.idxStats
        self._idxStatsTier = AlignmentRecord.idxStatsTier
        self._flagStat = AlignmentRecord.flagStat
        self._flagStatTier = AlignmentRecord.flagStatTier
        self._coverage = AlignmentRecord.coverage
        self._coverageTier = AlignmentRecord.coverageTier
        self._insertSizeMetrics = AlignmentRecord.insertSizeMetrics
        self._insertSizeMetricsTier = AlignmentRecord.insertSizeMetricsTier
        self._fastqc = AlignmentRecord.fastqc
        self._fastqcTier = AlignmentRecord.fastqcTier
        self._reference = AlignmentRecord.reference
        self._referenceTier = AlignmentRecord.referenceTier
        self._sequencingId = AlignmentRecord.sequencingId
        self._sequencingIdTier = AlignmentRecord.sequencingIdTier
        self._site = AlignmentRecord.site
        self._siteTier = AlignmentRecord.siteTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.Alignment)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._alignmentId = parsed.alignmentId
        self._alignmentIdTier = parsed.alignmentIdTier
        self._sampleId = parsed.sampleId
        self._sampleIdTier = parsed.sampleIdTier
        self._inHousePipeline = parsed.inHousePipeline
        self._inHousePipelineTier = parsed.inHousePipelineTier
        self._alignmentTool = parsed.alignmentTool
        self._alignmentToolTier = parsed.alignmentToolTier
        self._mergeTool = parsed.mergeTool
        self._mergeToolTier = parsed.mergeToolTier
        self._markDuplicates = parsed.markDuplicates
        self._markDuplicatesTier = parsed.markDuplicatesTier
        self._realignerTarget = parsed.realignerTarget
        self._realignerTargetTier = parsed.realignerTargetTier
        self._indelRealigner = parsed.indelRealigner
        self._indelRealignerTier = parsed.indelRealignerTier
        self._baseRecalibrator = parsed.baseRecalibrator
        self._baseRecalibratorTier = parsed.baseRecalibratorTier
        self._printReads = parsed.printReads
        self._printReadsTier = parsed.printReadsTier
        self._idxStats = parsed.idxStats
        self._idxStatsTier = parsed.idxStatsTier
        self._flagStat = parsed.flagStat
        self._flagStatTier = parsed.flagStatTier
        self._coverage = parsed.coverage
        self._coverageTier = parsed.coverageTier
        self._insertSizeMetrics = parsed.insertSizeMetrics
        self._insertSizeMetricsTier = parsed.insertSizeMetricsTier
        self._fastqc = parsed.fastqc
        self._fastqcTier = parsed.fastqcTier
        self._reference = parsed.reference
        self._referenceTier = parsed.referenceTier
        self._sequencingId = parsed.sequencingId
        self._sequencingIdTier = parsed.sequencingIdTier
        self._site = parsed.site
        self._siteTier = parsed.siteTier

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def getAlignmentId(self):
        return self._alignmentId

    def getAlignmentIdTier(self):
        return self._alignmentIdTier

    def getSampleId(self):
        return self._sampleId

    def getSampleIdTier(self):
        return self._sampleIdTier

    def getInHousePipeline(self):
        return self._inHousePipeline

    def getInHousePipelineTier(self):
        return self._inHousePipelineTier

    def getAlignmentTool(self):
        return self._alignmentTool

    def getAlignmentToolTier(self):
        return self._alignmentToolTier

    def getMergeTool(self):
        return self._mergeTool

    def getMergeToolTier(self):
        return self._mergeToolTier

    def getMarkDuplicates(self):
        return self._markDuplicates

    def getMarkDuplicatesTier(self):
        return self._markDuplicatesTier

    def getRealignerTarget(self):
        return self._realignerTarget

    def getRealignerTargetTier(self):
        return self._realignerTargetTier

    def getIndelRealigner(self):
        return self._indelRealigner

    def getIndelRealignerTier(self):
        return self._indelRealignerTier

    def getBaseRecalibrator(self):
        return self._baseRecalibrator

    def getBaseRecalibratorTier(self):
        return self._baseRecalibratorTier

    def getPrintReads(self):
        return self._printReads

    def getPrintReadsTier(self):
        return self._printReadsTier

    def getIdxStats(self):
        return self._idxStats

    def getIdxStatsTier(self):
        return self._idxStatsTier

    def getFlagStat(self):
        return self._flagStat

    def getFlagStatTier(self):
        return self._flagStatTier

    def getCoverage(self):
        return self._coverage

    def getCoverageTier(self):
        return self._coverageTier

    def getInsertSizeMetrics(self):
        return self._insertSizeMetrics

    def getInsertSizeMetricsTier(self):
        return self._insertSizeMetricsTier

    def getFastqc(self):
        return self._fastqc

    def getFastqcTier(self):
        return self._fastqcTier

    def getReference(self):
        return self._reference

    def getReferenceTier(self):
        return self._referenceTier

    def getSequencingId(self):
        return self._sequencingId

    def getSequencingIdTier(self):
        return self._sequencingIdTier

    def getSite(self):
        return self._site

    def getSiteTier(self):
        return self._siteTier


class VariantCalling(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.VariantCallingCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(VariantCalling, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._variantCallingId = None
        self._variantCallingIdTier = None
        self._sampleId = None
        self._sampleIdTier = None
        self._inHousePipeline = None
        self._inHousePipelineTier = None
        self._tabulate = None
        self._tabulateTier = None
        self._annotation = None
        self._annotationTier = None
        self._mergeTool = None
        self._mergeToolTier = None
        self._rdaToTab = None
        self._rdaToTabTier = None
        self._delly = None
        self._dellyTier = None
        self._postFilter = None
        self._postFilterTier = None
        self._clipFilter = None
        self._clipFilterTier = None
        self._cosmic = None
        self._cosmicTier = None
        self._dbSnp = None
        self._dbSnpTier = None
        self._alignmentId = None
        self._alignmentIdTier = None
        self._site = None
        self._siteTier = None

        self._objectAttr = {
            "variantCallingId": self.getVariantCallingId,
            "sampleId": self.getSampleId,
            "inHousePipeline": self.getInHousePipeline,
            "variantCaller": self.getVariantCaller,
            "tabulate": self.getTabulate,
            "annotation": self.getAnnotation,
            "mergeTool": self.getMergeTool,
            "rdaToTab": self.getRdaToTab,
            "delly": self.getDelly,
            "postFilter": self.getPostFilter,
            "clipFilter": self.getClipFilter,
            "cosmic": self.getCosmic,
            "dbSnp": self.getDbSnp,
            "alignmentId": self.getAlignmentId,
            "site": self.getSite,
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getVariantCallingIdTier():
                record['variantCallingId'] = self.getVariantCallingId()
            if tier >= self.getSampleIdTier():
                record['sampleId'] = self.getSampleId()
            if tier >= self.getInHousePipelineTier():
                record['inHousePipeline'] = self.getInHousePipeline()
            if tier >= self.getVariantCallerTier():
                record['variantCaller'] = self.getVariantCaller()
            if tier >= self.getTabulateTier():
                record['tabulate'] = self.getTabulate()
            if tier >= self.getAnnotationTier():
                record['annotation'] = self.getAnnotation()
            if tier >= self.getMergeToolTier():
                record['mergeTool'] = self.getMergeTool()
            if tier >= self.getRdaToTabTier():
                record['rdaToTab'] = self.getRdaToTab()
            if tier >= self.getDellyTier():
                record['delly'] = self.getDelly()
            if tier >= self.getPostFilterTier():
                record['postFilter'] = self.getPostFilter()
            if tier >= self.getClipFilterTier():
                record['clipFilter'] = self.getClipFilter()
            if tier >= self.getCosmicTier():
                record['cosmic'] = self.getCosmic()
            if tier >= self.getDbSnpTier():
                record['dbSnp'] = self.getDbSnp()
            if tier >= self.getAlignmentIdTier():
                record['alignmentId'] = self.getAlignmentId()
            if tier >= self.getSiteTier():
                record['site'] = self.getSite()
        except TypeError:
            pass

        VariantCalling = protocol.VariantCalling(**record)
        self.serializeMetadataAttributes(VariantCalling)

        return VariantCalling

    def populateFromRow(self, VariantCallingRecord):
        """
        """
        self._created = VariantCallingRecord.created
        self._updated = VariantCallingRecord.updated
        self._name = VariantCallingRecord.name
        self._description = VariantCallingRecord.description
        self.setAttributesJson(VariantCallingRecord.attributes)

        # Unique fields
        self._variantCallingId = VariantCallingRecord.variantCallingId
        self._variantCallingIdTier = VariantCallingRecord.variantCallingIdTier
        self._sampleId = VariantCallingRecord.sampleId
        self._sampleIdTier = VariantCallingRecord.sampleIdTier
        self._inHousePipeline = VariantCallingRecord.inHousePipeline
        self._inHousePipelineTier = VariantCallingRecord.inHousePipelineTier
        self._variantCaller = VariantCallingRecord.variantCaller
        self._variantCallerTier = VariantCallingRecord.variantCallerTier
        self._tabulate = VariantCallingRecord.tabulate
        self._tabulateTier = VariantCallingRecord.tabulateTier
        self._annotation = VariantCallingRecord.annotation
        self._annotationTier = VariantCallingRecord.annotationTier
        self._mergeTool = VariantCallingRecord.mergeTool
        self._mergeToolTier = VariantCallingRecord.mergeToolTier
        self._rdaToTab = VariantCallingRecord.rdaToTab
        self._rdaToTabTier = VariantCallingRecord.rdaToTabTier
        self._delly = VariantCallingRecord.delly
        self._dellyTier = VariantCallingRecord.dellyTier
        self._postFilter = VariantCallingRecord.postFilter
        self._postFilterTier = VariantCallingRecord.postFilterTier
        self._clipFilter = VariantCallingRecord.clipFilter
        self._clipFilterTier = VariantCallingRecord.clipFilterTier
        self._cosmic = VariantCallingRecord.cosmic
        self._cosmicTier = VariantCallingRecord.cosmicTier
        self._dbSnp = VariantCallingRecord.dbSnp
        self._dbSnpTier = VariantCallingRecord.dbSnpTier
        self._alignmentId = VariantCallingRecord.alignmentId
        self._alignmentIdTier = VariantCallingRecord.alignmentIdTier
        self._site = VariantCallingRecord.site
        self._siteTier = VariantCallingRecord.siteTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.VariantCalling)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._variantCallingId = parsed.variantCallingId
        self._variantCallingIdTier = parsed.variantCallingIdTier
        self._sampleId = parsed.sampleId
        self._sampleIdTier = parsed.sampleIdTier
        self._inHousePipeline = parsed.inHousePipeline
        self._inHousePipelineTier = parsed.inHousePipelineTier
        self._variantCaller = parsed.variantCaller
        self._variantCallerTier = parsed.variantCallerTier
        self._tabulate = parsed.tabulate
        self._tabulateTier = parsed.tabulateTier
        self._annotation = parsed.annotation
        self._annotationTier = parsed.annotationTier
        self._mergeTool = parsed.mergeTool
        self._mergeToolTier = parsed.mergeToolTier
        self._rdaToTab = parsed.rdaToTab
        self._rdaToTabTier = parsed.rdaToTabTier
        self._delly = parsed.delly
        self._dellyTier = parsed.dellyTier
        self._postFilter = parsed.postFilter
        self._postFilterTier = parsed.postFilterTier
        self._clipFilter = parsed.clipFilter
        self._clipFilterTier = parsed.clipFilterTier
        self._cosmic = parsed.cosmic
        self._cosmicTier = parsed.cosmicTier
        self._dbSnp = parsed.dbSnp
        self._dbSnpTier = parsed.dbSnpTier
        self._alignmentId = parsed.alignmentId
        self._alignmentIdTier = parsed.alignmentIdTier
        self._site = parsed.site
        self._siteTier = parsed.siteTier

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def getVariantCallingId(self):
        return self._variantCallingId

    def getVariantCallingIdTier(self):
        return self._variantCallingIdTier

    def getSampleId(self):
        return self._sampleId

    def getSampleIdTier(self):
        return self._sampleIdTier

    def getInHousePipeline(self):
        return self._inHousePipeline

    def getInHousePipelineTier(self):
        return self._inHousePipelineTier

    def getVariantCaller(self):
        return self._variantCaller

    def getVariantCallerTier(self):
        return self._variantCallerTier

    def getTabulate(self):
        return self._tabulate

    def getTabulateTier(self):
        return self._tabulateTier

    def getAnnotation(self):
        return self._annotation

    def getAnnotationTier(self):
        return self._annotationTier

    def getMergeTool(self):
        return self._mergeTool

    def getMergeToolTier(self):
        return self._mergeToolTier

    def getRdaToTab(self):
        return self._rdaToTab

    def getRdaToTabTier(self):
        return self._rdaToTabTier

    def getDelly(self):
        return self._delly

    def getDellyTier(self):
        return self._dellyTier

    def getPostFilter(self):
        return self._postFilter

    def getPostFilterTier(self):
        return self._postFilterTier

    def getClipFilter(self):
        return self._clipFilter

    def getClipFilterTier(self):
        return self._clipFilterTier

    def getCosmic(self):
        return self._cosmic

    def getCosmicTier(self):
        return self._cosmicTier

    def getDbSnp(self):
        return self._dbSnp

    def getDbSnpTier(self):
        return self._dbSnpTier

    def getAlignmentId(self):
        return self._alignmentId

    def getAlignmentIdTier(self):
        return self._alignmentIdTier

    def getSite(self):
        return self._site

    def getSiteTier(self):
        return self._siteTier


class FusionDetection(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.FusionDetectionCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(FusionDetection, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._fusionDetectionId = None
        self._fusionDetectionIdTier = None
        self._sampleId = None
        self._sampleIdTier = None
        self._inHousePipeline = None
        self._inHousePipelineTier = None
        self._svDetection = None
        self._svDetectionTier = None
        self._fusionDetection = None
        self._fusionDetectionTier = None
        self._realignment = None
        self._realignmentTier = None
        self._annotation = None
        self._annotationTier = None
        self._genomeReference = None
        self._genomeReferenceTier = None
        self._geneModels = None
        self._geneModelsTier = None
        self._alignmentId = None
        self._alignmentIdTier = None
        self._site = None
        self._siteTier = None

        self._objectAttr = {
            "fusionDetectionId": self.getFusionDetectionId,
            "sampleId": self.getSampleId,
            "inHousePipeline": self.getInHousePipeline,
            "svDetection": self.getSvDetection,
            "fusionDetection": self.getFusionDetection,
            "realignment": self.getRealignment,
            "annotation": self.getAnnotation,
            "genomeReference": self.getGenomeReference,
            "geneModels": self.getGeneModels,
            "alignmentId": self.getAlignmentId,
            "site": self.getSite,
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getFusionDetectionIdTier():
                record['fusionDetectionId'] = self.getFusionDetectionId()
            if tier >= self.getSampleIdTier():
                record['sampleId'] = self.getSampleId()
            if tier >= self.getInHousePipelineTier():
                record['inHousePipeline'] = self.getInHousePipeline()
            if tier >= self.getSvDetectionTier():
                record['svDetection'] = self.getSvDetection()
            if tier >= self.getFusionDetectionTier():
                record['fusionDetection'] = self.getFusionDetection()
            if tier >= self.getRealignmentTier():
                record['realignment'] = self.getRealignment()
            if tier >= self.getAnnotationTier():
                record['annotation'] = self.getAnnotation()
            if tier >= self.getGenomeReferenceTier():
                record['genomeReference'] = self.getGenomeReference()
            if tier >= self.getGeneModelsTier():
                record['geneModels'] = self.getGeneModels()
            if tier >= self.getAlignmentIdTier():
                record['alignmentId'] = self.getAlignmentId()
            if tier >= self.getSiteTier():
                record['site'] = self.getSite()
        except TypeError:
            pass

        FusionDetection = protocol.FusionDetection(**record)
        self.serializeMetadataAttributes(FusionDetection)

        return FusionDetection

    def populateFromRow(self, FusionDetectionRecord):
        """
        """
        self._created = FusionDetectionRecord.created
        self._updated = FusionDetectionRecord.updated
        self._name = FusionDetectionRecord.name
        self._description = FusionDetectionRecord.description
        self.setAttributesJson(FusionDetectionRecord.attributes)

        # Unique fields
        self._fusionDetectionId = FusionDetectionRecord.fusionDetectionId
        self._fusionDetectionIdTier = FusionDetectionRecord.fusionDetectionIdTier
        self._sampleId = FusionDetectionRecord.sampleId
        self._sampleIdTier = FusionDetectionRecord.sampleIdTier
        self._inHousePipeline = FusionDetectionRecord.inHousePipeline
        self._inHousePipelineTier = FusionDetectionRecord.inHousePipelineTier
        self._svDetection = FusionDetectionRecord.svDetection
        self._svDetectionTier = FusionDetectionRecord.svDetectionTier
        self._fusionDetection = FusionDetectionRecord.fusionDetection
        self._fusionDetectionTier = FusionDetectionRecord.fusionDetectionTier
        self._realignment = FusionDetectionRecord.realignment
        self._realignmentTier = FusionDetectionRecord.realignmentTier
        self._annotation = FusionDetectionRecord.annotation
        self._annotationTier = FusionDetectionRecord.annotationTier
        self._genomeReference = FusionDetectionRecord.genomeReference
        self._genomeReferenceTier = FusionDetectionRecord.genomeReferenceTier
        self._geneModels = FusionDetectionRecord.geneModels
        self._geneModelsTier = FusionDetectionRecord.geneModelsTier
        self._alignmentId = FusionDetectionRecord.alignmentId
        self._alignmentIdTier = FusionDetectionRecord.alignmentIdTier
        self._site = FusionDetectionRecord.site
        self._siteTier = FusionDetectionRecord.siteTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.FusionDetection)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._fusionDetectionId = parsed.fusionDetectionId
        self._fusionDetectionIdTier = parsed.fusionDetectionIdTier
        self._sampleId = parsed.sampleId
        self._sampleIdTier = parsed.sampleIdTier
        self._inHousePipeline = parsed.inHousePipeline
        self._inHousePipelineTier = parsed.inHousePipelineTier
        self._svDetection = parsed.svDetection
        self._svDetectionTier = parsed.svDetectionTier
        self._fusionDetection = parsed.fusionDetection
        self._fusionDetectionTier = parsed.fusionDetectionTier
        self._realignment = parsed.realignment
        self._realignmentTier = parsed.realignmentTier
        self._annotation = parsed.annotation
        self._annotationTier = parsed.annotationTier
        self._genomeReference = parsed.genomeReference
        self._genomeReferenceTier = parsed.genomeReferenceTier
        self._geneModels = parsed.geneModels
        self._geneModelsTier = parsed.geneModelsTier
        self._alignmentId = parsed.alignmentId
        self._alignmentIdTier = parsed.alignmentIdTier
        self._site = parsed.site
        self._siteTier = parsed.siteTier

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def getFusionDetectionId(self):
        return self._fusionDetectionId

    def getFusionDetectionIdTier(self):
        return self._fusionDetectionIdTier

    def getSampleId(self):
        return self._sampleId

    def getSampleIdTier(self):
        return self._sampleIdTier

    def getInHousePipeline(self):
        return self._inHousePipeline

    def getInHousePipelineTier(self):
        return self._inHousePipelineTier

    def getSvDetection(self):
        return self._svDetection

    def getSvDetectionTier(self):
        return self._svDetectionTier

    def getFusionDetection(self):
        return self._fusionDetection

    def getFusionDetectionTier(self):
        return self._fusionDetectionTier

    def getRealignment(self):
        return self._realignment

    def getRealignmentTier(self):
        return self._realignmentTier

    def getAnnotation(self):
        return self._annotation

    def getAnnotationTier(self):
        return self._annotationTier

    def getGenomeReference(self):
        return self._genomeReference

    def getGenomeReferenceTier(self):
        return self._genomeReferenceTier

    def getGeneModels(self):
        return self._geneModels

    def getGeneModelsTier(self):
        return self._geneModelsTier

    def getAlignmentId(self):
        return self._alignmentId

    def getAlignmentIdTier(self):
        return self._alignmentIdTier

    def getSite(self):
        return self._site

    def getSiteTier(self):
        return self._siteTier


class ExpressionAnalysis(datamodel.DatamodelObject):
    """
    """
    compoundIdClass = datamodel.ExpressionAnalysisCompoundId

    def __init__(self, parentContainer, localId):
        """
        """
        # Call parent constructor
        super(ExpressionAnalysis, self).__init__(parentContainer, localId)

        # Common fields
        self._created = datetime.datetime.now().isoformat()
        self._updated = datetime.datetime.now().isoformat()
        self._name = localId
        self._description = None
        self._datasetId = parentContainer.getId()

        # Unique fields
        self._expressionAnalysisId = None
        self._expressionAnalysisIdTier = None
        self._sampleId = None
        self._sampleIdTier = None
        self._readLength = None
        self._readLengthTier = None
        self._reference = None
        self._referenceTier = None
        self._alignmentTool = None
        self._alignmentToolTier = None
        self._bamHandling = None
        self._bamHandlingTier = None
        self._expressionEstimation = None
        self._expressionEstimationTier = None
        self._sequencingId = None
        self._sequencingIdTier = None
        self._site = None
        self._siteTier = None

        self._objectAttr = {
            "expressionAnalysisId": self.getExpressionAnalysisId,
            "sampleId": self.getSampleId,
            "readLength": self.getReadLength,
            "reference": self.getReference,
            "alignmentTool": self.getAlignmentTool,
            "bamHandling": self.getBamHandling(),
            "expressionEstimation": self.getExpressionEstimation,
            "sequencingId": self.getSequencingId,
            "site": self.getSite
        }

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            'id': self.getId(),
            'dataset_id': self._datasetId,
            'created': self.getCreated(),
            'updated': self.getUpdated(),
            'name': self.getName(),
            'description': self.getDescription(),
        }

        # Unique fields
        try:
            if tier >= self.getExpressionAnalysisIdTier():
                record['expressionAnalysisId'] = self.getExpressionAnalysisId()
            if tier >= self.getSampleIdTier():
                record['sampleId'] = self.getSampleId()
            if tier >= self.getReadLengthTier():
                record['readLength'] = self.getReadLength()
            if tier >= self.getReferenceTier():
                record['reference'] = self.getReference()
            if tier >= self.getAlignmentToolTier():
                record['alignmentTool'] = self.getAlignmentTool()
            if tier >= self.getBamHandlingTier():
                record['bamHandling'] = self.getBamHandling()
            if tier >= self.getExpressionEstimationTier():
                record['expressionEstimation'] = self.getExpressionEstimation()
            if tier >= self.getSequencingIdTier():
                record['sequencingId'] = self.getSequencingId()
            if tier >= self.getSiteTier():
                record['site'] = self.getSite()
        except TypeError:
            pass

        ExpressionAnalysis = protocol.ExpressionAnalysis(**record)
        self.serializeMetadataAttributes(ExpressionAnalysis)

        return ExpressionAnalysis

    def populateFromRow(self, ExpressionAnalysisRecord):
        """
        """
        self._created = ExpressionAnalysisRecord.created
        self._updated = ExpressionAnalysisRecord.updated
        self._name = ExpressionAnalysisRecord.name
        self._description = ExpressionAnalysisRecord.description
        self.setAttributesJson(ExpressionAnalysisRecord.attributes)

        # Unique fields
        self._expressionAnalysisId = ExpressionAnalysisRecord.expressionAnalysisId
        self._expressionAnalysisIdTier = ExpressionAnalysisRecord.expressionAnalysisIdTier
        self._sampleId = ExpressionAnalysisRecord.sampleId
        self._sampleIdTier = ExpressionAnalysisRecord.sampleIdTier
        self._readLength = ExpressionAnalysisRecord.readLength
        self._readLengthTier = ExpressionAnalysisRecord.readLengthTier
        self._reference = ExpressionAnalysisRecord.reference
        self._referenceTier = ExpressionAnalysisRecord.referenceTier
        self._alignmentTool = ExpressionAnalysisRecord.alignmentTool
        self._alignmentToolTier = ExpressionAnalysisRecord.alignmentToolTier
        self._bamHandling = ExpressionAnalysisRecord.bamHandling
        self._bamHandlingTier = ExpressionAnalysisRecord.bamHandlingTier
        self._expressionEstimation = ExpressionAnalysisRecord.expressionEstimation
        self._expressionEstimationTier = ExpressionAnalysisRecord.expressionEstimationTier
        self._sequencingId = ExpressionAnalysisRecord.sequencingId
        self._sequencingIdTier = ExpressionAnalysisRecord.sequencingIdTier
        self._site = ExpressionAnalysisRecord.site
        self._siteTier = ExpressionAnalysisRecord.siteTier

        return self

    def populateFromJson(self, jsonString):
        """
        """
        try:
            parsed = protocol.fromJson(jsonString, protocol.ExpressionAnalysis)
        except:
            raise exceptions.InvalidJsonException(jsonString)
        self._created = parsed.created
        self._updated = parsed.updated
        self._name = parsed.name
        self._description = parsed.description
        attributes = {}
        for key in parsed.attributes.attr:
            attributes[key] = protocol.toJsonDict(parsed.attributes.attr[key])['values']
        self.setAttributes(attributes)

        # Unique fields
        self._expressionAnalysisId = parsed.expressionAnalysisId
        self._expressionAnalysisIdTier = parsed.expressionAnalysisIdTier
        self._sampleId = parsed.sampleId
        self._sampleIdTier = parsed.sampleIdTier
        self._readLength = parsed.readLength
        self._readLengthTier = parsed.readLengthTier
        self._reference = parsed.reference
        self._referenceTier = parsed.referenceTier
        self._alignmentTool = parsed.alignmentTool
        self._alignmentToolTier = parsed.alignmentToolTier
        self._bamHandling = parsed.bamHandling
        self._bamHandlingTier = parsed.bamHandlingTier
        self._expressionEstimation = parsed.expressionEstimation
        self._expressionEstimationTier = parsed.expressionEstimationTier
        self._sequencingId = parsed.sequencingId
        self._sequencingIdTier = parsed.sequencingIdTier
        self._site = parsed.site
        self._siteTier = parsed.siteTier

        return self

    def getCreated(self):
        return self._created

    def getUpdated(self):
        return self._updated

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def getExpressionAnalysisId(self):
        return self._expressionAnalysisId

    def getExpressionAnalysisIdTier(self):
        return self._expressionAnalysisIdTier

    def getSampleId(self):
        return self._sampleId

    def getSampleIdTier(self):
        return self._sampleIdTier

    def getReadLength(self):
        return self._readLength

    def getReadLengthTier(self):
        return self._readLengthTier

    def getReference(self):
        return self._reference

    def getReferenceTier(self):
        return self._referenceTier

    def getAlignmentTool(self):
        return self._alignmentTool

    def getAlignmentToolTier(self):
        return self._alignmentToolTier

    def getBamHandling(self):
        return self._bamHandling

    def getBamHandlingTier(self):
        return self._bamHandlingTier

    def getExpressionEstimation(self):
        return self._expressionEstimation

    def getExpressionEstimationTier(self):
        return self._expressionEstimationTier

    def getSequencingId(self):
        return self._sequencingId

    def getSequencingIdTier(self):
        return self._sequencingIdTier

    def getSite(self):
        return self._site

    def getSiteTier(self):
        return self._siteTier