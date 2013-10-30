import os
import StringIO
import struct
import unittest

from chunks import Chunk
from fields import UnsignedLongField


class OneFieldChunk(Chunk):
    Fields = (
        UnsignedLongField('key'),
    )

    @staticmethod
    def matches(fp):
        buf = fp.read(4)
        sig = struct.unpack('<L', buf)[0]
        if sig == 0x01020304:
            return True
        else:
            fp.seek(-4, os.SEEK_CUR)
            return False


class ChunkTest(unittest.TestCase):
    def setUp(self):
        self.fp = StringIO.StringIO()
        sig = 0x01020304
        self.fp.write(struct.pack('<L', sig))
        key = 10
        self.fp.write(struct.pack('<L', key))
        self.fp.seek(0)

        self.fake_fp = StringIO.StringIO()
        sig = 0x04030201
        self.fake_fp.write(struct.pack('<L', sig))
        self.fake_fp.seek(0)

    def test_match(self):
        self.assertTrue(OneFieldChunk.matches(self.fp))
        self.assertEquals(self.fp.tell(), 4)

        self.assertFalse(OneFieldChunk.matches(self.fake_fp))
        self.assertEquals(self.fake_fp.tell(), 0)

    def test_populate(self):
        self.assertTrue(OneFieldChunk.matches(self.fp))
        c = OneFieldChunk(self.fp)
        self.assertEquals(c.key, 10)

    def tearDown(self):
        self.fp.close()
        self.fake_fp.close()


if __name__ == '__main__':
    unittest.main()
