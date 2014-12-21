import abc
import pandas
import numpy


class BasicFish(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args):
        pass

    @property
    def delta(self):
        """How many days will be wasted."""
        return 0

    @abc.abstractproperty
    def nargs(self):
        """return number of arguments required for this operation"""
        raise NotImplementedError()

    @abc.abstractmethod
    def operate(self, *args): 
        """Abstarct method to do some operation. """
        raise NotImplementedError()

    def yaha(self, stack):
        args = [stack.pop() for _ in range(self.nargs)]
        v = self.operate(*args)
        stack.append(v)

class FishOp0(BasicFish):
    @property
    def nargs(self):
        """return number of arguments required for this operation"""
        return 0

class FishConstant(FisoOp0):
    def __init__(self, v):
        self.__val = v

    def operate(self): 
        return self.__val

class FishOp1(BasicFish):
    @property
    def nargs(self):
        """return number of arguments required for this operation"""
        return 1

class FishNegitive(FishOp1):
    def operate(self, v): 
        return -v

class FishRollingMean(FishOp1):
    def __init__(self, n):
        assert n > 0
        self.__n = n

    @property
    def delta(self):
        return n

    def operate(self, v): 
        return v.rolling_mean(v, self.__n)

class FishOp2(FishOperation):
    @property
    def nargs(self):
        """return number of arguments required for this operation"""
        return 2

class FishAdd(FishOp2):
    def operate(self, v1, v2): 
        return v1+v2

class FishSub(FishOp2):
    def operate(self, v1, v2): 
        return v1-v2

class FishMul(FishOp2):
    def operate(self, v1, v2): 
        return v1*v2

class FishDiv(FishOp2):
    def operate(self, v1, v2): 
        return v1/v2

class FishPow(FishOp2):
    def operate(self, v1, v2): 
        return pow(v1, v2)

class FishOp3(FishOperation):
    @property
    def nargs(self):
        """return number of arguments required for this operation"""
        return 3

