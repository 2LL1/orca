from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from rest_framework import serializers
from madlee.serializers import UserSerializer
from orca.models import BasicEntry, LogForEntry, Ocean, Alpha, Universe

class BasicEntrySerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    author = UserSerializer()

class LogForEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogForEntry        

class OceanSerializer(BasicEntrySerializer):
    class Meta:
        model = Ocean

class AlphaSerializer(BasicEntrySerializer):
    class Meta:
        model = Alpha

class UniverseSerializer(BasicEntrySerializer):
    class Meta:
        model = Universe


