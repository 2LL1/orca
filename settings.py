# -*- coding: utf-8 -*-  

#Please turn it on in debug mode
DEBUG = False

#Base folder for all databases. Should been created before execute.
DB_PATH = r"db"

# Tune for performance
DB_PRAGMA = """
PRAGMA cache_size = 160000;
PRAGMA journal_mode = OFF;
"""

K05_DATA_FOLDER = 'raw_data/5min'

NLS_LANG = 'AMERICAN_AMERICA.UTF8'
JYDB_CONNECTION = 'jydb/jydb@jydb'

REFRESH_HINTS = {
	'K05_S': K05_DATA_FOLDER,
	'K05_I': K05_DATA_FOLDER,
}

FRAME_DIRECTION = ['stock', 'stamp'] # Swap it if you want to use timestamp as columns


DATE_0 = 200001010000
