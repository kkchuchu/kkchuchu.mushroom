import abc
import argparse


class Runnable():
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, arguments):
        self._arguments = arguments

    @abc.abstractmethod
    def producer(self):
        pass
    @abc.abstractmethod
    def consumer(self):
        pass

class ArgumentHandler(object):
    def __init__(self, *args, **kwargs):
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('producer_consumer', help='This is a producer or a consumer')
    
    def _parseargs(self):
        self.arguments = self._parser.parse_args()

