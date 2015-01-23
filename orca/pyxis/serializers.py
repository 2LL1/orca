from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from rest_framework import serializers
from madlee.serializers import UserSerializer
from pyxis.models import Account, Command, JobLog

class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command

class AccountSerializer(serializers.ModelSerializer):
    commands = CommandSerializer(many=True, read_only=True)
    class Meta:
        model = Account


class JobLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobLog

