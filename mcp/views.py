from django.contrib import auth
from django.shortcuts import redirect
from ttr.util import *
from .forms import *

def login(request):
    # Check to make sure the user isn't logged in, and redirect if they are
    if request.user.is_authenticated():
        return redirect(request.GET.get('next', 'mcp:panel'))

    # If the request is POST, let's try to process their log in information
    context = {}
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            if user.is_active:
                if user.level >= 200:
                    # Before we create the login cookie, check whether or not "Remember Me" was checked
                    print request.POST.get('remember_me')
                    if request.POST.get('remember_me') != "on":
                        # It wasn't checked, so tell the cookie to expire when the browser closes
                        request.session.set_expiry(0)

                    # Login and redirect to '/' if a next parameter wasn't passed
                    auth.login(request, user)
                    return redirect(request.GET.get('next', 'mcp:panel'))
                else:
                    context = dict(auth_message_type='warning', auth_message='You are not authorized to come in here.')
            else:
                context = dict(auth_message_type='warning', auth_message='Your account was disabled by the administrator.')
        else:
            context = dict(auth_message_type='warning', auth_message='Your username or password was incorrect.')

    # The request isn't POST, or auth failed, display the log in page
    return render_template(request, 'mcp/login.html', context)

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
        'permissions': permissions,
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