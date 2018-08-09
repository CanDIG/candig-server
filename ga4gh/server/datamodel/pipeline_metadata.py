"""
CanDIG - 2018-08-07

Pipeline metadata objects

"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import json

import ga4gh.server.datamodel as datamodel
import ga4gh.server.exceptions as exceptions

import ga4gh.schemas.protocol as protocol

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

    def toProtocolElement(self, tier=0):
        """
        """
        record = {
            str('id'): str(self.getId()),
            str('dataset_id'): str(self._datasetId),
            str('created'): str(self.getCreated()),
            str('updated'): str(self.getUpdated()),
            str('name'): str(self.getName()),
            str('description'): str(self.getDescription()),
        }

        # Unique fields
        if tier >= self.getExtractionIdTier():
            record[str('extractionId')] = str(self.getExtractionId())
        if tier >= self.getSampleIdTier():
            record[str('sampleId')] = str(self.getSampleId())
        if tier >= self.getRnaBloodTier():
            record[str('rnaBlood')] = str(self.getRnaBlood())
        if tier >= self.getDnaBloodTier():
            record[str('dnaBlood')] = str(self.getDnaBlood())
        if tier >= self.getRnaTissueTier():
            record[str('rnaTissue')] = str(self.getRnaTissue())
        if tier >= self.getDnaTissueTier():
            record[str('dnaTissue')] = str(self.getDnaTissue())

        Extraction = protocol.Extraction(**record)
        self.serializeAttributes(Extraction)

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
            attributes[key] = {
                "values": protocol.toJsonDict(parsed.attributes.attr[key])}
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