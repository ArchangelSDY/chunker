import os
import threading


class ParseTimeoutException(Exception):
    pass


class Parser:
    ChunkClasses = ()
    Timeout = 60

    def __init__(self, fp):
        self.fp = fp
        self.total_length = Parser.get_total_length(fp)
        self.chunks = []
        self._timeout_timer = None
        self.is_timeout = False

    @staticmethod
    def get_total_length(fp):
        return os.fstat(fp.fileno()).st_size

    def parse(self):
        self._set_timeout()

        while self.fp.tell() < self.total_length:
            for chunk_cls in self.__class__.ChunkClasses:
                if chunk_cls.matches(self.fp):
                    chunk = chunk_cls(self.fp)
                    self.chunks.append(chunk)
                    break

            if self.is_timeout:
                raise ParseTimeoutException()

        self._timeout_timer.cancel()

    def _set_timeout(self):
        def handler():
            self.is_timeout = True

        self._timeout_timer = threading.Timer(self.__class__.Timeout, handler)
        self._timeout_timer.start()
