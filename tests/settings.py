# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "8bhf=t3yt!9q!lf&7zpdd85)ffjudj5em_^c&u^6o0+0oodf_t"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        'NAME': 'mentions',  # Or path to database file if using sqlite3.
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "rest_framework",
    # Apps for Testing
    "model_mommy",
    "tests",
    # Main app
    "mentions",
]

SITE_ID = 1

_MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
)

if django.VERSION >= (1, 10):
    MIDDLEWARE = _MIDDLEWARE_CLASSES
else:
    MIDDLEWARE_CLASSES = _MIDDLEWARE_CLASSES
