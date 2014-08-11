from ttr.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'toontownrewritten_dev',
        'USER': 'ttr_dev_user',
        'PASSWORD': 'this_is_so_secure_it_blows_your_mind',
        'HOST': '23.92.16.247',
        'PORT': '3306',
    }
}