from .base import *

# ADD debug debug_toolbar for debug

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

INTERNAL_IPS = [
    '127.0.0.1',
]

DEBUG = True

# For development, web is necessary for stripe
ALLOWED_HOSTS = ['*']

# for testing password reset
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'