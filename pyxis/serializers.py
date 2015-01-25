from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from rest_framework import serializers
from madlee.serializers import UserSerializer
from pyxis.models import Account, Command, JobLog

class CommandSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField()
    class Meta:
        model = Command
        fields = ('id', 'name', 'command', 'work_folder', 'account')

class AccountSerializer(serializers.ModelSerializer):
    
    commands = CommandSerializer(many=True, read_only=True)
    class Meta:
        model = Account
        fields = ('id', 'name', 'url', 'commands',)


class JobLogSerializer(serializers.ModelSerializer):

    command = CommandSerializer(read_only=True)
    author = UserSerializer(read_only=True)
    class Meta:
        model = JobLog
        fields = ('id', 'command', 'author', 'timestamp0', 'timestamp1', 'timestampZ', 'return_code')