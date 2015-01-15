from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route


from orca.serializers import *

class OrcaViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        result = self.queryset
        return result
        if not self.request.user.is_superuser:
            q = Q(owner=self.request.user) | Q(status='P')
            result = self.queryset.filter(q)

        return result

    @detail_route(methods=['post'])
    def set_name(self, request, pk=None):
        record = self.get_object()
        if record.owner == request.user:
            record.name = request.POST['name']
            record.save()
            return Response({'status': 'name changed.'})
        else:
            return Response("Only owner can edit the name.",
                            status=status.HTTP_403_FORBIDDEN)

    @detail_route(methods=['post'])
    def set_describe(self, request, pk=None):
        record = self.get_object()
        if record.owner == request.user:
            record.describe = request.POST['describe']
            record.save()
            return Response({'status': 'Describe changed.'})
        else:
            return Response("Only owner can edit the name.",
                            status=status.HTTP_403_FORBIDDEN)


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

   
def render_html(request, path, basic_path='orca/%s.html'):
    context = {'user':request.user}
    return render(request, basic_path % path, context)

