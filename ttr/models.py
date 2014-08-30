import base64, hashlib, uuid, datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.forms import model_to_dict
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
    totp_secret = models.CharField(max_length=255, blank=True, null=True)
    keyed = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    class Meta:
        managed = False
        db_table = 'user'

    def get_mini_name(self):
        profile = self.get_mod_profile()
        first_name = profile.get('first_name', '')
        last_name = profile.get('last_name', '')

        mini_name = first_name

        # If we have a last name, we only want to display an initial.
        if last_name:
            mini_name += ' ' + last_name[0]
            # Append period if we don't already have one.
            if not mini_name.endswith('.'):
                mini_name += '.'

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

        return pbkdf2_hash == new_hash

    def begin_two_factor_authentication(self, session):
        # Generate a TFA key and salt, store them for later verification
        tfa_key = str(uuid.uuid4())
        tfa_salt = str(uuid.uuid4())
        session['tfa_key'] = tfa_key
        session['tfa_salt'] = tfa_salt

        # Generate the signature to send back to the user
        tfa_sig = base64.b16encode(pbkdf2(tfa_key + self.password, tfa_salt, 1000, 24))

        return {
            'status': 'tfa',
            'tfa_userid': self.id,
            'tfa_signature': tfa_sig
        }

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

# Infractions System
class Infraction(models.Model):
    # Internal can only be seen by staff, external will be shown to the user.
    # Internal is technically optional, but will almost always be filled with details.
    external_reason = models.TextField()
    internal_reason = models.TextField(blank=True, null=True)

    # The user who created/reported the infraction
    moderator = models.ForeignKey(User)

    # The date the infraction was first created (not necessarily approved)
    created = models.DateTimeField(default=datetime.datetime.now)

    # Approved can either be True, False or NULL. Null means it is awaiting a decision.
    # We want to keep it even if it is not approved because it is good to have on record.
    # When this decision is made, the decided field will be populated with the current DateTime.
    approved = models.NullBooleanField(blank=True, null=True)
    decided = models.DateTimeField(blank=True, null=True)

    # If expiration is NULL it lasts forever.
    expiration = models.DateTimeField(blank=True, null=True)

    ### Consequence Types ###
    # Defaults are passive, meaning they have no effect on the user
    # unless they are explicitly set to something.
    # For example, change_level is NULL by default, so it will only
    # change their level if it has a value such as 100.
    change_level        = models.IntegerField(blank=True, null=True)
    speedchat_only      = models.BooleanField(default=False)
    no_true_friends     = models.BooleanField(default=False)
    no_community_areas  = models.BooleanField(default=False) # parties, estates

    class Meta:
        managed = False
        db_table = 'infraction'

    def toDetailedDict(self):
        infraction = model_to_dict(self)
        subjects = []

        for raw_subject in self.subjects.all():
            subject = model_to_dict(raw_subject)

            if raw_subject.identifier_type == "user":
                try:
                    user = model_to_dict(User.objects.get(pk=raw_subject.identifier))
                    del user['password']
                    del user['totp_secret']
                    subject['instance'] = user
                except:
                    subject['instance'] = None
            elif raw_subject.identifier_type == "ip_address":
                subject['instance'] = raw_subject.identifier
            else:
                subject['instance'] = None

            subjects.append(subject)

        infraction['subjects'] = subjects
        return infraction

class InfractionSubject(models.Model):
    identifier_type = models.CharField(max_length=30)
    identifier = models.CharField(max_length=255)
    infraction = models.ForeignKey(Infraction, related_name='subjects')

    ### Barbed Subjects ###
    # If a subject is covered in barbs, any contact with it will cause
    # the infraction to spread. So if 123.456.77.31 is barbed and Anth
    # logs in from that IP, Anth will be added as an infraction subject.
    # It also works in reverse.
    barbed = models.BooleanField(default=False)

    # If this subject was created because of a barb, we will reference it here.
    # A value of NULL means it was set directly by the moderator.
    pricked_by = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'infraction_subject'
