import os
import StringIO
import struct
import unittest

from chunks import Chunk
from fields import UnsignedLongField, UnsignedShortField
from parsers import Parser, ParseTimeoutException


class OneFieldChunk(Chunk):
    Fields = (
        UnsignedLongField('long'),
    )

    @staticmethod
    def matches(fp):
        buf = fp.read(4)
        sig = struct.unpack('<L', buf)[0]
        if sig == 0x010101010:
            return True
        else:
            fp.seek(-4, os.SEEK_CUR)
            return False


class TwoFieldChunk(Chunk):
    Fields = (
        UnsignedLongField('long'),
        UnsignedShortField('short'),
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
        long = 10
        self.fp.write(struct.pack('<L', long))
        short = 5
        self.fp.write(struct.pack('<H', short))
        self.fp.seek(0)

        self.fake_fp = StringIO.StringIO()
        sig = 0x04030201
        self.fake_fp.write(struct.pack('<L', sig))
        self.fake_fp.seek(0)

    def test_match(self):
        self.assertTrue(TwoFieldChunk.matches(self.fp))
        self.assertEquals(self.fp.tell(), 4)

        self.assertFalse(TwoFieldChunk.matches(self.fake_fp))
        self.assertEquals(self.fake_fp.tell(), 0)

    def test_populate(self):
        self.assertTrue(TwoFieldChunk.matches(self.fp))
        c = TwoFieldChunk(self.fp, None)
        c.populate()
        self.assertEquals(c.long, 10)
        self.assertEquals(c.short, 5)

    def tearDown(self):
        self.fp.close()
        self.fake_fp.close()


class TwoChunksParser(Parser):
    ChunkClasses = (
        TwoFieldChunk,
        OneFieldChunk,
    )


class QuickTimeoutParser(Parser):
    Timeout = 0


class ParserTest(unittest.TestCase):
    TempFile = 'test.tmp'

    def setUp(self):
        self.fp = open(ParserTest.TempFile, 'wb+')

        # Chunk 1
        sig = 0x01020304
        self.fp.write(struct.pack('<L', sig))
        long = 10
        self.fp.write(struct.pack('<L', long))
        short = 5
        self.fp.write(struct.pack('<H', short))

        # Chunk 2
        sig = 0x10101010
        self.fp.write(struct.pack('<L', sig))
        long = 15
        self.fp.write(struct.pack('<L', long))

        # Reset cursor
        self.fp.flush()
        self.fp.seek(0)

    def test_parse(self):
        parser = TwoChunksParser(self.fp)
        parser.parse()
        self.assertEquals(parser.chunks[0].long, 10)
        self.assertEquals(parser.chunks[0].short, 5)
        self.assertEquals(parser.chunks[1].long, 15)
        self.assertFalse(parser.is_timeout)

    def test_timeout(self):
        with self.assertRaises(ParseTimeoutException):
            parser = QuickTimeoutParser(self.fp)
            parser.parse()
            self.assertTrue(parser.is_timeout)

    def tearDown(self):
        self.fp.close()

        if os.path.exists(ParserTest.TempFile):
            os.remove(ParserTest.TempFile)


if __name__ == '__main__':
    unittest.main()
