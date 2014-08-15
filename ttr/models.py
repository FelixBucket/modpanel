import base64, hashlib
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.utils.crypto import pbkdf2
from mcp.models import ModProfile
from mcp.permissions import permissions

## TTR Models ##
# Models where managed = False prevents Django/South from making schema changes

# Custom User model to play nice with Play (har har)
class User(AbstractBaseUser):
    username = models.CharField(max_length=255, null=True, unique=True)
    email = models.CharField(max_length=255, null=True)
    verified = models.BooleanField(default=False)
    activated = models.BooleanField(default=False)
    level = models.IntegerField(blank=True, null=True, db_column='type')
    register_date = models.DateTimeField(blank=True, null=True)
    register_ip = models.CharField(max_length=255, null=True)
    activate_date = models.DateTimeField(blank=True, null=True)
    gs_user_id = models.IntegerField(default=-1, null=True)
    toonbook_user_id = models.IntegerField(default=-1, null=True)
    totp_secret = models.CharField(max_length=255, null=True)
    keyed = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    class Meta:
        managed = False
        db_table = 'user'

    def get_mini_name(self):
        profile = self.get_mod_profile()
        last_name = profile.get('last_name', '')
        if len(last_name) == 0:
            last_name = ' '
        mini_name = profile.get('first_name') + ' ' + last_name[0]

        # Check and see if we already have a period
        if not mini_name[-1:] == '.':
            mini_name + '.'

        return mini_name

    def get_short_name(self):
        profile = self.get_mod_profile()
        return profile.get('first_name')

    def get_long_name(self):
        profile = self.get_mod_profile()
        return profile.get('first_name') + ' ' + profile.get('last_name')

    def check_password(self, raw_password):
        # Convert Play format to Django format
        iterations, salt, pbkdf2_hash = self.password.split(':')

        new_raw_hash = pbkdf2(raw_password, base64.b16decode(salt.upper()), iterations, 24, hashlib.sha1)
        new_hash = base64.b16encode(new_raw_hash).lower()

        print pbkdf2_hash
        print new_hash

        return pbkdf2_hash == new_hash

    def get_mod_profile(self):
        try:
            return {
                'first_name': self.mod_profile.first_name,
                'last_name': self.mod_profile.last_name,
                'avatar': self.mod_profile.avatar,
            }
        except:
            return {'first_name': '', 'last_name': '', 'avatar': None}

    def get_permissions(self):
        perms = []
        for permission, level_required in permissions.iteritems():
            if self.level >= level_required:
                perms.append(permission)
        return perms

# Scheduled Session from Play
class ScheduledSession(models.Model):
    user = models.ForeignKey(User, null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    approved = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'scheduled_session'

# News Items and Comments from Play
class NewsItem(models.Model):
    author = models.ForeignKey(User, null=True)
    post_time = models.DateTimeField(null=True)
    release_time = models.DateTimeField(null=True)
    author_name = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    body = models.TextField(null=True)

    class Meta:
        managed = False
        db_table = 'news_item'

class NewsItemComment(models.Model):
    body = models.TextField(null=True)
    ip_address = models.CharField(max_length=255, db_column='ip', null=True)
    user = models.ForeignKey(User, null=True)
    post = models.ForeignKey(NewsItem, null=True)
    parent = models.ForeignKey('self', null=True)
    author = models.CharField(max_length=255, null=True)
    css = models.CharField(max_length=255, null=True)
    approved = models.BooleanField(default=False)
    posted = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'comment'
        ordering = ['id']

# Toon Names from Play
class ToonName(models.Model):
    toon_id = models.IntegerField(null=True)
    user_id = models.IntegerField(blank=True, null=True)
    candidate_name = models.CharField(max_length=255, null=True)
    current_name = models.CharField(max_length=255, blank=True, null=True)
    received = models.DateTimeField(null=True)
    processed = models.DateTimeField(blank=True, null=True)
    submitted = models.DateTimeField(blank=True, null=True)
    was_rejected = models.BooleanField()
    reviewer = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'toon_name'
        ordering = ['received']