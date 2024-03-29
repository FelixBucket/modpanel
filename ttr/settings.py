"""
Django settings for ttr project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dqd@s+8b(cxmupv7*i$*=y!l0ddo&eybq$s17@hlj8c3h27=jh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']


# Application definition
DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
THIRD_PARTY_APPS = (
    'south',
    'tastypie',
)
LOCAL_APPS = (
    'ttr',
    'mcp',
)
INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'ttr.middleware.ttr_middleware.RequireLoginMiddleware',
    'ttr.middleware.ttr_middleware.RequireModProfile',
)

ROOT_URLCONF = 'ttr.urls'

WSGI_APPLICATION = 'ttr.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
VERSION = '41'
STATIC_ROOT = BASE_DIR + '/static/'
STATIC_URL = '/static/' + VERSION + '/'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
import dj_database_url
DATABASES = {'default': dj_database_url.config()}
DATABASES['default']['CONN_MAX_AGE'] = None

# Users and Auth

AUTH_USER_MODEL = 'ttr.User'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'ttr.two_factor_auth.TwoFactorAuthBackend')
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher', # Force compatibility with Play
)

# Automatic Login Required URLs
LOGIN_URL = '/login/'

LOGIN_REQUIRED_URLS = (
    r'/(.*)$',
)
LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    r'/api/v1/login/$',
    r'/login(.*)$',
    r'/logout(.*)$',
    STATIC_URL,
)

# Mod Profile Requirement
MODP_CREATE_URL = 'mcp:first_time'

MODP_REQUIRED_URLS = (
    r'/(.*)$',
)
MODP_REQUIRED_URLS_EXCEPTIONS = (
    r'/api/v1/login/$',
    r'/login(.*)$',
    r'/logout(.*)$',
    r'/first_time/$',
    STATIC_URL,
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Tastypie
TASTYPIE_DEFAULT_FORMATS = ['json']

# Pusher Settings
# Default to dev settings if env variable is not set
PUSHER_APP_ID = os.environ.get('PUSHER_APP_ID', '85566')
PUSHER_KEY_ID = os.environ.get('PUSHER_KEY_ID', 'a15e68a0fae7ee180ce2')
PUSHER_SECRET = os.environ.get('PUSHER_SECRET', '1d25d81aa43375f641ac')
PUSHER_LIB = '//js.pusher.com/2.2/pusher.min'

# RPC Settings
RPC_ENDPOINT = os.environ.get('RPC_ENDPOINT', '')
RPC_USERNAME = os.environ.get('RPC_USERNAME', '')
RPC_PASSWORD = os.environ.get('RPC_PASSWORD', '')

# Kibana Settings
KIBANA_ROOT = os.environ.get('KIBANA_ROOT', '')
KIBANA_USERNAME = os.environ.get('KIBANA_USERNAME', '')
KIBANA_PASSWORD = os.environ.get('KIBANA_PASSWORD', '')
