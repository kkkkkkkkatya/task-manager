import os

from .base import *


ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
DEBUG = os.getenv("DEBUG", "False") == "True"




# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ['POSTGRES_DB'],
        "USER": os.environ['POSTGRES_USER'],
        "PASSWORD": os.environ['POSTGRES_PASSWORD'],
        "HOST": os.environ['POSTGRES_HOST'],
        "PORT": int(os.environ['POSTGRES_DB_PORT']),
    }
}
