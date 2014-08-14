from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # MCP Auth
    url(r'^login/$', 'mcp.views.login', name='login'),
    url(r'^logout/$', 'mcp.views.logout', name='logout'),

    # First Time Mod Panel Registration
    url(r'^first_time/$', 'mcp.views.first_time', name='first_time'),

    # MCP Single Page Application
    url(r'^$', 'mcp.views.app', name='panel'),
)
