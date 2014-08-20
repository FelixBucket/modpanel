from django.conf.urls import patterns, include, url

# Tastypie
from tastypie.api import Api
from .api_v1 import *

v1_api = Api(api_name='v1')
v1_api.register(ActionStoryResource())
v1_api.register(BulletinResource())
v1_api.register(UserResource())
v1_api.register(ToonNameResource())
v1_api.register(NewsItemCommentResource())
v1_api.register(BasicShardHistoryResource())
v1_api.register(AccountResource())

urlpatterns = patterns('',
    ### API Endpoints First ###

    # General APIs #
    url(r'^api/v1/login/$', 'ttr.api_v1.LoginResource'),
    url(r'^api/v1/pending_counts/$', 'ttr.api_v1.PendingCountsResource'),

    # Dashboard APIs #
    url(r'^api/v1/dashboard_stats/$', 'ttr.api_v1.DashboardStatsResource'),
    url(r'^api/v1/population_history/$', 'ttr.api_v1.PopulationHistoryResource'),
    url(r'^api/v1/leaderboards/$', 'ttr.api_v1.LeaderboardsResource'),

    # Toon Names APIs #
    url(r'^api/v1/toon_names/(\d+)/moderate/$', 'ttr.api_v1.ToonNameModerateAction'),

    # News Comments APIs #
    url(r'^api/v1/news_item_comments/(\d+)/moderate/$', 'ttr.api_v1.NewsItemCommentModerateAction'),

    # Accounts APIs #
    url(r'^api/v1/find_accounts/([\w\-]+)/$', 'ttr.api_v1.FindAccountsResource'),

    # Utility APIs #
    url(r'^api/v1/shards/$', 'ttr.api_v1.ShardsResource'),

    # Potentially Deprecated APIs #
    url(r'^api/v1/avatar/$', 'ttr.api_v1.FindAccountFromAvId'),

    # All the TastyPie Resources #
    url(r'^api/', include(v1_api.urls)),

    # This is the entry point to the application
    # In the future if we add different components, the MCP can be moved to a subdirectory
    # url(r'^$', 'ttr.views.home', name='home'),
    url(r'^', include('mcp.urls', namespace='mcp')),
)