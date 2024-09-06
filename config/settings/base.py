"""
Django settings Created all base file by cookiecutter.

Generated by 'django-admin startproject' using Django 5.0.7.
"""

# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
import os
from pathlib import Path
from dotenv import load_dotenv


dotenv_path = Path(".env")
if dotenv_path.exists():
    load_dotenv(dotenv_path, override=True)
else:
    print("Don't Exists .env file")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = os.getenv("DEBUG", "False") == "True"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "default_se@cret_key@#$fa")


THIRD_PARTY_APPS = [
    
    "django_extensions",
    "rest_framework",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
    
    
    
    
]
LOCAL_APPS = [
    "apps.sample.apps.SampleConfig",
    "apps.account.apps.AccountConfig",
    
    "apps.api.apps.ApiConfig",
    
    
]
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    
    "corsheaders.middleware.CorsMiddleware",
    
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASE_URL = os.getenv("DATABASE_URL")
from urllib.parse import urlparse

url = urlparse(DATABASE_URL)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": url.path[1:],
        "USER": url.username,
        "PASSWORD": url.password,
        "HOST": url.hostname,
        "PORT": url.port,
    }
}

# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = "fa-ir"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
# STORAGES = {
#     "default": {
#         "BACKEND": "django.core.files.storage.FileSystemStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CACHES = {
    
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_LOCATION", "redis://localhost:6379"),
    }
    
}

LOGGING_LEVEL = "DEBUG" if DEBUG else "INFO"
LOGGING_FILE_PATH_ERROR = BASE_DIR / "logs" / "err.log"
LOGGING_FILE_PATH_INFO = BASE_DIR / "logs" / "main.log"

os.makedirs(os.path.dirname(LOGGING_FILE_PATH_ERROR), exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname}-{asctime}-{module}-{message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname}-{message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": LOGGING_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file_warning_error": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": LOGGING_FILE_PATH_ERROR,
            "formatter": "verbose",
        },
        "file_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOGGING_FILE_PATH_INFO,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file_warning_error", "file_info"],
            "level": "INFO",
            "propagate": False,
        },
        "application": {
            "handlers": ["console", "file_warning_error", "file_info"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
    },
}

SITE_ID = 1

AUTH_USER_MODEL = "account.User"
# LOGIN_URL = "account:login"

from .other.email import *

from .other.drf import *
from .other.cors import *
from .other.spectacular import *
from .other.jwt import *





