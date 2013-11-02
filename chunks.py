import copy
import os


class Chunk(object):
    Fields = ()

    def __new__(cls, *args, **kargs):
        instance = super(Chunk, cls).__new__(cls, *args, **kargs)
        instance.fields = copy.deepcopy(cls.Fields)
        instance.fields_map = {f.name: f for f in instance.fields}
        return instance

    def __init__(self, fp, parser):
        self.fp = fp
        self.parser = parser

    def __getattr__(self, key):
        return self.fields_map[key].value

    @staticmethod
    def matches(fp):
        return False

    def populate(self):
        for field in self.fields:
            field.populate(self.fp, self)

    def __str__(self):
        dumps = []
        dumps.append('\n----------')
        for field in self.fields:
            dumps.append('%s: %s' % (field.name, field.value))
        dumps.append('----------\n')
        return '\n'.join(dumps)


class ToTheEndChunk(Chunk):
    def populate(self, fp):
        fp.seek(0, os.SEEK_END)
