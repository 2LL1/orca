from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from pyxis.serializers import *



class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

class CommandViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommandSerializer
    queryset = Command.objects.all()

class JobLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobLogSerializer
    queryset = JobLog.objects.all()
   
def render_html(request, path, basic_path='pyxis/%s.html'):
    context = {'user':request.user}
    return render(request, basic_path % path, context)
