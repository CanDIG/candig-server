"""
Tests the file handle cache
"""

import os
import shutil
import tempfile
import unittest
import uuid

import candig.server.datamodel as datamodel


class TestFileHandleCache(datamodel.PysamFileHandleCache, unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFileHandleCache, self).__init__()
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        self._tempdir = tempfile.mkdtemp(prefix="ga4gh_file_cache",
                                         dir=tempfile.gettempdir())

    def _getFileHandle(self, dataFile):
        def openMethod(dataFile):
            return open(dataFile, 'w')
        return self.getFileHandle(dataFile, openMethod)

    def testGetFileHandle(self):
        def genFileName(x):
            return os.path.join(self._tempdir, str(uuid.uuid4()))

        # Set cache size to 9 files max
        self.setMaxCacheSize(9)

        # Build a list of 10 files and add their handles to the cache
        fileList = list(map(genFileName, range(0, 10)))

        for f in fileList:
            handle = self._getFileHandle(f)
            self.assertEqual(self._cache.count((f, handle)), 1)

        self.assertEqual(len(self._memoTable), len(self._cache))

        # Ensure that the first added file has been removed from the cache
        self.assertEqual([x for x in self._cache if x[0] == fileList[0]], [])

        topIndex = len(self._cache) - 1

        # Update priority of this file and ensure it's no longer the
        # least recently used
        self.assertEqual(self._cache[topIndex][0], fileList[1])
        self._getFileHandle(fileList[1])
        self.assertNotEqual(self._cache[topIndex][0], fileList[1])
        self.assertEqual(self._cache[0][0], fileList[1])

    def testSetCacheMaxSize(self):
        self.assertRaises(ValueError, self.setMaxCacheSize, 0)
        self.assertRaises(ValueError, self.setMaxCacheSize, -1)

    def tearDown(self):
        shutil.rmtree(self._tempdir)
