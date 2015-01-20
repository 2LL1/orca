from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route


from orca.serializers import *
from orca.models import STATUS_CHOICES, User

class OrcaViewSet(viewsets.ReadOnlyModelViewSet):

    def _save_log(self, record, author, note):
        log = LogForEntry()
        log.entry = record
        log.author = author
        log.note = note
        log.save()

    def get_queryset(self):
        result = self.queryset
        return result
        if not self.request.user.is_superuser:
            q = Q(owner=self.request.user) | Q(status='P')
            result = self.queryset.filter(q)

        return result

    def _save_change(self, request, pk, attr):
        new_val = request.POST[attr]
        record = self.get_object()
        if record.owner == request.user:
            author = request.user
            old_val = getattr(record, attr)
            note = "Change %s [%s]->[%s]" % (attr, old_val, new_val)
            if new_val != old_val:
                setattr(record, attr, new_val)
                record.save()
                self._save_log(record, author, note)
                return Response({'status': '%s changed.' % attr})
            else:
                return Response({'status': '%s do not changed'})
        else:
            return Response("Only owner can edit the %s." % attr,
                            status=status.HTTP_403_FORBIDDEN)

    @detail_route(methods=['post'])
    def set_name(self, request, pk=None):
        return self._save_change(request, pk, 'name')

    @detail_route(methods=['post'])
    def set_describe(self, request, pk=None):
        return self._save_change(request, pk, 'describe')

    @detail_route(methods=['post'])
    def set_status(self, request, pk=None):
        return self._save_change(request, pk, 'status')

    @detail_route(methods=['post'])
    def set_update_on(self, request, pk=None):
        return self._save_change(request, pk, 'update_on')

    def _save_record(self, record, request):
        record.name = request.POST['name']
        record.describe = request.POST['describe']
        record.status = request.POST['status']
        record.update_on = request.POST['update_on']
        record.update_code = request.POST['update_code']
        record.save()

    @detail_route(methods=['post'])
    def set_owner(self, request, pk=None):
        new_val = request.POST['owner']
        new_val = User.objects.get(username = new_val)
        record = self.get_object()
        if record.owner.is_superuser:
            old_val = record.owner.usrename
            note = "Change owner [%s]->[%s]" % (old_val, new_val)
            self._save_log(record, author, note)
            record.owner = new_val
            record.save()
            return Response({'status': '%s changed.' % attr})
        else:
            return Response("Only super user can edit owner.",
                            status=status.HTTP_403_FORBIDDEN)

    @detail_route(methods=['post'])
    def save(self, request, pk=None):
        record = self.get_object()
        if record.owner == request.user:
            self._save_record(record, request)
            self._save_log(record, request.user, "Changed the record")
            return Response({'status': 'Record changed.', 'id': record.id})
        else:
            return Response("Only owner can edit the record.",
                            status=status.HTTP_403_FORBIDDEN)

    def _new(self, request, record):
        record.owner = record.author = request.user
        self._save_record(record, request)
        self._save_log(record, request.user, "Created the record")
        return Response({'status': 'Record created.', 'id': record.id})

    @list_route(methods=['get'])
    def filter(self, request):
        status = dict(STATUS_CHOICES)
        users = User.objects.filter(is_active=True)
        users = UserSerializer(users, many=True).data
        return Response({'status': status, 'users': users})

class LogForEntryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LogForEntrySerializer
    queryset = LogForEntry.objects.all()


class OceanViewSet(OrcaViewSet):
    serializer_class = OceanSerializer
    queryset = Ocean.objects.all()

    @list_route(methods=['post'])
    def new(self, request):
        return self._new(request, Ocean())

class AlphaViewSet(OrcaViewSet):
    serializer_class = AlphaSerializer
    queryset = Alpha.objects.all()

    @list_route(methods=['post'])
    def new(self, request):
        return self._new(request, Alpha())

class UniverseViewSet(OrcaViewSet):
    serializer_class = UniverseSerializer
    queryset = Universe.objects.all()

    @list_route(methods=['post'])
    def new(self, request):
        return self._new(request, Universe())

   
def render_html(request, path, basic_path='orca/%s.html'):
    context = {'user':request.user}
    return render(request, basic_path % path, context)

