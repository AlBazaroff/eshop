from .base import *

DEBUG = True

# For development, web is necessary for stripe
ALLOWED_HOSTS = ['*']

# for testing password reset
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'