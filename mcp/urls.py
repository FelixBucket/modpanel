from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # MCP Single Page Application
    url(r'^$', 'mcp.views.app', name='panel'),
)
