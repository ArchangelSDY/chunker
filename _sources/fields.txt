Fields
===================================

Fields are data components within a chunk. When a chunk populating, data inside are parsed and populated by the order of their defination in :attr:`Chunk.Fields`. Then we can access them as attributes of the chunk by their names.

.. HINT::
    Feel free to send me pull requests on `GitHub <https://github.com/ArchangelSDY/chunker>`_ if fields listed here cannot meet your needs.

Example::

    class DataChunk(Chunk):
        # Fields are parsed in this order
        Fields = (
            UnsignedLongField('data_length'),
            StringField('data', length_field_name='data_length'),
            UnsignedLongField('extra_length'),
            SkipBasedOnLengthField('extra', length_field_name='extra_length'),
        )

.. autoclass:: fields.Field

Fixed Length Fields
-----------------------------------

Fixed length fields are used for simple data with fixed length.

.. autoclass:: fields.BytesField

.. autoclass:: fields.UnsignedLongField

.. autoclass:: fields.UnsignedShortField

.. autoclass:: fields.UnsignedCharField

Variable Length Fields
-----------------------------------

Variable length fields are used for data with variable length. They usually rely on other fields to provide their lengths.

Example::

    class DataChunk(Chunk):
        Fields = (
            UnsignedLongField('length'),
            StringField('data', length_field_name='length'),
        )

.. autoclass:: fields.VariableLengthField

.. autoclass:: fields.StringField

Skip Fields
-----------------------------------

Sometimes we are not interested in all fields and only want to extract part of them. In these conditions, we can use skip fields as placeholders. Skip fields simply move forward without reading any bytes so that we can save memory and parse faster.

Example::

    class DataChunk(Chunk):
        Fields = (
            UnsignedLongField('data_length'),

            # Skip data whose length is extracted from 'data_length' field.
            SkipBasedOnLengthField('data', length_field_name='data_length'),

            # Skip data whose length is 3 times of the 'data_length'.
            SkipBasedOnCalcField('detailed_data', calc_func=lambda c: 3 * c.data_length),

            # Skip data left to end of the file object.
            SkipToTheEndField('extra'),
        )

.. autoclass:: fields.SkipBasedOnLengthField

.. autoclass:: fields.SkipBasedOnCalcField

.. autoclass:: fields.SkipToTheEndField
