from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

from rest_framework import serializers
from madlee.serializers import UserSerializer
from orca.models import BasicEntry, LogForEntry, Ocean, Alpha, AlphaItem, Universe, UniverseItem

class BasicEntrySerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    author = UserSerializer()

class LogForEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogForEntry        

class OceanSerializer(BasicEntrySerializer):
    class Meta:
        model = Alpha

class AlphaSerializer(BasicEntrySerializer):
    class Meta:
        model = Alpha

class UniverseSerializer(BasicEntrySerializer):
    class Meta:
        model = Universe


