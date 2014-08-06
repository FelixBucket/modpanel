from django import template
register = template.Library()
import os, re, json
from django.conf import settings

from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict

version_cache = {}

rx = re.compile(r"^(.*)\.(.*?)$")
def version(path_string):
    try:
        if path_string in version_cache:
            mtime = version_cache[path_string]
        else:
            mtime = os.path.getmtime('%s%s' % (settings.STATIC_URL, path_string,))
            version_cache[path_string] = mtime

        return settings.STATIC_URL + rx.sub(r"\1.%d.\2" % mtime, path_string)
    except:
        return settings.STATIC_URL + path_string

register.simple_tag(version)

@register.filter(name='jsonencode')
def jsonencode(obj):
    class CloudEncoder(DjangoJSONEncoder):
        def default(self, obj, **kwargs):
            if isinstance(obj, date):
                return str(obj)
            elif isinstance(obj, models.Model):
                return model_to_dict(obj)
            elif isinstance(obj, ImageFieldFile):
                if obj:
                    return obj.url
                return None
            elif isinstance(obj, Decimal):
                return str(obj)
            else:
                return DjangoJSONEncoder.default(obj, **kwargs)
    if isinstance(obj, QuerySet):
        obj = list(obj)
    return json.dumps(obj, cls=CloudEncoder)