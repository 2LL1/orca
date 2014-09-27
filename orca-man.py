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
	parse_logging_pargument(args)
	o = ocean(args.ocean_name)
	o.create(args.ocean_name)
	o.init_db(args.hints)


parser = ArgumentParser(prog="orca-man")
parser.add_argument('--logging-filename', help='set the name of log file', default='orca-man.log')
parser.add_argument('--logging-level', help='set the level of logging', default='INFO', choices='DEBUG INFO '.split())
parser.add_argument('--logging-format', help='set the format of logging', default='%(levelname)s: [%(asctime)s] %(message)s')
parser.add_argument('--logging-datefmt', help='set the format of logging date format', default='%Y/%m/%d %I:%M:%S %p')
parser.add_argument('--logging-filemode', help='set the open mode of logfile', default='a')


subparsers = parser.add_subparsers(help="Database operations")

parser_init_db = subparsers.add_parser('init_db', help='Initialize an ocean')
parser_init_db.add_argument('ocean_name')
parser_init_db.add_argument('hints')
parser_init_db.set_defaults(func=init_db)

parser_refresh = subparsers.add_parser('refresh', help='Refresh an ocean')
parser_refresh.add_argument('ocean_name')
parser_refresh.add_argument('hints')


if __name__ == '__main__':
	args = parser.parse_args()
	args.func(args)
	
