from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # MCP Auth
    url(r'^login/$', 'mcp.views.login', name='login'),
    url(r'^logout/$', 'mcp.views.logout', name='logout'),

    # MCP Single Page Application
    url(r'^$', 'mcp.views.app', name='panel'),
)
