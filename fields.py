import struct


class Field(object):
    def __init__(self, name, fmt, length):
        self.name = name
        self.value = None
        self.fmt = fmt
        self.length = length

    def populate(self, fp):
        buf = fp.read(self.length)
        self.value = struct.unpack(self.fmt, buf)[0]


class UnsignedLongField(Field):
    def __init__(self, name, big_endian=False):
        endian = '>' if big_endian else '<'
        fmt = endian + 'L'
        super(UnsignedLongField, self).__init__(name, fmt, 4)


class UnsignedShortField(Field):
    def __init__(self, name, big_endian=False):
        endian = '>' if big_endian else '<'
        fmt = endian + 'H'
        super(UnsignedLongField, self).__init__(name, fmt, 2)
