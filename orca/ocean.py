# -*- coding: utf-8 -*-  

from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

"""
Databases
by madlee @ 2014.09.19
"""

import abc

import sqlite3
import csv
import logging

import numpy
from pandas import read_sql, read_pickle
from pandas.tools.pivot import pivot_table

from django.conf import settings
from orca.tools import *

logger = logging.getLogger('orca.ocean')

SQL_CREATE_OCEAN_ST = """CREATE TABLE IF NOT EXISTS T_%(name)s ( 
    %(columns)s, 
    PRIMARY KEY (%(primary_keys)s)
);
CREATE INDEX IF NOT EXISTS I_%(name)s_%(fields_name)s ON T_%(name)s (%(fields)s);
""".split(';')

SQL_INSERT_OCEAN_ST = """INSERT INTO %(table_name)s
    (%(columns)s) VALUES (%(questions)s)
"""

SQL_GET_VALUE_D = """SELECT stock, date, %(value_name)s 
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

SQL_SELECT_DAYS = """SELECT DISTINCT date 
    FROM %(table_name)s
    %(where)s
    ORDER BY date
"""

SQL_MIN_DATE = """SELECT MIN(date) 
    FROM %(table_name)s
    %(where)s
"""

SQL_MAX_DATE = """SELECT MAX(date) 
    FROM %(table_name)s
    %(where)s
"""

SQL_SELECT_KDAY_STOCK_FROM_ORACLE = """SELECT TradingDay, SecuCode, OpenPrice, HighPrice, LowPrice, ClosePrice, TurnoverVolume, TurnoverValue, TurnoverDeals
    FROM SecuMain INNER JOIN QT_DailyQuote ON SecuMain.InnerCode = QT_DailyQuote.InnerCode
    WHERE (secumarket = 83 AND SecuCode LIKE '60%%' OR secumarket = 90 AND SecuCode LIKE '30%%' OR secumarket = 90 AND SecuCode LIKE '00%%')
        AND TradingDay = to_date('%s', 'yyyy-mm-dd') 
    ORDER BY SecuCode
"""

SQL_SELECT_SHIFT_DATE = ["""SELECT DISTINCT date FROM %(table_name)s
    WHERE date < ?
    ORDER BY date DESC
""",

"""SELECT DISTINCT date FROM %(table_name)s
    WHERE date > ?
    ORDER BY date
"""]

SQL_GET_ALPHA = """SELECT date, stock, value 
    FROM T_ALPHA
    %(where)s 
"""

SQL_RESET_ALPHA = """DELETE FROM T_ALPHA
    WHERE alpha_id = ?
"""

SQL_DELETE_ALPHA_ITEMS = """DELETE FROM T_ALPHA
    WHERE alpha_id = ? AND ? <= date AND date <= ? 
"""

SQL_INSERT_ALPHA_ITEMS = """INSERT INTO T_ALPHA
    (date, stock, value, alpha_id) 
    VALUES (?, ?, ?, ?)
"""

SQL_GET_UNIVERSE = """SELECT date, stock 
    FROM T_UNIVERSE
    %(where)s 
"""

SQL_RESET_UNIVERSE = """DELETE FROM T_UNIVERSE
    WHERE universe_id = ?
"""

SQL_DELETE_UNIVERSE_ITEMS = """DELETE FROM T_UNIVERSE
    WHERE universe_id=? AND date>=? AND date<=? 
"""

SQL_INSERT_UNIVERSE_ITEMS = """INSERT INTO T_UNIVERSE
    (date, stock, universe_id) 
    VALUES (?, ?, ?)
"""

SQL_CREATE_OCEAN_MINUTE = """CREATE TABLE IF NOT EXISTS T_%(name)s ( 
    id INTEGER PRIMARY KEY,
    time INTEGER,
    date INTEGER,
    stock INTEGER,
    CONSTRAINT unique_tds UNIQUE (time, date, stock)
);
CREATE TABLE IF NOT EXISTS T_%(field)s (
    id INTEGER PRIMARY KEY REFERENCES T_%(name)s (id),
    value FLOAT
)""".split(';')


SQL_INSERT_OCEAN_MINUTE = """SELECT MAX(id)+1
    FROM T_%(name)s;
INSERT INTO T_%(name)s
    (id, time, date, stock) VALUES (?, ?, ?, ?);
INSERT INTO T_%(field)s
    (id, value) VALUES (?, ?);
""".split(';')

SQL_GET_VALUE_MINUTE = """SELECT stock, date, %(value_name)s 
    FROM T_%(table_name)s
        %(from_tables)s
    %(where)s
"""

SQL_MIN_DATE_MINUTE = """SELECT date 
    FROM %(table_name)s
    WHERE id IN (
        SELECT MIN(id) 
        FROM %(table_name)s
        %(where)s
    )
"""

SQL_MAX_DATE_MINUTE = """SELECT date 
    FROM %(table_name)s
    WHERE id IN (
        SELECT MAX(id) 
        FROM %(table_name)s
        %(where)s
    )
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
        except TypeError as _:
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
        del args['date1']

    date2 = args.get('date2', None)
    if date2:
        where.append('date < ?')
        parameters.append(date2)
        del args['date2']

    for k, v in args.iteritems():
        where.append('%s = ?' % k)
        parameters.append(v)

    if where:
        where = 'WHERE ' + ' AND '.join(where)
        return where, parameters
    else:
        return '', []

class BasicOcean(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def stack(self, names, cursor=None, **kwargs):
        raise NotImplementedError()

class OceanSqlite3(BasicOcean):
    """The base class for all stock databases"""

    def __init__(self, name, fields):
        """Init the ocean with the path to the db file and the name of the table or view"""
        path = join_path(settings.ORCA_DB_PATH, name + '.db')
        self.__conn = sqlite3.connect(path)
        self.__name = name
        self.__table = 'T_%s' % name
        self.__fields = fields
        self.execute_sqls(settings.ORCA_DB_PRAGMA)

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

    def min_date(self, cursor=None, **kwargs):
        return self._count_by_sql(SQL_MIN_DATE, cursor, **kwargs)

    def max_date(self, cursor=None, **kwargs):
        return self._count_by_sql(SQL_MAX_DATE, cursor, **kwargs)

    def get_shift_date(self, date1, shift, cursor=None):
        if shift != 0:
            if shift > 0:
                sql = SQL_SELECT_SHIFT_DATE[0]
            else:
                sql = SQL_SELECT_SHIFT_DATE[1]
                shift = -shift

            sql %= {'table_name': self.__table}

            if cursor == None:
                cursor = self.conn.cursor()

            if cursor.execute(sql, (date1,)):
                rows = cursor.fetchmany(shift)
                date1 = rows[-1][0]

        return date1

    def count_date(self, cursor=None, **kwargs):
        """Count the stamp points between [day1, day2)"""
        return self._count_by_sql(SQL_COUNT_DATE, cursor, **kwargs)
        
    def count_stock(self, cursor=None, **kwargs):
        """Count the stock points between [day1, day2)"""
        return self._count_by_sql(SQL_COUNT_STOCK, cursor, **kwargs)

    def get_dates(self, cursor=None, **kwargs):
        sql = SQL_SELECT_DAYS
        where, params = _build_sql_where(**kwargs)
        sql %= {'table_name':self.__table, 'where': where}
        if cursor == None:
            cursor = self.conn.cursor()

        logger.debug('Start load SQL Data %s', sql)
        t1 = Timer()
        result = read_sql(sql, self.conn, params=params)
        logger.debug('Loaded %d rows in %s', len(result), t1)
        return result['date']

    def save_cache(self, fields, cursor=None, **kwargs):
        logger.info('Loading data from ocean %s to create cache.', self.name)
        timer = Timer()

        frames = self.frames(fields, cursor, **kwargs)
        output = kwargs.get('output', self.name)
        for k, v in frames.iteritems():
            logger.info('Saving cache %s.%s', output, k)
            filename = join_path(settings.ORCA_CACHE_PATH, output+'.'+k)
            v.to_pickle(filename)
        logger.info('%d cache(s) were saved in %s.', len(frames), timer)

def load_cache(name):
    fullname = join_path(settings.ORCA_CACHE_PATH, name)
    return read_pickle(fullname)

class OceanWithSingleTableOnly(OceanSqlite3):
    def create(self, name):
        """Create the database"""
        cursor = self.conn.cursor()

        column_names = self.PRIMARY_KEY + self.fields
        column_types = ["INTEGER"]*len(self.PRIMARY_KEY) + ["FLOAT"] * len(self.fields)
        columns = ','.join(['%s %s' % (i, j) for i, j in zip(column_names, column_types)])
        sql = SQL_CREATE_OCEAN_ST[0] % {'name': name, 'columns': columns, 'primary_keys': ','.join(self.PRIMARY_KEY)}
        logger.debug('Execute SQL %s', sql)
        cursor.execute(sql)

        for fields in self.INDEXES:
            fields = fields.split()
            sql = SQL_CREATE_OCEAN_ST[1] % {'name': name, 'fields': ', '.join(fields), 'fields_name': '_'.join(fields)}
            logger.debug('Execute SQL %s', sql)
            cursor.execute(sql)

        self.commit()
        del cursor

    def push_rows(self, rows, cursor=None):
        if cursor == None:
            cursor = self.conn.cursor()
        vars = {
            'table_name': self.__table, 
            'columns': ','.join(self.PRIMARY_KEY + self.fields), 
            'questions': ','.join('?'*(len(self.fields)+len(self.PRIMARY_KEY)))
        }
        sql = SQL_INSERT_OCEAN_ST % vars
        logger.debug('Execute SQL %s', sql)
        cursor.executemany(sql, rows)

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

    def frame(self, name, cursor=None, **kwargs):
        """return a value frame between [day1, day2). 
            name: The column name of the value"""

        stacks = self.stack(name, cursor, **kwargs)
        logger.debug('Start Pivot stacks')
        t1 = Timer()
        result = stacks.pivot('date', 'stock', name)
        result.columns = numpy.char.mod('%06d', result.columns)
        logger.debug('Finished pivoting in %s', t1)
        return result


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
        os.environ['NLS_LANG'] = settings.ORCA_NLS_LANG
        conn = cx_Oracle.connect(conn_string)
        cursor = conn.cursor()

        t1 = self.max_date()
        if t1 == None:
            t1 = settings.ORCA_DATE_0
        else:
            t1 = Date(t1 / 10000, t1 % 10000 / 100, t1 % 100) + ONE_DAY

        t2 = Date.today()
        while t1 < t2:
            self.import_query(self.SQL_SOURCE, cursor, t1)
            t1 += ONE_DAY
            
        logger.info('Finished of refreshing database %s', self.name)

class OceanKDay(OceanWithSingleTableOnly, MixinFromOracle):
    PRIMARY_KEY = ['date', 'stock', ]
    INDEXES = ['stock']
    SQL_GET_VALUE = SQL_GET_VALUE_D
    COLUMN_NAMES = "open high low close volume value deals".split()

    def __init__(self, name, sql):
        OceanWithSingleTableOnly.__init__(self, name, OceanKDay.COLUMN_NAMES)
        MixinFromOracle.__init__(self, sql)

    def uniform(self, row):
        row = list(row)
        row[0] = row[0].year * 10000 + row[0].month*100 + row[0].day
        row[1] = int(row[1])
        return row

ocean_man['SDAY'] = OceanKDay, SQL_SELECT_KDAY_STOCK_FROM_ORACLE


def get_shift_date(date1, shift):
    return ocean_man['SDAY'].get_shift_date(date1, shift)

def get_frame(hints, date1, date2, shift=0):
    hints = hints.split('.')
    o = ocean_man[hints[0]]
    date1 = get_shift_date(date1, shift)

    return o.frame(hints[1], *hints[2:], date1=date1, date2=date2)

def get_trading_days(date1, date2, window=None):
    return ocean_man['SDAY'].get_dates(date1=date1, date2=date2)

class OceanAlpha(OceanWithSingleTableOnly):
    """Ocean with date only."""
    PRIMARY_KEY = ['alpha_id', 'date', 'stock', ]
    INDEXES = ['alpha_id stock']
    COLUMN_NAMES = ['value']
    SQL_GET_VALUE = SQL_GET_ALPHA

    def __init__(self, name, *args):
        super(OceanAlpha, self).__init__(name, OceanAlpha.COLUMN_NAMES)

    def stack(self, id, cursor=None, **kwargs):
        if 'alpha_id' not in kwargs:
            kwargs['alpha_id'] = id
        else:
            assert id == 'value' or kwargs['alpha_id'] == id
        return super(OceanAlpha, self).stack('value', cursor, **kwargs)

    def frame(self, id, cursor=None, **kwargs):
        kwargs['alpha_id'] = id
        return super(OceanAlpha, self).frame('value', cursor, **kwargs)


    def reset(self, id, cursor=None):
        if cursor == None:
            cursor = self.conn.cursor()
        logger.info("Start Reset ALPHA-[%s]", id)
        t1 = Timer()
        cursor.execute(SQL_RESET_ALPHA, (id,))
        rowcount = cursor.rowcount
        self.conn.commit()
        logger.info("Reset ALPHA-[%s] in %s. %d record(s) were deleted.", id, t1, rowcount)

    def update(self, id, frame, cursor=None):
        if cursor == None:
            cursor = self.conn.cursor()
        logger.info("Start Update ALPHA-[%s]", id)

        days = frame.index
        if len(days):
            # Drop old values
            min_date = int(min(days))
            max_date = int(max(days))

            t1, t_all = Timer(), Timer()
            logger.info("Deleting records between [%s, %s]", min_date, max_date)
            cursor.execute(SQL_DELETE_ALPHA_ITEMS, (id, min_date, max_date))
            rowcount = cursor.rowcount
            logger.info("Deteled %d record(s) in %s", rowcount, t1)
            t1.reset()

        frame = frame.stack().reset_index()
        frame.columns = ['date', 'stock', 'value']
        frame['alpha_id'] = id

        data = [tuple(x) for x in frame.values]

        logger.info("Prepared %d data in %s", len(frame), t1)
        t1.reset()

        cursor.executemany(SQL_INSERT_ALPHA_ITEMS, data)
        self.conn.commit()
        logger.info("Inserted %d rows in %s", len(frame), t1)
        logger.info("Updated ALPHA-[%s] in %s", id, t_all)

ocean_man['ALPHA'] = OceanAlpha, ''


class OceanUniverse(OceanWithSingleTableOnly):
    """Ocean with date only."""
    PRIMARY_KEY = ['universe_id', 'date', 'stock', ]
    INDEXES = ['universe_id stock']
    COLUMN_NAMES = []
    SQL_GET_VALUE = SQL_GET_UNIVERSE

    def __init__(self, name, *args):
        super(OceanUniverse, self).__init__(name, OceanUniverse.COLUMN_NAMES)

    def stack(self, id, cursor=None, **kwargs):
        kwargs['universe_id'] = id
        return super(OceanUniverse, self).stack('', cursor, **kwargs)

    def frame(self, id, cursor=None, **kwargs):
        stacks = self.stack(id, cursor, **kwargs)

        logger.debug('Start Pivot stacks')
        t1 = Timer()
        stacks['value'] = True
        result = pivot_table(stacks, 'value', 'date', 'stock', fill_value=False)
        result.columns = numpy.char.mod('%06d', result.columns)
        logger.debug('Finished pivoting in %s', t1)
        return result

    def reset(self, id, cursor=None):
        if cursor == None:
            cursor = self.conn.cursor()
        logger.info("Start Reset UNIVERSE-[%s]", id)
        t1 = Timer()
        cursor.execute(SQL_RESET_UNIVERSE, (id,))
        rowcount = cursor.rowcount
        self.conn.commit()
        logger.info("Reset UNIVERSE-[%s] in %s. %d record(s) were deleted.", id, t1, rowcount)

    def update(self, univ_id, frame, cursor=None):
        if cursor == None:
            cursor = self.conn.cursor()
        logger.info("Start Update UNIVERSE-[%s]", univ_id)

        days = frame.index
        if len(days):
            # Drop old values
            min_date = int(min(days))
            max_date = int(max(days))

            t1, t_all = Timer(), Timer()
            logger.info("Deleting records between [%s, %s]", min_date, max_date)

            cursor.execute(SQL_DELETE_UNIVERSE_ITEMS, (univ_id, min_date, max_date))
            rowcount = cursor.rowcount
            logger.info("Deteled %d record(s) in %s", rowcount, t1)
            t1.reset()

        frame = frame.stack().reset_index()
        frame.columns = ['date', 'stock', 'value']
        frame = frame[frame['value']] # Keep true value only.
        del frame['value']
        frame['universe_id'] = univ_id

        data = [tuple(x) for x in frame.values]

        logger.info("Prepared %d data in %s", len(frame), t1)
        t1.reset()

        cursor.executemany(SQL_INSERT_UNIVERSE_ITEMS, data)
        self.conn.commit()
        logger.info("Inserted %d rows in %s", len(frame), t1)
        logger.info("Updated UNIVERSE-[%s] in %s", id, t_all)

ocean_man['UNIVERSE'] = OceanUniverse, ''


class OceanKMinute(OceanSqlite3, MixinFromCSV):
    """Ocean with minute label"""

    COLUMN_NAMES = "price,open,close,high,low,vol,amount,cjbs,yclose,syl1,syl2,buy1,buy2,buy3,buy4,buy5,sale1,sale2,sale3,sale4,sale5,bc1,bc2,bc3,bc4,bc5,sc1,sc2,sc3,sc4,sc5,wb,lb,zmm,buy_vol,buy_amount,sale_vol,sale_amount,w_buy,w_sale".split(',')
    SQL_GET_VALUE = SQL_GET_VALUE_MINUTE

    def __init__(self, name, filter):
        OceanSqlite3.__init__(self, name, OceanKMinute.COLUMN_NAMES)
        self.__filter = filter
        
    def create(self, name):
        """Create the database"""
        cursor = self.conn.cursor()
        var = {'name': name}
        
        sql = SQL_CREATE_OCEAN_MINUTE[0] % var
        logger.debug('Execute SQL %s', sql)
        cursor.execute(sql)

        for i in self.fields:
            var['field'] = i
            sql = SQL_CREATE_OCEAN_MINUTE[1] % var
            logger.debug('Execute SQL %s', sql)
            cursor.execute(sql)

        self.commit()
        del cursor

    def push_rows(self, rows, cursor=None):
        if cursor == None:
            cursor = self.conn.cursor()

        var = {
            'name': self.name
        }
        sql = SQL_INSERT_OCEAN_MINUTE[0] % var
        logger.debug('Execute SQL %s', sql)
        cursor.execute(sql)
        id0 = cursor.fetchone()[0]
        if id0 == None:
            id0 = 1


        data = [(id0+i, row[0], row[1], row[2]) for i, row in enumerate(rows)]
        sql = SQL_INSERT_OCEAN_MINUTE[1] % var
        logger.debug('Execute SQL %s', sql)
        cursor.executemany(sql, data)

        
        for i, field in enumerate(self.fields):
            var['field'] = field
            data = [(j+id0, row[3+i]) for j, row in enumerate(rows)]
            sql = SQL_INSERT_OCEAN_MINUTE[2] % var
            logger.debug('Execute SQL %s', sql)
            cursor.executemany(sql, data)


    def uniform(self, row, titles):
        if self.__filter(row[0]):
            stock = int(row[0][2:])
            stamp = DateTime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
            date = stamp.year*10000 + stamp.month*100 + stamp.day
            time = stamp.hour * 100 + stamp.minute
            return [time, date, stock] + [float(i) for i in row[3:]]
        else:
            return None

    def stack(self, time, names, cursor=None, **kwargs):
        try:
            names = names.split()
        except AttributeError:
            pass

        for name in names:
            if name not in self.fields:
                raise KeyError('%s is not a field.', name)

        value_names = ["T_%s.value as %s" % (i, i) for i in names]
        from_tables = ["INNER JOIN T_%s ON T_%s.id=T_%s.id" % (i, self.name, i) for i in names]

        kwargs['time'] = time
        where, params = _build_sql_where(**kwargs)
        
        sql = self.SQL_GET_VALUE % {'table_name':self.name,
            'value_name': ','.join(value_names), 
            'from_tables': '\n'.join(from_tables),
            'where': where}
        logger.debug('Start load SQL Data %s', sql)
        t1 = Timer()
        result = read_sql(sql, self.conn, params=params)
        logger.debug('Loaded %d rows in %s', len(result), t1)
        return result

    def frame(self, time, name, cursor=None, **kwargs):
        # TODO: 
        """return a value frame between [day1, day2). 
            name: The column name of the value"""

        stacks = self.stack(time, name, cursor, **kwargs)
        logger.debug('Start Pivot stacks')
        t1 = Timer()
        result = stacks.pivot('date', 'stock', name)
        result.columns = numpy.char.mod('%06d', result.columns)
        logger.debug('Finished pivoting in %s', t1)
        return result

    def min_date(self, cursor=None, **kwargs):
        return self._count_by_sql(SQL_MIN_DATE_MINUTE, cursor, **kwargs)

    def max_date(self, cursor=None, **kwargs):
        return self._count_by_sql(SQL_MIN_DATE_MINUTE, cursor, **kwargs)

is_stock = lambda token: token[:4] in {'SH60', 'SZ30', 'SZ00'}
is_index = lambda token: not is_stock(token)

ocean_man['S30'] = OceanKMinute, is_stock
ocean_man['I30'] = OceanKMinute, is_index

ocean_man['S05'] = OceanKMinute, is_stock
ocean_man['I05'] = OceanKMinute, is_index

ocean_man['S01'] = OceanKMinute, is_stock
ocean_man['I01'] = OceanKMinute, is_index

