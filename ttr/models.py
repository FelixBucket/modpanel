import base64, hashlib
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.utils.crypto import pbkdf2

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

    def check_password(self, raw_password):
        # Convert Play format to Django format
        iterations, salt, pbkdf2_hash = self.password.split(':')

        new_raw_hash = pbkdf2(raw_password, base64.b16decode(salt.upper()), iterations, 24, hashlib.sha1)
        new_hash = base64.b16encode(new_raw_hash).lower()

        return pbkdf2_hash == new_hash