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

K05_DATA_FOLDER = 'raw_data/5min'
K01_DATA_FOLDER = 'raw_data/1min'

NLS_LANG = 'AMERICAN_AMERICA.UTF8'

REFRESH_HINTS = {
	'K05S': K05_DATA_FOLDER,
	'K05I': K05_DATA_FOLDER,
	'K01S': K01_DATA_FOLDER,
	'K01I': K01_DATA_FOLDER,
}

FRAME_DIRECTION = ['stock', 'stamp'] # Swap it if you want to use timestamp as columns


DATE_0 = Date(2000, 1, 1)
