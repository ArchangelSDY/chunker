import os
import struct


class Field(object):
    def __init__(self, name):
        self.name = name
        self.value = None
        self.length = 0

    def populate(self, fp, chunk):
        raise NotImplementedError('Field is abstract.')


class BytesField(Field):
    def __init__(self, name, fmt, length):
        super(BytesField, self).__init__(name)
        self.name = name
        self.fmt = fmt
        self.length = length

    def populate(self, fp, chunk):
        buf = fp.read(self.length)
        self.value = struct.unpack(self.fmt, buf)[0]


class UnsignedLongField(BytesField):
    def __init__(self, name, big_endian=False):
        endian = '>' if big_endian else '<'
        fmt = endian + 'L'
        super(UnsignedLongField, self).__init__(name, fmt, 4)


class UnsignedShortField(BytesField):
    def __init__(self, name, big_endian=False):
        endian = '>' if big_endian else '<'
        fmt = endian + 'H'
        super(UnsignedShortField, self).__init__(name, fmt, 2)


class UnsignedCharField(BytesField):
    def __init__(self, name, big_endian=False):
        endian = '>' if big_endian else '<'
        fmt = endian + 'B'
        super(UnsignedCharField, self).__init__(name, fmt, 1)


class VariableLengthField(Field):
    def __init__(self, name, length_field_name):
        super(VariableLengthField, self).__init__(name)
        self.length_field_name = length_field_name

    def populate(self, fp, chunk):
        self.length = chunk.__getattr__(self.length_field_name)


class StringField(VariableLengthField):
    def populate(self, fp, chunk):
        super(StringField, self).populate(fp, chunk)
        self.value = fp.read(self.length)


class SkipBasedOnCalcField(Field):
    def __init__(self, name, calc_func):
        super(SkipBasedOnCalcField, self).__init__(name)
        self.calc_func = calc_func

    def populate(self, fp, chunk):
        offset = self.calc_func(chunk)
        fp.seek(offset, os.SEEK_CUR)


class SkipBasedOnLengthField(VariableLengthField):
    def populate(self, fp, chunk):
        super(SkipBasedOnLengthField, self).populate(fp, chunk)
        fp.seek(self.length, os.SEEK_CUR)


class SkipToTheEndField(Field):
    def populate(self, fp, chunk):
        fp.seek(chunk.parser.total_length, os.SEEK_SET)
