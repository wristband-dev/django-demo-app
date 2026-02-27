"""
Django settings for demo_project.

Using quick-start development settings which are unsuitable for production!!

See: https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

WRISTBAND SETUP GUIDE:
----------------------
Minimal Setup (required):
  - WRISTBAND_AUTH: SDK configuration
  - SESSION_ENGINE: Encrypted cookie-based sessions
  - WRISTBAND_SESSION_SECRET: Session encryption key
  - SessionMiddleware in MIDDLEWARE

CSRF Token Protection (optional):
  - CsrfViewMiddleware in MIDDLEWARE
  - CSRF_COOKIE_AGE and CSRF_COOKIE_SECURE: matches Session cookie configurations

Django User Integration (optional):
  - django.contrib.auth in INSTALLED_APPS
  - django.contrib.admin in INSTALLED_APPS (for admin panel)
  - AuthenticationMiddleware in MIDDLEWARE
  - AUTHENTICATION_BACKENDS with WristbandAuthBackend
  - DATABASES to store User objects
  - WRISTBAND_ADAPTER for custom role mapping
  - django.contrib.auth.context_processors.auth in TEMPLATES (for admin panel)

Template Integration (optional):
  - Custom context processor to expose auth data in templates

All Wristband-related settings are marked with __WRISTBAND__ comments throughout this file.
"""

import os
import warnings
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project (i.e., BASE_DIR / 'subdir')
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-demo-key-change-in-production"  # nosec B105 - Demo only, not for production

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",  # <-- Add this if you need access to Django's User model
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "demo_app",  # <-- This is the current Wristband demo app.
]

AUTHENTICATION_BACKENDS = [
    "wristband.django_auth.WristbandAuthBackend",  # __WRISTBAND__: Use only for Django User integration (optional)
]

# __WRISTBAND__: Custom adapter for role mapping when using the Wristband auth backend (optional)
WRISTBAND_AUTH_BACKEND_ADAPTER = "demo_app.adapters.MyWristbandAdapter"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",  # <-- Enables session support
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  # <-- Enforce CSRF protection (optional)
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # <-- Set Django User on "request.user" (optional)
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "demo_project.urls"
ASGI_APPLICATION = "demo_project.asgi.application"
# WSGI_APPLICATION = "demo_project.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",  # <-- Needed for Admin Panel
                "demo_app.context_processors.wristband_auth",  # <-- Adds authenticated user data to Django templates
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# __WRISTBAND__: Database required when using WristbandAuthBackend to store Django User objects (optional)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    # __WRISTBAND__: Enable debug logging statements in the Wristband SDK in development (optional).
    # IMPORTANT: Remove Wristband logging in Production!!
    "loggers": {
        "wristband": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Suppress the StreamingHttpResponse warning in development
if DEBUG:
    warnings.filterwarnings(
        "ignore",
        message="StreamingHttpResponse must consume synchronous iterators in order to serve them asynchronously",
        category=Warning,
        module="django.core.handlers.asgi",
    )

# __WRISTBAND__: Wristband Django Auth SDK Configurations.
WRISTBAND_AUTH = {
    "client_id": os.environ.get("CLIENT_ID"),
    "client_secret": os.environ.get("CLIENT_SECRET"),
    "wristband_application_vanity_domain": os.environ.get("APPLICATION_VANITY_DOMAIN"),
    "dangerously_disable_secure_cookies": True,  # IMPORTANT: Set to False in Production!!
    "scopes": ["openid", "offline_access", "email", "profile", "roles"],
}

# __WRISTBAND__: Django Session Configurations
SESSION_ENGINE = "wristband.django_auth.sessions.backends.encrypted_cookies"  # Enables encrypted session cookies
SESSION_COOKIE_AGE = 3600  # 1 hour of inactivity
SESSION_COOKIE_SECURE = False  # IMPORTANT: Set to True in Production!!
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_SAMESITE = "Lax"  # Reasonably secure default option
# IMPORTANT: In production, use a strong, randomly-generated secret (32+ characters)!!
WRISTBAND_SESSION_SECRET = "dummy_67f44f4964e6c998dee827110c"  # nosec B105 - Demo only, not for production

# __WRISTBAND__: CSRF Configurations (Optional)
CSRF_COOKIE_AGE = 3600  # 1 hour (make value the same as SESSION_COOKIE_AGE)
CSRF_COOKIE_SECURE = False  # IMPORTANT: Set to True in Production!!
