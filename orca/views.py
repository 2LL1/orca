from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


from django.shortcuts import render
from rest_framework import viewsets

from orca.serializers import *

class LogForEntryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LogForEntrySerializer
    queryset = LogForEntry.objects.all()

class AlphaViewSet(viewsets.ModelViewSet):
    serializer_class = AlphaSerializer
    queryset = Alpha.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class UniverseViewSet(viewsets.ModelViewSet):
    serializer_class = UniverseSerializer
    queryset = Universe.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

def render_html(request, path, basic_path='orca/%s.html'):
    context = {'user':request.user}
    return render(request, basic_path % path, context)