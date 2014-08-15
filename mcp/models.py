import time
from django.conf import settings
from django.db import models

class ModProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='mod_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.CharField(max_length=100, blank=True, null=True)

class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='activity', blank=True, null=True)
    description = models.TextField()
    timestamp = models.IntegerField(default=lambda: int(time.time()))
    icon = models.CharField(max_length=50, blank=True, null=True) # Only for cases where there is no user
    action = models.BooleanField(default=True) # Defines whether or not to count it as an action

class Bulletin(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bulletins')
    timestamp = models.IntegerField(default=lambda: int(time.time()))
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='read_bulletins')

    class Meta:
        ordering = ['-timestamp']

    def check_read(self, user_id):
        return self.read_by.filter(id=user_id).count() != 0