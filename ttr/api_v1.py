from django.contrib import auth
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.resources import ModelResource
from . import api
from . import util
from .models import *
from mcp.models import *
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

### TTR Model Resources
# None Yet

### MCP Model Resources ###
def user_dict(bundle, user_prop_name):
    user = getattr(bundle.obj, user_prop_name)
    profile = user.get_mod_profile()
    return {
        'id': user.id,
        'short_name': user.get_short_name(),
        'long_name': user.get_long_name(),
        'avatar': profile.get('avatar'),
    }

@csrf_exempt
def LoginResource(request):
    # Check to make sure the user isn't logged in already, if they are we'll return the same data below
    if not request.user.is_authenticated():
        user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            if user.is_active:
                if user.level >= 200:
                    # Login
                    auth.login(request, user)
                else:
                    return api.error(403, errors='You are not authorized to come in here.')
            else:
                return api.error(403, errors='Your account was disabled by the administrator.')
        else:
            return api.error(400, errors='Your username or password was incorrect.')
    else:
        user = request.user

    if not hasattr(user, 'mod_profile'):
        return api.error(400, errors='Please login from the website to set up your account for the first time.')

    # Fetch user information
    permissions = user.get_permissions()

    csrf_holder = {}
    csrf_holder.update(csrf(request))

    response = {
        'user': {
            'id': request.user.id,
            'short_name': request.user.get_short_name(),
            'long_name': request.user.get_long_name(),
            'avatar': request.user.mod_profile.avatar,
            'level': request.user.level,
            'csrf_token': unicode(csrf_holder.get('csrf_token')),
        },
        'permissions': permissions,
    }
    return api.response(response)

def PendingCountsResource(request):
    toon_names_count = 0
    comments_count = NewsItemComment.objects.filter(approved=False).count()
    return api.response(dict(toon_names=toon_names_count, comments=comments_count))

def DashboardStatsResource(request):
    accounts_count = User.objects.all().count()
    playtimes_count = ScheduledSession.objects.all().count()
    return api.response(dict(accounts=accounts_count, playtimes=playtimes_count, actions_today=0, total_actions=0))

class BulletinResource(DirectModelResource):
    class Meta:
        queryset = Bulletin.objects.all()
        resource_name = 'bulletins'
        limit = 20
        max_limit = None
        authorization = UserLevelAuthorization('post_bulletin')
        always_return_data = True

    def dehydrate(self, bundle):
        bundle.data['author'] = user_dict(bundle, 'author')
        bundle.data['unread'] = not bundle.obj.check_read(bundle.request.user.id)
        return bundle

    # Mark the bulletin as read if it is pulled directly
    def obj_get(self, bundle, **kwargs):
        obj = super(BulletinResource, self).obj_get(bundle, **kwargs)

        user = bundle.request.user
        if not bundle.obj.check_read(user.id):
            bundle.obj.read_by.add(user)

        return obj

    # Ensure the logged in user gets saved as the author
    # Also mark it as read for the writer
    def obj_create(self, bundle, **kwargs):
        bundle = super(BulletinResource, self).obj_create(bundle, author=bundle.request.user)
        bundle.obj.read_by.add(bundle.request.user)
        return bundle