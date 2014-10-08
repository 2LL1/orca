# -*- coding: utf-8 -*-  

from datetime import date as Date

#Please turn it on in debug mode
DEBUG = False

#Base folder for all databases. Should been created before execute.
DB_PATH = r"db"

CACHE_PATH = r"cache"

# Tune for performance
DB_PRAGMA = """
PRAGMA cache_size = 160000;
PRAGMA journal_mode = OFF;
"""

DB_PRAGMA = ""

K05_DATA_FOLDER = 'raw_data/5min'
K01_DATA_FOLDER = 'raw_data/1min'

KDAY_SOURCE = 'jydb/jydb@jydb'

NLS_LANG = 'AMERICAN_AMERICA.UTF8'

REFRESH_HINTS = {
	'S05': K05_DATA_FOLDER,
	'I05': K05_DATA_FOLDER,
	'S01': K01_DATA_FOLDER,
	'I01': K01_DATA_FOLDER,
	'SDAY': KDAY_SOURCE
}

FRAME_DIRECTION = ['stock', 'stamp'] # Swap it if you want to use timestamp as columns


DATE_0 = Date(2000, 1, 1)
