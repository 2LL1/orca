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

