from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from django.conf.urls import patterns, url, include
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from madlee import urls as madlee_urls
from orca.views import *
from pyxis.views import *


router_orca = DefaultRouter(trailing_slash=False)
router_orca.register(r'log', LogForEntryViewSet)
router_orca.register(r'ocean', OceanViewSet)
router_orca.register(r'alpha', AlphaViewSet)
router_orca.register(r'universe', UniverseViewSet)

router_pyxis = DefaultRouter(trailing_slash=False)
router_pyxis.register(r'account', AccountViewSet)
router_pyxis.register(r'command', CommandViewSet)
router_pyxis.register(r'joblog', JobLogViewSet)


urlpatterns = patterns('',
	url(r'^orca/(.+)\.html$', 'orca.views.render_html'),
	url(r'^orca/(.+)\.form$', 'orca.views.render_html', {'basic_path': 'orca/%s.form'}),
	url(r'^orca/', include(router_orca.urls)),
	url(r'^pyxis/(.+)\.html$', 'pyxis.views.render_html'),
	url(r'^pyxis/(.+)\.form$', 'pyxis.views.render_html', {'basic_path': 'pyxis/%s.form'}),
	url(r'^pyxis/', include(router_pyxis.urls)),
	url(r'^madlee/',  include(madlee_urls, namespace='madlee')),
    url(r'^admin/', include(admin.site.urls)),
)
