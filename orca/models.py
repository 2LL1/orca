from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

STATUS_CHOICES = [  ('D', 'DEVELOPING'),    # In developing. No auto-update will be applied.
                    ('T', 'TESTING'),       # In testing. Will be update everyday.
                    ('P', 'PRODUCT'),       # A stable production. Will be update everyday.
                    ('X', 'DEPRECATED')     # Deprecated. 
                ]

@python_2_unicode_compatible
class BasicEntry(models.Model):
    """Basic class for Alpha, Universe and Category"""

    # Name of it.
    name = models.CharField(max_length=200)
    # In default it is author. But admin may change it to anyone else.
    owner = models.ForeignKey(User) 
    # Say something.
    describe = models.TextField(default='')

    # If it is None, NO update. Otherwize, it will update every day on specific time.
    # Time is in format hhmm. For example: 1400 means 2:00 pm on machine time.
    update_on = models.IntegerField(null=True, default=None)
    # The python code to run for updating.
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
        permissions = ( ('can_deploy', 'Can deploy as PRODUCT'), )

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
        order_with_respect_to = 'entry'

class Alpha(BasicEntry):
    """Alpha. You know what it is."""
    pass

@python_2_unicode_compatible
class AlphaItem(models.Model):
    """Items in alpha. Please do not access it directly. Use the 
    functions in class Alpha to manipulate the items in data frame"""
    alpha = models.ForeignKey(Alpha)
    date = models.IntegerField()
    stock = models.IntegerField()
    value = models.FloatField()

    def __str__(self):
        return '[%06d] %06d: %.4f' % (self.date, self.stock, self.value)

    class Meta:
        order_with_respect_to = 'alpha'
        unique_together = ('alpha', 'date', 'stock')

class Universe(BasicEntry):
    """A set of stock on specific date"""
    pass

@python_2_unicode_compatible
class UniverseItem(models.Model):
    """Items in Universe. Please do not access it directly. Use the 
    functions in class Universe to manipulate the items in data frame"""

    universe = models.ForeignKey(Universe)
    date = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return '[%06d] %06d' % (self.date, self.stock)

    class Meta:
        order_with_respect_to = 'universe'
        unique_together = ('universe', 'date', 'stock')


class Category(BasicEntry):
    """A set of specific stock"""
    pass

@python_2_unicode_compatible
class CategoryItem(models.Model):
    """Items in Category. Please do not access it directly. Use the 
    functions in class Category to manipulate the items in data frame"""
    category  = models.ForeignKey(Category)
    stock = models.IntegerField()

    def __str__(self):
        return '[%06d]' % self.stock
