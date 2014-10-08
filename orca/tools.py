# -*- coding: utf-8 -*-  
""" misc functions and types
 by madlee @ 2014.09.19
"""


from os import listdir as list_dir
from os.path import join as join_path, split as split_path, isfile as is_file, isdir as is_dir
from datetime import date as Date, datetime as DateTime, timedelta as TimeDelta

import re
import types

DIGITS = re.compile(r'\d+')
ONE_DAY = TimeDelta(1)

def timestamp(t):
    tt = type(t)
    if tt is Date:
        return DateTime(t.year, t.month, t.day, 0, 0, 0)
    if tt is DateTime:
        return t

    tokens = None
    if tt is types.StringType:
        tokens = DIGITS.findall(t)
        if tokens:
            tokens = [int(i) for i in tokens]
            if len(tokens) == 1:
                t = int(t)
                tt = types.IntType
            elif len(tokens) == 2:
                raise ValueError('Cannot convert %s to DateTime' % t)
 
    if tt is types.IntType:
        tokens = []
        while t > 0:
            tokens.append(t % 100)
            t /= 100
        tokens.reverse()

    try:
        if tokens:
            if tokens[0] < 90:
                tokens[0] += 2000
            elif tokens[0] < 100:
                tokens[0] += 1900

            return DateTime(*tokens)
    except:
        pass
        
    raise ValueError('Cannot convert %s to DateTime' % t)


class Timer(object):
    def __init__(self):
        self.reset()
    
    def __str__(self):
        return str(self.delta)

    @property
    def delta(self):
        return DateTime.now() - self.__start

    def reset(self):
        self.__start = DateTime.now()