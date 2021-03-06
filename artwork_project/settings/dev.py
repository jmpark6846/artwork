from .base import *
print('dev settings loaded')
DEBUG = True

DATABASES = {
    'default': {
        "ENGINE": "django_s3_sqlite",
        "NAME": "sqlite.db",
        "BUCKET": "artwork-db-bucket",
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
