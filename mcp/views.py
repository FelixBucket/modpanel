from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect
from ttr.util import *
from .forms import *

def login(request):
    # Check to make sure the user isn't logged in, and redirect if they are
    if request.user.is_authenticated():
        return redirect(request.GET.get('next', 'mcp:panel'))

    return render_template(request, 'mcp/login.html')

def logout(request):
    # Logout and redirect to login screen
    context = {}
    if request.user.is_authenticated():
        context = dict(auth_message_type='info', auth_message='Bye ' + request.user.get_short_name() + ', see you around!')
        auth.logout(request)
    return render_template(request, 'mcp/login.html', context)

def app(request):
    # Load permissions
    permissions = request.user.get_permissions()

    return render_template(request, 'mcp/app.html', {
        'user': {
            'id': request.user.id,
            'mini_name': request.user.get_mini_name(),
            'short_name': request.user.get_short_name(),
            'long_name': request.user.get_long_name(),
            'avatar': request.user.mod_profile.avatar,
            'email': request.user.email,
            'level': request.user.level,
        },
        'permissions': permissions,
        'version': settings.VERSION,
        'pusher_key_id': settings.PUSHER_KEY_ID,
    })

def first_time(request):
    # If the user already has a mod profile, send them right in
    if hasattr(request.user, 'mod_profile'):
        return redirect('mcp:panel')

    # If the request is POST, let's try to process their additional information
    context = {}
    if request.method == 'POST':
        post = request.POST.copy()
        post['user'] = request.user.id
        form = ModProfileForm(post)
        try:
            profile = form.save()
            return redirect('mcp:panel')
        except:
            context = dict(auth_message_type='warning', auth_message='Please fill out all the fields. You can make up information if you like.')

    return render_template(request, 'mcp/first_time.html', context)