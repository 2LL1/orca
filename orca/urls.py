from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from django.conf.urls import patterns, url, include
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from madlee import urls as madlee_urls
from orca.views import *


router = DefaultRouter(trailing_slash=False)
router.register(r'log', LogForEntryViewSet)
router.register(r'ocean', OceanViewSet)
router.register(r'alpha', AlphaViewSet)
router.register(r'universe', UniverseViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = patterns('orca.views',
	url(r'^orca/(.+)\.html$', 'render_html', name='render_html'),
	url(r'^orca/(.+)\.form$', 'render_html', {'basic_path': 'orca/%s.form'}, name='render_form'),
	url(r'^orca/', include(router.urls)),
	url(r'^madlee/',  include(madlee_urls, namespace='madlee')),
    url(r'^admin/', include(admin.site.urls)),
)
