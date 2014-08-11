from django.conf import settings
from django.db import models

class ModProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.CharField(max_length=100)