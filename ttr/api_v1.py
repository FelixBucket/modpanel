from django.contrib import auth
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.resources import ModelResource, ALL
from . import api
from . import util
from .tasty_util import *
from .models import *
from mcp.models import *
from mcp.permissions import permissions

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

class ActivityResource(DirectModelResource):
    class Meta:
        queryset = Activity.objects.all()
        resource_name = 'activities'
        limit = 50
        max_limit = None

    def dehydrate(self, bundle):
        bundle.data['user'] = user_dict(bundle, 'user')
        return bundle

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

class UserResource(DirectModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        excludes = ['password']
        filtering = {
            'id': ALL,
            'username': ALL,
            'email': ALL,
        }
        limit = 100
        max_limit = None
        authorization = ReadOnlyUserLevelAuthorization('find_user', MODE_MATCH_LEVEL)
