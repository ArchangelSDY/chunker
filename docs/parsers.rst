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

    .. attribute:: fp

        FilePtr object to read.

    .. attribute:: chunks

        A list of chunks inside.

.. autoclass:: parsers.FileParser

.. autoexception:: parsers.ParseTimeoutException
