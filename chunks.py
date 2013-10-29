class Chunk(object):
    fields = ()
    fields_map = {}

    def __init__(self, fp):
        self.fields_map = {f.name: f for f in self.fields}
        self.populate(fp)

    def __getattr__(self, key):
        return self.fields_map[key].value

    @staticmethod
    def matches(fp):
        return False

    def populate(self, fp):
        for field in self.fields:
            field.populate(fp)
