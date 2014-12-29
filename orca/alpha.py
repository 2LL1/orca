from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import abc

import pandas
import numpy

class BasicAlpha(object):
    """Basic class for all Alpha"""
    __metaclass__ = abc.ABCMeta

    def __int__(self):
        pass

    @abc.abstractmethod
    def generate_n(self, date1, date2):
        """Generate a set of alpha between [date1, date2)."""
        raise NotImplementedError()

    def generate_1(self, date1):
        return self.generate_n(date1, date1+1)

class AlphaRandom(BasicAlpha):
    def __init__(self):
        pass

    def generate_n(self, date1, data2):
        date = args['date']
        sid = args['sid']
        rows = len(dates)
        cols = len(sid)
        return DataFrame(numpy.random.random((rows, cols)), dates, sid)
