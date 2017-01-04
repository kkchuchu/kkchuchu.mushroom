from abc import ABCMeta

class Sink(object):
    def __init__(self):
        self.sep = ','
    def add(self, row):
        pass


class ToCommaCsv(Sink):
    def __init__(self, file_path):
        super().__init__()
        self.__file_path = file_path
        self.__fp = open(file_path, 'w+')

    def add(self, row):
        print(*row, sep=self.sep, file=self.__fp)

    def __del__(self):
        self.__fp.close()
