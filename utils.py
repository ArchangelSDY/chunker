import os


class OffsetFilePtr(object):
    def __init__(self, fp, offset, total_length):
        self.fp = fp
        self.offset = offset
        self.total_length = total_length

    def read(self, n):
        return self.fp.read(n)

    def seek(self, pos, mode):
        if mode == os.SEEK_CUR:
            self.fp.seek(pos, os.SEEK_CUR)
        elif mode == os.SEEK_SET:
            self.fp.seek(self.offset + pos, os.SEEK_SET)
        elif mode == os.SEEK_END:
            self.fp.seek(self.offset + self.total_length + pos, os.SEEK_SET)

    def tell(self):
        return self.fp.tell() - self.offset

    def close(self):
        self.fp = None
        self.offset = 0
        self.total_length = 0
