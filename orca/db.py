# -*- coding: utf-8 -*-  
"""
Databases
by madlee @ 2014.09.19
"""

import sqlite3
import csv
import logging

import numpy
from pandas import read_sql, read_pickle

import settings
from orca.tools import *

logger = logging.getLogger('orca.db')

SQL_CREATE_OCEAN = """CREATE TABLE IF NOT EXISTS T_%(name)s ( 
    %(columns)s, 
    PRIMARY KEY (%(primary_keys)s)
);
CREATE INDEX IF NOT EXISTS I_%(name)s_%(fields_name)s ON T_%(name)s (%(fields)s);
""".split(';')

SQL_INSERT_OCEAN = """INSERT INTO %(table_name)s
    (%(columns)s) VALUES (%(questions)s)
"""

SQL_GET_VALUE_D = """SELECT stock, date, date*10000 AS stamp, %(value_name)s 
    FROM %(table_name)s
    %(where)s
"""

SQL_GET_VALUE_DT = """SELECT stock, date, time, date*10000+time AS stamp, %(value_name)s 
    FROM %(table_name)s
    %(where)s
"""

SQL_COUNT_STOCK = """SELECT COUNT(DISTINCT stock)
    FROM %(table_name)s
    %(where)s
"""

SQL_COUNT_DATE = """SELECT COUNT(DISTINCT date) 
    FROM %(table_name)s
    %(where)s
"""

SQL_COUNT_TIME = """SELECT COUNT(DISTINCT time) 
    FROM %(table_name)s
    %(where)s
"""


SQL_MAX_DATE = """SELECT MAX(date) 
    FROM %(table_name)s
    %(where)s
"""

SQL_SELECT_KDAY_STOCK_FROM_ORACLE = """SELECT SecuCode, TradingDay, PrevClosePrice, OpenPrice, HighPrice, LowPrice, ClosePrice, TurnoverVolume, TurnoverValue, TurnoverDeals
    FROM SecuMain INNER JOIN QT_DailyQuote ON SecuMain.InnerCode = QT_DailyQuote.InnerCode
    WHERE (secumarket = 83 AND SecuCode LIKE '60%%' OR secumarket = 90 AND SecuCode LIKE '30%%' OR secumarket = 90 AND SecuCode LIKE '00%%')
        AND TradingDay = to_date('%s', 'yyyy-mm-dd') 
    ORDER BY SecuCode
"""

class OceanManager(object):
    def __init__(self):
        self.__pool = {}

    def __setitem__(self, name, cls_ocean):
        self.__pool[name] = cls_ocean

    def __getitem__(self, name):
        result = self.__pool[name]
        try:
            result = result[0](name, *result[1:])
            self.__pool[name] = result
        except TypeError as e:
            pass

        return result

ocean_man = OceanManager()

def ocean(name):
    """A shortcut to get an instance of ocean with specified name. """
    return ocean_man[name]

def _build_sql_where(**args):
    """Build where clause to limit the sql result"""
    where, parameters = [], []
    date1 = args.get('date1', None)
    if date1:
        where.append('date >= ?')
        parameters.append(date1)

    date2 = args.get('date2', None)
    if date2:
        where.append('date < ?')
        parameters.append(date2)

    date_in = args.get('date_in', None)
    if date_in:
        v = list(date_in)
        parameters += v
        where.append('date IN (%s)' % ','.join('?'*len(v)))

    time1 = args.get('time1', None)
    if time1:
        where.append('time >= ?')
        parameters.append(time1)

    time2 = args.get('time2', None)
    if time2:
        where.append('time < ?')
        parameters.append(time2)

    time_in = args.get('time_in', None)
    if time_in:
        v = list(time_in)
        parameters += v
        where.append('time IN (%s)' % ','.join('?'*len(v)))

    if where:
        where = 'WHERE ' + ' AND '.join(where)
        return where, parameters
    else:
        return '', []

class BasicOcean(object):
    """The base class for all stock databases"""

    def __init__(self, name, fields):
        """Init the ocean with the path to the db file and the name of the table or view"""
        path = join_path(settings.DB_PATH, name + '.db')
        self.__conn = sqlite3.connect(path)
        self.__name = name
        self.__table = 'T_%s' % name
        self.__fields = fields
        self.execute_sqls(settings.DB_PRAGMA)

    @property
    def name(self):
        return self.__name

    @property
    def conn(self):
        """return the connection of this database"""
        return self.__conn

    @property
    def fields(self):
        return self.__fields

    def commit(self):
        """commit changes"""
        self.__conn.commit()

    def execute_sqls(self, sqls, cursor=None):
        """execute a set of sqls"""
        if cursor == None:
            cursor = self.conn.cursor()
        
        for i in sqls.split(';'):
            i = i.strip()
            if i:
                logger.debug('Execute SQL %s', i)
                cursor.execute(i)

        return cursor

    def create(self, name):
        """Create the database"""
        cursor = self.conn.cursor()

        column_names = self.PRIMARY_KEY + self.fields
        column_types = ["INTEGER"]*len(self.PRIMARY_KEY) + ["FLOAT"] * len(self.fields)
        columns = ','.join(['%s %s' % (i, j) for i, j in zip(column_names, column_types)])
        sql = SQL_CREATE_OCEAN[0] % {'name': name, 'columns': columns, 'primary_keys': ','.join(self.PRIMARY_KEY)}
        logger.debug('Execute SQL %s', sql)
        cursor.execute(sql)

        for fields in self.INDEXES:
            fields = fields.split()
            sql = SQL_CREATE_OCEAN[1] % {'name': name, 'fields': ', '.join(fields), 'fields_name': '_'.join(fields)}
            logger.debug('Execute SQL %s', sql)
            cursor.execute(sql)

        self.commit()
        del cursor

    def _count_by_sql(self, sql, cursor=None, **kwargs):
        where, params = _build_sql_where(**kwargs)
        sql %= {'table_name':self.__table, 'where': where}
        if cursor == None:
            cursor = self.conn.cursor()
        logger.debug('Execute SQL %s', sql)
        cursor.execute(sql, params)
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0

    def max_date(self, cursor=None, **kwargs):
        return self._count_by_sql(SQL_MAX_DATE, cursor, **kwargs)

    def count_date(self, cursor=None, **kwargs):
        """Count the stamp points between [day1, day2)"""
        return self._count_by_sql(SQL_COUNT_DATE, cursor, **kwargs)
        
    def count_stock(self, cursor=None, **kwargs):
        """Count the stock points between [day1, day2)"""
        return self._count_by_sql(SQL_COUNT_STOCK, cursor, **kwargs)

    def count_time(self, cursor=None, **kwargs):
        """Count the stock points between [day1, day2)"""
        return self._count_by_sql(SQL_COUNT_TIME, cursor, **kwargs)

    def stack(self, names, cursor=None, **kwargs):
        try:
            names = names.split()
        except AttributeError:
            pass

        for name in names:
            if name not in self.fields:
                raise KeyError('%s is not a field.', name)

        where, params = _build_sql_where(**kwargs)
        sql = self.SQL_GET_VALUE % {'value_name': ','.join(names), 'table_name':self.__table, 'where': where}
        logger.debug('Start load SQL Data %s', sql)
        t1 = Timer()
        result = read_sql(sql, self.conn, params=params)
        logger.debug('Loaded %d rows in %s', len(result), t1)
        return result
        

    def frames(self, names, cursor=None, **kwargs):
        """return a value frame between [day1, day2). 
            name: The column name of the value"""

        try:
            names = names.split()
        except AttributeError:
            pass
        
        stacks = self.stack(names, cursor, **kwargs)
        logger.debug('Start Pivot stacks')
        t1 = Timer()
        result = {}
        for i in names:
            result[i] = stacks.pivot(settings.FRAME_DIRECTION[0], settings.FRAME_DIRECTION[1], i)
            if settings.FRAME_DIRECTION[0] == 'stock':
                result[i].index = numpy.char.mod('%06d', result[i].index)
            if settings.FRAME_DIRECTION[1] == 'stock':
                result[i].columns = numpy.char.mod('%06d', result[i].columns)

        logger.debug('Finished pivoting in %s', t1)
        
        return result

    def push_rows(self, rows, cursor=None):
        if cursor == None:
            cursor = self.conn.cursor()
        vars = {
            'table_name': self.__table, 
            'columns': ','.join(self.PRIMARY_KEY + self.fields), 
            'questions': ','.join('?'*(len(self.fields)+len(self.PRIMARY_KEY)))
        }
        sql = SQL_INSERT_OCEAN % vars
        logger.debug('Execute SQL %s', sql)
        cursor.executemany(sql, rows)

    def save_cache(self, fields, cursor=None, **kwargs):
        logger.info('Loading data from ocean %s to create cache.', self.name)
        timer = Timer()

        frames = self.frames(fields, cursor, **kwargs)
        output = kwargs.get('output', self.name)
        for k, v in frames.iteritems():
            logger.info('Saving cache %s.%s', output, k)
            filename = join_path(settings.CACHE_PATH, output+'.'+k)
            v.to_pickle(filename)
        logger.info('%d cache(s) were saved in %s.', len(frames), timer)


def load_cache(name):
    fullname = join_path(settings.CACHE_PATH, name)
    return read_pickle(fullname)


class BasicOceanD(BasicOcean):
    """Ocean with date only."""
    PRIMARY_KEY = ['stock', 'date']
    INDEXES = {'date'}
    SQL_GET_VALUE = SQL_GET_VALUE_D


class BasicOceanDT(BasicOcean):
    """Ocean with date and time."""
    PRIMARY_KEY = ['stock', 'date', 'time']
    INDEXES = ['date', 'time', 'date time', 'stock time']
    SQL_GET_VALUE = SQL_GET_VALUE_DT


class MixinFromCSV(object):
    """Original data was saved in CSV file."""

    def import_csv(self, filename):
        """Import a csv file"""        
        with open(filename, 'rb') as reader:
            logger.info('Importing file %s', filename)
            timer = Timer()
            reader = csv.reader(reader)
            titles = reader.next()

            all_records = []

            for row in reader:
                row = self.uniform(row, titles)
                if row:
                    all_records.append(row)

            self.push_rows(all_records)
            self.commit()
            result = len(all_records)
            logger.info('Imported %d rows in %s', result, timer)
            return result

    def init_db(self, folder):
        """Refresh the source folder to check in new data"""
        logger.info('Began to initialize database %s', self.name)
        fileset = list_dir(folder)
        fileset.sort()
        for filename in fileset:
            if filename.endswith('.csv'):
                full_path = join_path(folder, filename)
                self.import_csv(full_path)                
        logger.info('Finished of initialization database %s', self.name)

    
    def refresh(self, folder):
        """Refresh the source folder to check in new data"""
        logger.info('Began to refresh database %s', self.name)
        date = self.max_date()
        date = Date(date/10000, date % 10000 / 100, date % 100) + ONE_DAY
        today = Date.today()
        while date < today:
            filename = date.strftime('%Y-%m-%d.csv')
            full_path = join_path(folder, filename)
            if is_file(full_path):
                self.import_csv(full_path)
            date +=  ONE_DAY
        logger.info('Finished of refreshing database %s', self.name)

class OceanKmin(BasicOceanDT, MixinFromCSV):
    COLUMN_NAMES = "price   open    close   high    low     vol     amount  cjbs    yclose  syl1    syl2    buy1    buy2    buy3    buy4    buy5    sale1   sale2   sale3   sale4   sale5   bc1     bc2     bc3     bc4     bc5     sc1     sc2     sc3     sc4     sc5     wb      lb      zmm     buy_vol buy_amount  sale_vol    sale_amount w_buy   w_sale  sectional_buy_vol   sectional_buy_amount    sectional_sale_vol  sectional_sale_amount   sectional_w_buy sectional_w_sale    sectional_yclose    sectional_open  sectional_close sectional_high  sectional_low   sectional_vol   sectional_amount    sectional_cjbs  sectional_wb".split()

    def __init__(self, name, filter):
        BasicOceanDT.__init__(self, name, OceanKmin.COLUMN_NAMES)
        self.__filter = filter

    def uniform(self, row, titles):
        if self.__filter(row[0]):
            stock = int(row[0][2:])
            stamp = DateTime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
            date = stamp.year*10000 + stamp.month*100 + stamp.day
            time = stamp.hour * 100 + stamp.minute
            return [stock, date, time] + [float(i) for i in row[3:]]
        else:
            return None

is_stock = lambda token: token[:4] in {'SH60', 'SZ30', 'SZ00'}
is_index = lambda token: not is_stock(token)

ocean_man['S05'] = OceanKmin, is_stock
ocean_man['I05'] = OceanKmin, is_index

ocean_man['S01'] = OceanKmin, is_stock
ocean_man['I01'] = OceanKmin, is_index


class MixinFromOracle(object):
    def __init__(self, sql):
        self.SQL_SOURCE = sql

    def import_query(self, sql, cursor, date):
        logger.info('Importing records on %s', date)
        t1 = Timer()
        all_records = []

        sql = sql % date.strftime('%Y-%m-%d')

        for row in cursor.execute(sql):
            row = self.uniform(row)
            if row:
                all_records.append(row)

        self.push_rows(all_records)
        self.commit()
        result = len(all_records)
        logger.info('Imported %d rows in %s', result, t1)
        return result

    def init_db(self, conn_string):
        self.refresh(conn_string)
        
    def refresh(self, conn_string):
        """Refresh the source database to check in new data"""
        import cx_Oracle
        import os

        logger.info('Began to refresh database %s.', self.name)        
        os.environ['NLS_LANG'] = settings.NLS_LANG
        conn = cx_Oracle.connect(conn_string)
        cursor = conn.cursor()

        t1 = self.max_date()
        if t1 == None:
            t1 = settings.DATE_0
        else:
            t1 = Date(t1 / 10000, t1 % 10000 / 100, t1 % 100) + ONE_DAY

        t2 = Date.today()
        while t1 < t2:
            self.import_query(self.SQL_SOURCE, cursor, t1)
            t1 += ONE_DAY
            
        logger.info('Finished of refreshing database %s', self.name)

class OceanKDay(BasicOceanD, MixinFromOracle):
    COLUMN_NAMES = "prev_close open high low close volume value deals".split()

    def __init__(self, name, sql):
        BasicOceanD.__init__(self, name, OceanKDay.COLUMN_NAMES)
        MixinFromOracle.__init__(self, sql)

    def uniform(self, row):
        row = list(row)
        row[0] = int(row[0])
        row[1] = row[1].year * 10000 + row[1].month*100 + row[1].day
        return row

ocean_man['SDAY'] = OceanKDay, SQL_SELECT_KDAY_STOCK_FROM_ORACLE

