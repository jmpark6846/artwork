from .base import *
print('local settings loaded')
DEBUG = True

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3"
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
