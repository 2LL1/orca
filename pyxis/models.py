from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import logging

from django.db import models, connection
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

from xmlrpclib import ServerProxy

@python_2_unicode_compatible
class Account(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    password = models.TextField()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Command(models.Model):
    account = models.ForeignKey(Account, related_name='commands')
    name = models.CharField(max_length=200)
    command = models.TextField()
    work_folder = models.TextField()

    def __str__(self):
        return '%s on %s' % (self.name, self.account)

@python_2_unicode_compatible
class JobLog(models.Model):
    command = models.ForeignKey(Command)
    author = models.ForeignKey(User)

    client_id = models.IntegerField()

    timestamp0 = models.DateTimeField(auto_now_add=True)
    timestamp1 = models.DateTimeField(auto_now=True)
    timestampZ = models.DateTimeField(null=True, default=None)

    return_code = models.IntegerField(null=True, default=None)

    def __str__(self):
        return str(self.author)

