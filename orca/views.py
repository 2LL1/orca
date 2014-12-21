from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


from django.shortcuts import render
from rest_framework import viewsets

from orca.serializers import *

class LogForEntryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LogForEntrySerializer
    queryset = LogForEntry.objects.all()

class AlphaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AlphaSerializer
    queryset = Alpha.objects.all()

class UniverseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UniverseSerializer
    queryset = Universe.objects.all()

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

def render_html(request, path, basic_path='orca/%s.html'):
    context = {'user':request.user}
    return render(request, basic_path % path, context)