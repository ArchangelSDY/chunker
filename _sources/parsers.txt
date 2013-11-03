Parsers
===================================

A parser defines chunk types it could meet during parsing.

Example::

    class DataParser(FileParser):
        ChunkClasses = (
            HeaderChunk,
            DataChunk,
        )

.. autoclass:: parsers.Parser

    .. attribute:: total_length

        Total length of the stream.

    .. attribute:: chunks

        A list of chunks inside.

.. autoclass:: parsers.FileParser

.. autoexception:: parsers.ParseTimeoutException
