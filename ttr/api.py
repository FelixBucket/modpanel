import json
from django.http import HttpResponse
from .util import jsonencode

class ApiException(Exception):
    def __init__(self, error):
        self.error = error
    def __str__(self):
        return str(self.error)

def response(response=None, **kwargs):
    if response is not None:
        if kwargs.get('encode', True) is not False:
            response = jsonencode(response)
        status = kwargs.get('status', 200)
        return HttpResponse(response, status=status, content_type="application/json")

    return HttpResponse(None, status=204)

def error(http_code=400, errors=None):
    if errors is None and http_code != 405:
        return HttpResponse(status=http_code)
    if http_code == 405 and errors is None:
        errors = 'That method is not allowed for this resource.'

    if isinstance(errors, basestring):
        response = {'error': errors}
    else:
        response = {'errors': errors}
    return HttpResponse(json.dumps(response), status=http_code, content_type="application/json")