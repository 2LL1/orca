from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from rest_framework import serializers
from madlee.serializers import UserSerializer
from pyxis.models import Account, Command, JobLog

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command

class JobLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobLog

