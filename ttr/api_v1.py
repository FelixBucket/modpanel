from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from . import api
from . import util
from .models import *
from mcp.models import *

# Default Meta for models that can be written to
class WritableDefaults:
    authorization = Authorization()
    always_return_data = True

# Hides the meta and objects properties in the JSON response
class DirectModelResource(ModelResource):
    def get_list(self, request, **kwargs):
        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, resource_uri=self.get_resource_uri(), limit=self._meta.limit, max_limit=self._meta.max_limit, collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()

        bundles = []

        for obj in to_be_serialized[self._meta.collection_name]:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle, for_list=True))

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized['objects'])

### TTR Model Resources
# None Yet

### MCP Model Resources ###
def SidebarCountsResource(request):
    toon_names_count = 0
    comments_count = NewsItemComment.objects.filter(approved=False).count()
    return api.response(dict(toon_names=toon_names_count, comments=comments_count))

def DashboardStatsResource(request):
    accounts_count = User.objects.all().count()
    playtimes_count = ScheduledSession.objects.all().count()
    return api.response(dict(accounts=accounts_count, playtimes=playtimes_count, actions_today=0, total_actions=0))