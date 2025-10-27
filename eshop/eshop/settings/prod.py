from .base import *

DEBUG = False

ADMINS = [
    ('Bazarov A', 'bazaroffalex@gmail.com')
]

# Static and media settings
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# EMAIL SETTINGS
# Add your own or import

EMAIL_HOST = ''
EMAIL_PORT = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = ''

ALLOWED_HOSTS = ['*']