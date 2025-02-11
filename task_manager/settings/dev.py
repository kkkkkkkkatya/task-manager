from .base import *


ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
DEBUG = os.getenv("DEBUG", "False") == "True"




# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
