"""
Class that builds the responses to the client
"""

import candig.schemas.pb as pb
import candig.schemas.protocol as protocol


class SearchResponseBuilder(object):
    """
    A class to allow sequential building of SearchResponse objects.
    """
    def __init__(self, responseClass, pageSize, maxBufferSize,
                 return_mimetype="application/json"):
        """
        Allocates a new SearchResponseBuilder for the specified
        responseClass, user-requested pageSize and the system mandated
        maxBufferSize (in bytes). The maxBufferSize is an
        approximate limit on the overall length of the serialised
        response.
        """
        self._pageSize = pageSize
        self._maxBufferSize = maxBufferSize
        self._numElements = 0
        self._nextPageToken = None
        self._protoObject = responseClass()
        self._valueListName = protocol.getValueListName(responseClass)
        self._bufferSize = self._protoObject.ByteSize()
        self._return_mimetype = return_mimetype

    def getPageSize(self):
        """
        Returns the page size for this SearchResponseBuilder. This is the
        user-requested maximum size for the number of elements in the
        value list.
        """
        return self._pageSize

    def getMaxBufferSize(self):
        """
        Returns the maximum internal buffer size for responses, which
        corresponds to total length (in bytes) of the serialised protobuf
        objects. This will always be less than the size of JSON output.
        """
        return self._maxBufferSize

    def getNextPageToken(self):
        """
        Returns the value of the nextPageToken for this
        SearchResponseBuilder.
        """
        return self._nextPageToken

    def setNextPageToken(self, nextPageToken):
        """
        Sets the nextPageToken to the specified value.
        """
        self._nextPageToken = nextPageToken

    def addValue(self, protocolElement):
        """
        Appends the specified protocolElement to the value list for this
        response.
        """
        self._numElements += 1
        self._bufferSize += protocolElement.ByteSize()
        attr = getattr(self._protoObject, self._valueListName)
        obj = attr.add()
        obj.CopyFrom(protocolElement)

    def isFull(self):
        """
        Returns True if the response buffer is full, and False otherwise.
        The buffer is full if either (1) the number of items in the value
        list is >= pageSize or (2) the total length of the serialised
        elements in the page is >= maxBufferSize.

        If page_size or max_response_length were not set in the request
        then they're not checked.
        """
        return (
            (self._pageSize > 0 and self._numElements >= self._pageSize) or
            (self._bufferSize >= self._maxBufferSize)
        )

    def getSerializedResponse(self):
        """
        Returns a string version of the SearchResponse that has
        been built by this SearchResponseBuilder.
        """
        self._protoObject.next_page_token = pb.string(self._nextPageToken)
        s = protocol.serialize(self._protoObject, self._return_mimetype)
        return s
