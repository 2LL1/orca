from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import traceback
from datetime import datetime as DateTime

from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route, api_view

from pyxis.serializers import *
from xmlrpclib import ServerProxy

def rest_view(func):
    def new_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if 'status' not in result:
                result['status'] = 'success'
            return Response(result)
        except Exception as e:
            if settings.DEBUG:
                traceback.print_exc()
            return Response({'status':'error', 'detail': str(e)})
    return new_func

class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

class CommandViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommandSerializer
    queryset = Command.objects.all()

    @detail_route(methods=['post'])
    @rest_view
    def new_job(self, request, pk=None):
        password = request.POST['password']
        user = authenticate(username=request.user.username, password=password)
        if user:
            if user.is_active:
                obj = self.get_object()
                proxy = ServerProxy(obj.account.url)
                result = proxy.run_shell(request.user.username, request.user.password, obj.command, obj.work_folder)
                log = JobLog()
                log.author = request.user
                log.command = obj
                log.client_id = result
                log.save()
                result = JobLogSerializer(log).data
            else:
                raise RuntimeError("User was disabled.")
        else:
            raise RuntimeError('Invalid password')

        return result

class JobLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobLogSerializer
    queryset = JobLog.objects.all()
   
def render_html(request, path, basic_path='pyxis/%s.html'):
    context = {'user':request.user}
    return render(request, basic_path % path, context)

@api_view(http_method_names=['POST'])
@rest_view
def refresh(request):
    accounts = {}
    for i in JobLog.objects.filter(timestampZ=None):
        if i.command.account in accounts:
            accounts[i.command.account].append(i)
        else:
            accounts[i.command.account] = [i]

    results = []
    for k, v in accounts.iteritems():
        proxy = ServerProxy(k.url)
        job_logs = {}
        for j in v:
            job_logs[j.client_id] = j

        ids = list(job_logs.keys())
        result = proxy.query_jobs(request.user.username, request.user.password, ids)
        for row in result[1:]:
            if row[-2] and row[0] in job_logs:
                log_i = job_logs[row[0]]
                log_i.timestampZ = DateTime.strptime(row[-2], '%Y-%m-%d %H:%M:%S.%f')
                log_i.return_code = row[-1]
                log_i.save()
                results.append(log_i)

    

    results = JobLogSerializer(results, many=True).data
    return {'results':results, 'count':len(results)}
