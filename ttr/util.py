from django.template import RequestContext
from django.shortcuts import render, render_to_response
from .templatetags.utils import *

def render_template(request, template, data=None):
    # Wrapper around render_to_response that fills in context_instance for you
    response = render_to_response(template, data,
                              context_instance=RequestContext(request))
    return response

def boilerplate_render(template):
    # Factory function for creating simple views that only forward to a template
    def view(request, **kwargs):
        response = render_template(request, template, kwargs)
        return response
    return view