import os
import threading


class ParseTimeoutException(Exception):
    pass


class Parser(object):
    ChunkClasses = ()
    Timeout = 60

    def __init__(self, fp, total_length=None):
        self.fp = fp
        if total_length is not None:
            self.total_length = total_length
        else:
            self.total_length = Parser.get_file_length(fp)
        self.chunks = []
        self._timeout_timer = None
        self.is_timeout = False

    @staticmethod
    def get_file_length(fp):
        return os.fstat(fp.fileno()).st_size

    def parse(self):
        self._set_timeout()

        while self.fp.tell() < self.total_length:
            for chunk_cls in self.__class__.ChunkClasses:
                if chunk_cls.matches(self.fp):
                    chunk = chunk_cls(self.fp, self)
                    chunk.populate()
                    self.chunks.append(chunk)
                    print chunk
                    break

            if self.is_timeout:
                raise ParseTimeoutException()

        self._timeout_timer.cancel()

    def _set_timeout(self):
        def handler():
            self.is_timeout = True

        self._timeout_timer = threading.Timer(self.__class__.Timeout, handler)
        self._timeout_timer.start()

    def close(self):
        self.fp.close()


class FileParser(Parser):
    def __init__(self, path):
        fp = open(path, 'rb')
        super(FileParser, self).__init__(fp)
