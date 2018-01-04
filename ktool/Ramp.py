import sys

import pandas
import numpy


class Ramp(object):
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__fp = open(file_path, 'r')

    def stream(self, batchsize=1):
        # Use pandas read csv method, may cause slow performance?
        return pandas.read_csv(self.__file_path, iterator=True, chunksize=batchsize)

    def sample(self, nrows = 10):
        return pandas.read_csv(self.__file_path, nrows=nrows)

    def stream_raw(self):
        return numpy.genfromtxt(self.__file_path, dtype=float, delimiter=',', names=True)

    def __del__(self):
        self.__fp.close()
