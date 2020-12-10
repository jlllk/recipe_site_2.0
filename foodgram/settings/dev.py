from .base import *

DEBUG = True
SITE_ID = 1
SECRET_KEY = 'vfd%qdcj&p-)5t@wnbjom*f8)k!n4g_mawmfk7-@p#wx-+ik1='
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}