from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from rest_framework import serializers
from orca.models import BasicEntry, LogForEntry, Alpha, AlphaItem, Universe, UniverseItem, Category, CategoryItem

class BasicEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicEntry

class LogForEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogForEntry        

class AlphaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alpha

class AlphaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlphaItem

class UniverseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universe

class UniverseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniverseItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

class CategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryItem

