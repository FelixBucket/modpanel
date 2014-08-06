from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # This is the entry point to the application
    # In the future if we add different components, the MCP can be moved to a subdirectory

    # url(r'^$', 'ttr.views.home', name='home'),
    url(r'^', include('mcp.urls', namespace='mcp')),
)
