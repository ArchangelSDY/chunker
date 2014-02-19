.. Chunker documentation master file, created by
   sphinx-quickstart on Sun Nov  3 00:14:38 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Chunker - Easy Chunk-Based File Structure Parsing
=================================================

Chunker provides simple APIs to help parsing chunk-based file structure such as Zip/PNG/JPEG/WAV, etc.

You simply define the structure and Chunker handles the rest.

.. toctree::
   :maxdepth: 2

   parsers
   chunks
   fields
   utils

An example printing out file names in a `zip <http://en.wikipedia.org/wiki/Zip_%28file_format%29>`_ file::

    class InsideFileChunk(Chunk):
        Fields = (
            # We've read signature already when doing matching
            UnsignedShortField('min_ver'),
            UnsignedShortField('general_purpose'),
            UnsignedShortField('compress_method'),
            UnsignedShortField('last_modified_time'),
            UnsignedShortField('last_modified_date'),
            UnsignedLongField('crc32'),
            UnsignedLongField('compressed_size'),
            UnsignedLongField('uncompressed_size'),
            UnsignedShortField('filename_length'),
            UnsignedShortField('extra_field_length'),
            StringField('filename', 'filename_length'),
            SkipBasedOnLengthField('extra_field', 'extra_field_length'),
            SkipBasedOnLengthField('data', 'compressed_size'),  # No need to read file content
        )

        @staticmethod
        def matches(fp):
            # Each file chunk starts with 0x04034b50
            buf = fp.read(4)
            sig = struct.unpack('<L', buf)[0]
            if sig == 0x04034b50:
                return True
            else:
                fp.seek(-4, os.SEEK_CUR)
                return False

    class SkipTheLeftChunk(ToTheEndChunk):
        @staticmethod
        def matches(fp):
            buf = fp.read(4)
            sig = struct.unpack('<L', buf)[0]
            if sig != 0x04034b50:
                return True
            else:
                fp.seek(-4, os.SEEK_CUR)
                return False

        def populate(self):
            # Skip the left
            self.fp.seek(0, os.SEEK_END)

    class ZipParser(FileParser):
        ChunkClasses = (
            InsideFileChunk,    # Chunk indicating files in the zip package.
            SkipTheLeftChunk,   # We have no interest in other chunk types at the end of the zip file.
        )

    p = ZipParser('test.zip')
    p.parse()
    for chunk in p.chunks:
        if isinstance(chunk, InsideFileChunk):
            print chunk.filename
