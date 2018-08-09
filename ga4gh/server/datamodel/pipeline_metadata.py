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
    compoundIdClass = datamodel.PatientCompoundId

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

