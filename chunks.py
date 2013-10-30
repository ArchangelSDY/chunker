class Chunk(object):
    Fields = ()

    def __new__(cls, *args, **kargs):
        cls.Fields_Map = {f.name: f for f in cls.Fields}
        return super(Chunk, cls).__new__(cls, *args, **kargs)

    def __init__(self, fp):
        self.populate(fp)

    def __getattr__(self, key):
        return self.__class__.Fields_Map[key].value

    @staticmethod
    def matches(fp):
        return False

    def populate(self, fp):
        for field in self.__class__.Fields:
            field.populate(fp)
