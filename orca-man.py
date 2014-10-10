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

logger = logging.getLogger('main')

def parse_logging_pargument(args):
	pars = {}
	for k, v in vars(args).iteritems():
		if k == 'logging_level':
			pars['level'] = getattr(logging, v.upper())
		elif k.startswith('logging_'): 
			pars[k[8:]] = v

	logging.basicConfig(**pars)

def init_db(args):
	o = ocean(args.ocean_name)
	o.create(args.ocean_name)
	o.init_db(args.hints)

def refresh(args):
	o = ocean(args.ocean_name)
	o.refresh(args.hints)

def create_cache(args):
	o = ocean(args.ocean_name)
	par = {} 
	for k, v  in vars(args).iteritems():
		if k.startswith('logging_'):
			pass
		elif k == 'fields':
			pass
		elif k == 'ocean_name':
			pass
		elif k == 'func':
			pass
		else:
			par[k] = v
	o.save_cache(args.fields, None, **par)

LOGGING_LEVELS ='DEBUG INFO WARNING ERROR CRITICAL'.split()
parser = ArgumentParser(prog="orca-man")
parser.add_argument('--logging-filename', help='set the name of log file', default='orca-man.log')
parser.add_argument('--logging-level', help='set the level of logging', default='INFO', choices=LOGGING_LEVELS)
parser.add_argument('--logging-format', help='set the format of logging', default='%(levelname)s: [%(asctime)s] %(message)s')
parser.add_argument('--logging-datefmt', help='set the format of logging date format', default='%Y/%m/%d %I:%M:%S %p')
parser.add_argument('--logging-filemode', help='set the open mode of logfile', default='a')


db_parsers = parser.add_subparsers(help="Database operations")

parser_init_db = db_parsers.add_parser('init_db', help='Initialize an ocean')
parser_init_db.add_argument('ocean_name', help='The name of the ocean')
parser_init_db.add_argument('hints', help="hint for Initialization")
parser_init_db.set_defaults(func=init_db)

parser_refresh = db_parsers.add_parser('refresh', help='Refresh an ocean')
parser_refresh.add_argument('ocean_name', help='The name of the ocean')
parser_refresh.add_argument('hints', help="hint for refreshing")
parser_refresh.set_defaults(func=refresh)

parser_cache = db_parsers.add_parser('cache', help='Generate cache')
parser_cache.add_argument('ocean_name', help='The name of the ocean')
parser_cache.add_argument('fields', nargs='+', help='Fields to save into cache')
parser_cache.add_argument('--date1', type=int)
parser_cache.add_argument('--date2', type=int)
parser_cache.add_argument('--date-in', type=int, nargs='*')
parser_cache.add_argument('--time1', type=int)
parser_cache.add_argument('--time2', type=int)
parser_cache.add_argument('--time-in', type=int, nargs='*')
parser_cache.add_argument('--output')
parser_cache.set_defaults(func=create_cache)


if __name__ == '__main__':
	args = parser.parse_args()
	parse_logging_pargument(args)
	try:
		args.func(args)
	except Exception as e:
		logger.error('Unexpect %s happend. It said: %s', type(e), e)
		raise
	
