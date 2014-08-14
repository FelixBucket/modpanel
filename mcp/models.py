import time
from django.conf import settings
from django.db import models

class ModProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='mod_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.CharField(max_length=100)

class Bulletin(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bulletins')
    timestamp = models.IntegerField(default=lambda: int(time.time()))
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='read_bulletins')