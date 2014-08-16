import datetime, time
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
from ttr.rpc import RPC

### TTR Model Resources
# None Yet

### MCP Model Resources ###
def user_dict(bundle, user_prop_name):
    try:
        user = getattr(bundle.obj, user_prop_name)
        profile = user.get_mod_profile()
        return {
            'id': user.id,
            'mini_name': user.get_mini_name(),
            'short_name': user.get_short_name(),
            'long_name': user.get_long_name(),
            'avatar': profile.get('avatar'),
        }
    except:
        return None

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
            'mini_name': user.get_mini_name(),
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
    today = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
    today_timestamp = time.mktime(today.timetuple())

    accounts_count = User.objects.all().count()
    playtimes_count = ScheduledSession.objects.all().count()
    actions_today_count = Activity.objects.filter(action=True, timestamp__gte=today_timestamp).count()
    total_actions_count = Activity.objects.filter(action=True).count()
    return api.response(dict(accounts=accounts_count, playtimes=playtimes_count,
                            actions_today=actions_today_count, total_actions=total_actions_count))

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
    # Also mark it as read for the writer and create an activity event
    def obj_create(self, bundle, **kwargs):
        user = bundle.request.user
        bundle = super(BulletinResource, self).obj_create(bundle, author=user)
        bundle.obj.read_by.add(user)
        Activity.objects.log(user.get_mini_name() + ' posted a bulletin titled "' + bundle.obj.title + '".', user)
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

class ToonNameResource(DirectModelResource):
    class Meta:
        queryset = ToonName.objects.all()
        resource_name = 'toon_names'
        filtering = {
            'processed': ALL,
        }
        limit = 40
        max_limit = None
        authorization = ReadOnlyUserLevelAuthorization('approve_name', MODE_MATCH_LEVEL)

    def dehydrate(self, bundle):
        bundle.data['reviewer'] = user_dict(bundle, 'reviewer')
        return bundle

def ToonNameModerateAction(request, name_id):
    if not request.method == "POST":
        return api.error(405)

    user = request.user

    try:
        name = ToonName.objects.get(pk=name_id, processed=None)
    except:
        return api.response(status=201) # If it wasn't been found, it has already been moderated

    name.processed = datetime.datetime.now()
    name.reviewer = user

    rpc = RPC()

    if int(request.POST.get('approve', 0)) == 1:
        name.was_rejected = False
        if rpc.client.approveName(avId=name.toon_id, name=name.candidate_name) == None:
            name.save()
            Activity.objects.log(user.get_mini_name() + ' approved the name "' + name.candidate_name + '".', user)
    else:
        name.was_rejected = True
        if rpc.client.rejectName(avId=name.toon_id) == None:
            name.save()
            Activity.objects.log(user.get_mini_name() + ' rejected the name "' + name.candidate_name + '".', user)

    return api.response(status=201)

class NewsItemCommentResource(DirectModelResource):
    class Meta:
        queryset = NewsItemComment.objects.all()
        resource_name = 'news_item_comments'
        filtering = {
            'approved': ALL,
        }
        limit = 40
        max_limit = None
        authorization = ReadOnlyUserLevelAuthorization('approve_comment', MODE_MATCH_LEVEL)

    def dehydrate(self, bundle):
        bundle.data['post'] = bundle.obj.post.title
        return bundle

def NewsItemCommentModerateAction(request, comment_id):
    if not request.method == "POST":
        return api.error(405)

    user = request.user

    try:
        comment = NewsItemComment.objects.get(pk=comment_id)
    except:
        return api.response(status=201) # If it wasn't been found, it likely was already rejected

    if int(request.POST.get('approve', 0)) == 1:
        comment.approved = True
        comment.save()
        Activity.objects.log(user.get_mini_name() + ' approved the comment "' + comment.body + '".', user)
    else:
        Activity.objects.log(user.get_mini_name() + ' rejected the comment "' + comment.body + '".', user)
        comment.delete()

    return api.response(status=201)
