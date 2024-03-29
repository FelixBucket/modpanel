from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.resources import ModelResource
from . import util
from .models import *
from mcp.permissions import permissions

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

# Custom Authorization Class to work with user levels
MODE_ALWAYS_ALLOW = 0
MODE_MATCH_LEVEL = 1
MODE_ALLOW_CREATOR = 2
MODE_NEVER_ALLOW = 3
class UserLevelAuthorization(Authorization):
    def __init__(self, permission, read_mode=MODE_ALWAYS_ALLOW, delete_mode=MODE_NEVER_ALLOW, user_property='user'):
        self.permission = permission
        self.read_mode = read_mode
        self.delete_mode = delete_mode
        self.user_property = user_property

    def read_list(self, object_list, bundle):
        if self.read_mode == MODE_ALWAYS_ALLOW:
            return object_list
        elif self.read_mode == MODE_MATCH_LEVEL and bundle.request.user.level >= permissions[self.permission]:
            return object_list
        elif self.read_mode == MODE_ALLOW_CREATOR:
            return object_list.filter(**{self.user_property: bundle.request.user})
        else:
            raise Unauthorized("You do not have permission to see that.")

    def read_detail(self, object_list, bundle):
        if self.read_mode == MODE_ALWAYS_ALLOW:
            return True
        elif self.read_mode == MODE_MATCH_LEVEL and bundle.request.user.level >= permissions[self.permission]:
            return True
        elif self.read_mode == MODE_ALLOW_CREATOR and bundle.obj.get(self.user_property) == bundle.request.user:
            return True
        else:
            return False

    def create_list(self, object_list, bundle):
        if bundle.request.user.level >= permissions[self.permission]:
            return object_list
        raise Unauthorized("You do not have permission to create that.")

    def create_detail(self, object_list, bundle):
        return bundle.request.user.level >= permissions[self.permission]

    def update_list(self, object_list, bundle):
        if bundle.request.user.level >= permissions[self.permission]:
            return object_list
        raise Unauthorized("You do not have permission to update that.")

    def update_detail(self, object_list, bundle):
        return bundle.request.user.level >= permissions[self.permission]

    def delete_list(self, object_list, bundle):
        if self.delete_mdoe == MODE_ALWAYS_ALLOW:
            return object_list
        elif self.delete_mdoe == MODE_MATCH_LEVEL and bundle.request.user.level >= permissions[self.permission]:
            return object_list
        elif self.delete_mdoe == MODE_ALLOW_CREATOR:
            return object_list.filter(**{self.user_property: bundle.request.user})
        else:
            raise Unauthorized("You do not have permission to delete that.")

    def delete_detail(self, object_list, bundle):
        if self.delete_mode == MODE_ALWAYS_ALLOW:
            return True
        elif self.delete_mode == MODE_MATCH_LEVEL and bundle.request.user.level >= permissions[self.permission]:
            return True
        elif self.delete_mode == MODE_ALLOW_CREATOR and bundle.obj.get(self.user_property) == bundle.request.user:
            return True
        else:
            return False

# A convenience version of UserLevelAuthorization that is strictly for reading
class ReadOnlyUserLevelAuthorization(Authorization):
    def __init__(self, permission, read_mode=MODE_ALWAYS_ALLOW, delete_mode=MODE_NEVER_ALLOW, user_property='user'):
        self.permission = permission
        self.read_mode = read_mode
        self.delete_mode = delete_mode
        self.user_property = user_property

    def read_list(self, object_list, bundle):
        if self.read_mode == MODE_ALWAYS_ALLOW:
            return object_list
        elif self.read_mode == MODE_MATCH_LEVEL and bundle.request.user.level >= permissions[self.permission]:
            return object_list
        elif self.read_mode == MODE_ALLOW_CREATOR:
            return object_list.filter(**{self.user_property: bundle.request.user})
        else:
            raise Unauthorized("You do not have permission to see that.")

    def read_detail(self, object_list, bundle):
        if self.read_mode == MODE_ALWAYS_ALLOW:
            return True
        elif self.read_mode == MODE_MATCH_LEVEL and bundle.request.user.level >= permissions[self.permission]:
            return True
        elif self.read_mode == MODE_ALLOW_CREATOR and bundle.obj.get(self.user_property) == bundle.request.user:
            return True
        else:
            return False

    def create_list(self, object_list, bundle):
        raise Unauthorized("You do not have permission to create that.")

    def create_detail(self, object_list, bundle):
        return False

    def update_list(self, object_list, bundle):
        raise Unauthorized("You do not have permission to update that.")

    def update_detail(self, object_list, bundle):
        return False

    def delete_list(self, object_list, bundle):
        raise Unauthorized("You do not have permission to delete that.")

    def delete_detail(self, object_list, bundle):
        return False