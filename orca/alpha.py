import abc

import pandas
import numpy

class BasicAlpha(object):
	"""Basic class for all Alpha"""
	__metaclass__ = abc.ABCMeta

	def __int__(self):
		pass

	@abc.abstractmethod
	def generate(self, date1, date2, args):
		"""Generate a set of alpha between [date1, date2)."""
		raise NotImplementedError()

	@abc.abstractproperty
	def delta(self):
		"""Return a number of days to indicate how many days you need in generatation 
		"""
		raise NotImplementedError()

	@abc.abstractproperty
	def required_data(self):
		"""Return a list of labels for ocean to get data.""" 
		raise ['sid', 'date']


class AlphaRandom(BasicAlpha):
	def __init__(self):
		pass

	def generate(self, date1, data2, args):
		date = args['date']
		sid = args['sid']
		rows = len(dates)
		cols = len(sid)
		return DataFrame(numpy.random.random((rows, cols)), dates, sid)

	@property
	def delta(self):
		return 0

	@property
	def required_data(self):
		return super(AlphaRandom, self).required_data

class AlphaRollingMean(BasicAlpha):
	def __init__(self, n, key):
		self.__delta = n
		self.__key = key

	def generate(self, date1, data2, args):
		frame = args[self.__key]
		result = pandas.rolling_mean(frame, self.__delta)[self.delta:] 
		result /= frame[self.delta:]
		return result - 1

	@property
	def delta(self):
		return self.__delta

	@property
	def required_data(self):
		return super(AlphaRandom, self).required_data + [self.__key]


class AlphaFishes(BasicAlpha):
	def __init__(self, ops, stack):
		self.__delta = n
		self.__key = key

	def generate(self, date1, data2, args):
		frame = args[self.__key]
		result = pandas.rolling_mean(frame, self.__delta)[self.delta:] 
		result /= frame[self.delta:]
		return result - 1
