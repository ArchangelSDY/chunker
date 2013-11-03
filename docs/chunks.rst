Chunks
===================================

A file usually contains many types of chunks. In most occasions, chunks are not arranged in a fixed order. So we need to use :meth:`matches` to read a few bytes first to detect if the following data match the specific chunk type.

.. autoclass:: chunks.Chunk
    :members:
