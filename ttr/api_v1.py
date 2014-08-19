import datetime, time, copy
from datetime import timedelta
from django.contrib import auth
from django.core.context_processors import csrf
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateformat import format
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
from mcp.util import require_permission
from ttr.rpc import RPC

### TTR Model Resources
# None Yet

### MCP Model Resources ###
def user_dict(bundle, user_prop_name):
    try:
        user = getattr(bundle.obj, user_prop_name)
        return user_dict_direct(user)
    except:
        return None

def user_dict_direct(user):
    try:
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
    ###
    # This method handles both phases of Two-Factor Authentication
    # If a value of tfa_userid is present, it will treat it as the second
    # leg of two-factor auth. If it is not, it will be the first leg.
    ###

    # Check to make sure the user isn't logged in already, if they are we'll return the same data below
    if not request.user.is_authenticated():

        if request.POST.get('tfa_userid'):
            ### The second leg of TFA ###
            user = auth.authenticate(session=request.session, user_id=request.POST.get('tfa_userid'), token=request.POST.get('tfa_token'), signature=request.POST.get('tfa_signature'))

            if user is not None:
                auth.login(request, user)
            else:
                return api.error(400, errors='Your authentication token was invalid.')
        else:
            ### The first leg of TFA, or potentially no TFA at all ###
            user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

            if user is not None:
                if user.is_active:
                    if user.level >= 200:

                        # Before we continue, check the remember_me option
                        if int(request.POST.get('remember_me', 0)) == 0:
                            # The user doesn't want us to remember them
                            # Tell the cookie to expire when the browser closes
                            request.session.set_expiry(0)

                        # The user has successfully verified their password and is authorized to login
                        # But first, let's see if they have two step auth enabled
                        if user.totp_secret:
                            return api.response(user.begin_two_factor_authentication(request.session))
                        else:
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
        return api.response({'status': 'pls_create_mod_profile'})

    # Fetch user information
    permissions = user.get_permissions()

    csrf_holder = {}
    csrf_holder.update(csrf(request))

    response = {
        'status': 'success',
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
    toon_names_count = ToonName.objects.filter(processed=None).count()
    comments_count = NewsItemComment.objects.filter(approved=False).count()
    return api.response(dict(toon_names=toon_names_count, comments=comments_count))

def DashboardStatsResource(request):
    today = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
    today_timestamp = time.mktime(today.timetuple())

    accounts_count = User.objects.all().count()
    playtimes_count = ScheduledSession.objects.all().count()
    actions_today_count = Action.objects.filter(timestamp__gte=today_timestamp).count()
    total_actions_count = Action.objects.all().count()
    return api.response(dict(accounts=accounts_count, playtimes=playtimes_count,
                            actions_today=actions_today_count, total_actions=total_actions_count))

class ActionStoryResource(DirectModelResource):
    class Meta:
        queryset = ActionStory.objects.all()
        resource_name = 'action_stories'
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
        Action.objects.log(user, 'posted', 'Bulletin', 0, related_id=bundle.obj.id)
        return bundle

class UserResource(DirectModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        excludes = ['password', 'totp_secret', 'gs_user_id', 'toonbook_user_id']
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

@require_permission('approve_name')
def ToonNameModerateAction(request, name_id):
    if not request.method == "POST":
        return api.error(405)

    user = request.user

    try:
        name = ToonName.objects.get(pk=name_id, processed=None)
    except:
        return api.response(status=201) # If it wasn't been found, it has already been moderated

    name.processed = datetime.datetime.now()
    name.submitted = datetime.datetime.now()
    name.reviewer = user

    rpc = RPC()

    # message code 100 = name approved
    # message code 101 = name rejected

    # Calculate the number of points to award based on the time the name has been waiting
    # The thought process is that the harder names will sit longer, so we will award more
    # points to those. It will vary from 1 to 3.
    # We will also reward a bonus point for a very quick moderation. (30 seconds)
    time_submitted = int(format(name.received, u'U'))
    time_delta = int(time.time()) - time_submitted
    print time_delta
    points = 1
    if (time_delta <= 30):
        points = 2
    elif (time_delta >= 1800): # 30 minutes
        points = 2
    elif (time_delta >= 10800): # 3 hours
        points = 3

    if int(request.POST.get('approve', 0)) == 1:
        name.was_rejected = False
        if rpc.client.approveName(avId=name.toon_id, name=name.candidate_name) == None:
            name.save()
            Action.objects.log(user, 'approved', 'Toon Name', points, related_id=name_id)
            # Alert the user that their name was approved.
            rpc.client.messageAvatar(avId=name.toon_id, code=100, params=[])
    else:
        name.was_rejected = True
        if rpc.client.rejectName(avId=name.toon_id) == None:
            name.save()
            Action.objects.log(user, 'rejected', 'Toon Name', points, related_id=name_id)
            # Alert the user that their name was denied.
            rpc.client.messageAvatar(avId=name.toon_id, code=101, params=[])

    util.send_pusher_message('toon_names', 'moderated', dict(toon_name_id=name.id, moderator=user.get_mini_name(), approve=int(request.POST.get('approve', 0))))

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

@require_permission('approve_comment')
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
        Action.objects.log(user, 'approved', 'Comment', 1, related_id=comment_id)
    else:
        Action.objects.log(user, 'rejected', 'Comment', 1, related_content=comment.body)
        comment.delete()

    util.send_pusher_message('news_comments', 'moderated', dict(comment_id=int(comment_id), moderator=user.get_mini_name(), approve=int(request.POST.get('approve', 0))))

    return api.response(status=201)

@require_permission('view_shards')
def ShardsResource(request):
    rpc = RPC()
    return api.response(rpc.client.listShards())

@require_permission('find_user')
def FindAccountFromAvId(request):
    avId = request.GET['avId']
    if not avId:
        return api.response(status=201, errors='You must specifiy an avId')

    rpc = RPC()
    accountId = rpc.client.getAccountByAvatarID(avId=avId)
    response = {"accountId": accountId}
    return api.response(response)

class BasicShardHistoryResource(DirectModelResource):
    class Meta:
        queryset = ShardCheckIn.objects.all()
        resource_name = 'basic_shard_history'
        filtering = {
            'district': ALL,
        }
        excludes = ['district_id', 'channel', 'heap_objects', 'heap_garbage', 'frame_rate', 'cpu_usage', 'mem_usage']
        limit = 200
        max_limit = None
        authorization = ReadOnlyUserLevelAuthorization('view_basic_shard_history', MODE_MATCH_LEVEL)

@require_permission('view_basic_shard_history')
def PopulationHistoryResource(request):
    # Load population data
    cursor = connection.cursor()
    cursor.execute("SELECT fetched as timestamp, SUM(population) as population FROM mcp_shardcheckin GROUP BY fetched ORDER BY fetched DESC;")
    population = cursor.fetchall()

    # Convert to a nicer format
    points = [dict(timestamp=p[0], population=int(p[1])) for p in population]

    return api.response(points)

def LeaderboardsResource(request):
    cursor = connection.cursor()

    now = datetime.datetime.now()
    leaderboards = {}

    order_mode = 'DESC'
    if request.GET.get('mode', '') == 'last':
        order_mode = 'ASC'

    # Daily
    today = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
    today_timestamp = str(time.mktime(today.timetuple()))
    cursor.execute("SELECT user_id, SUM(points) as total FROM mcp_action WHERE timestamp >= " + today_timestamp + " GROUP BY user_id ORDER BY total " + order_mode + " LIMIT 5;")
    leaderboards['daily'] = cursor.fetchall()

    # Weekly
    week_start = today - timedelta(days=today.weekday() + 1 % 7)
    week_start_timestamp = str(time.mktime(week_start.timetuple()))
    cursor.execute("SELECT user_id, SUM(points) as total FROM mcp_action WHERE timestamp >= " + week_start_timestamp + " GROUP BY user_id ORDER BY total " + order_mode + " LIMIT 5;")
    leaderboards['weekly'] = cursor.fetchall()

    # All Time
    cursor.execute("SELECT user_id, SUM(points) as total FROM mcp_action GROUP BY user_id ORDER BY total " + order_mode + " LIMIT 5;")
    leaderboards['all_time'] = cursor.fetchall()

    # Fill in details
    real_leaderboards = []
    for timeperiod, board in leaderboards.iteritems():
        pretty_board = []
        for leader in board:
            pretty_board.append(dict(user=user_dict_direct(User.objects.get(pk=leader[0])), points=int(leader[1])))
        leaderboards[timeperiod] = pretty_board

    return api.response(leaderboards)
