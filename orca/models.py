from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import logging

from django.db import models, connection
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

from orca.ocean import ocean_man


logger = logging.getLogger('orca.models')


STATUS_CHOICES = [  ('D', 'DEVELOPING'),    # In developing. No auto-update will be applied.
                    ('T', 'TESTING'),       # In testing. Will be update everyday. But other user cannot read.
                    ('P', 'PUBLISHED'),     # A stable production. Will be update everyday. User can read data.
                    ('X', 'DEPRECATED')     # Deprecated. Invisible to users.
                ]

SQL_SELECT_MAX_DATE = """SELECT MAX(date) 
    FROM %(table_name)s 
    WHERE %(node_name)s__id = ?
"""

SQL_SELECT_MIN_DATE = """SELECT MIN(date) 
    FROM %(table_name)s 
    WHERE %(node_name)s__id = ?
"""

SQL_SELECT_ALPHA = """SELECT date, stock, value 
    FROM orca_alphaitem 
    WHERE alpha_id = ? AND 
"""

@python_2_unicode_compatible
class BasicEntry(models.Model):
    """Basic class for Ocean, Alpha, Universe and Category. """

    # Name of it.
    name = models.CharField(max_length=200)
    # In default it is author. But admin may change it to anyone else.
    owner = models.ForeignKey(User) 
    # Say something.
    describe = models.TextField(default='')

    # If it is None, NO update. Otherwize, it will update every day on specific time.
    # Time is in format hhmm. For example: 1400 means 2:00 pm on machine time.
    update_on = models.IntegerField(null=True, default=None)
    
    # The python code to run for updating. Only owner can read it.
    update_code = models.TextField(default='')

    # The status of the entry.
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='D')

    author = models.ForeignKey(User, related_name='+')      # Who created this Entry
    timestamp0 = models.DateTimeField(auto_now_add=True)    # Created on
    timestamp1 = models.DateTimeField(auto_now=True)        # Last update on

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-timestamp0']

@python_2_unicode_compatible
class LogForEntry(models.Model):
    """Log and comment to the entry"""

    entry = models.ForeignKey(BasicEntry)                   # to which entry
    author = models.ForeignKey(User)                        # by who
    timestamp0 = models.DateTimeField(auto_now_add=True)    # on when
    note = models.TextField()                               # Do what

    def __str__(self):
        return self.note

    class Meta:
        ordering = ['-timestamp0']

class Ocean(BasicEntry):
    """A set of data"""
    pass

class Alpha(BasicEntry):
    """Alpha. You know what it is."""

    ITEM_TABLE_NAME = 'orca_alphaitem'
    
    def generate(self, date1, date2, code=None):
        """Generate alpha between [date1, date2)"""
        if not code:
            code = self.update_code

        vars = {'date1': date1, 'date2': date2}
        exec(code, {}, vars)
        return vars['result']

    def reset(self, date1=None, date2=None):
        # TODO:
        pass


    def update(self, date1, date2):
        alpha = self.generate(date1, date2)
        alpha = alpha[alpha['date'] >= date1 and alpha['date'] < date2]
        alpha = alpha.stack().reset_index()
        alpha.columns = ['date', 'stock', 'value']

        alpha = alpha[pandas.notnan(alpha['value'])]
        alpha['alpha_id'] = self.id
        alpha.to_sql(connection, connection, if_exists='append', index=False)

    def frame(self, date1=None, date2=None):
        assert self.id

    def max_date(self):
        sql = SQL_SELECT_MAX_DATE % {'table_name': self.ITEM_TABLE_NAME, 'node_name': 'alpha'}
        cursor = connection.cursor()
        if cursor.execute(sql, [self.id]):
            return cursor.fetchone()

    def min_date(self):
        sql = SQL_SELECT_MIN_DATE % {'table_name': self.ITEM_TABLE_NAME, 'node_name': 'alpha'}
        cursor = connection.cursor()
        if cursor.execute(sql, [self.id]):
            return cursor.fetchone()


class Universe(BasicEntry):
    """A set of stock on specific date"""
    pass

