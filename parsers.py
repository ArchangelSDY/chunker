import os


class Parser:
    Chunk_Classes = ()

    def __init__(self, fp):
        self.fp = fp
        self.total_length = Parser.get_total_length(fp)
        self.chunks = []

    @staticmethod
    def get_total_length(fp):
        return os.fstat(fp.fileno()).st_size

    def parse(self):
        while self.fp.tell() < self.total_length:
            for chunk_cls in self.__class__.Chunk_Classes:
                if chunk_cls.matches(self.fp):
                    chunk = chunk_cls(self.fp)
                    self.chunks.append(chunk)
                    break
