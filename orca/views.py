from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, permissions

from orca.serializers import *

class OrcaViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        result = self.queryset
        if not self.request.user.is_superuser:
            q = Q(owner=self.request.user) | Q(status='P')
            result = self.queryset.filter(q)

        return result


class LogForEntryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LogForEntrySerializer
    queryset = LogForEntry.objects.all()


class OceanViewSet(OrcaViewSet):
    serializer_class = OceanSerializer
    queryset = Ocean.objects.all()


class AlphaViewSet(OrcaViewSet):
    serializer_class = AlphaSerializer
    queryset = Alpha.objects.all()

class UniverseViewSet(OrcaViewSet):
    serializer_class = UniverseSerializer
    queryset = Universe.objects.all()

class CategoryViewSet(OrcaViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

   
def render_html(request, path, basic_path='orca/%s.html'):
    context = {'user':request.user}
    return render(request, basic_path % path, context)