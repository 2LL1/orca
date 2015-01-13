#! /bin/env python
# -*- coding: utf-8 -*-  

"""
Usages:
    %(command)s command args ....
    If you do not know how to use a command, please use 
    %(command)s help command for help messages.
"""

import sys
import logging
from argparse import ArgumentParser

from orca.db import ocean
from orca.tools import *

import settings

logger = logging.getLogger('orcaman')

def parse_logging_pargument(args):
	pars = {}
	for k, v in vars(args).iteritems():
		if k == 'logging_level':
			pars['level'] = getattr(logging, v.upper())
		elif k.startswith('logging_'): 
			pars[k[8:]] = v

	logging.basicConfig(**pars)

LOGGING_LEVELS ='DEBUG INFO WARNING ERROR CRITICAL'.split()
parser = ArgumentParser(prog="orca-man")
parser.add_argument('--logging-filename', help='set the name of log file', default='orca-man.log')
parser.add_argument('--logging-level', help='set the level of logging', default='INFO', choices=LOGGING_LEVELS)
parser.add_argument('--logging-format', help='set the format of logging', default='%(levelname)s: [%(asctime)s] %(message)s')
parser.add_argument('--logging-datefmt', help='set the format of logging date format', default='%Y/%m/%d %I:%M:%S %p')
parser.add_argument('--logging-filemode', help='set the open mode of logfile', default='a')


if __name__ == '__main__':
	args = parser.parse_args()
	parse_logging_pargument(args)
	try:
		args.func(args)
	except Exception as e:
		logger.error('Unexpect %s happend. It said: %s', type(e), e)
		raise
	