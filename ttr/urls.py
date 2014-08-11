from django.conf.urls import patterns, include, url

# Tastypie
from tastypie.api import Api
from .api_v1 import *

v1_api = Api(api_name='v1')
v1_api.register(BulletinResource())

urlpatterns = patterns('',
    # API Endpoints First
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/v1/sidebar_counts/', 'ttr.api_v1.SidebarCountsResource'),
    url(r'^api/v1/dashboard_stats/', 'ttr.api_v1.DashboardStatsResource'),

    # This is the entry point to the application
    # In the future if we add different components, the MCP can be moved to a subdirectory
    # url(r'^$', 'ttr.views.home', name='home'),
    url(r'^', include('mcp.urls', namespace='mcp')),
)