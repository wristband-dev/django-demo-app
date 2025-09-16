"""
Django settings for demo_project.

Using quick-start development settings - unsuitable for production!

See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
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
SECRET_KEY = "django-insecure-demo-key-change-in-production"  # nosec B105

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "demo_app",  # This is the current Wristband demo app.
]

# __WRISTBAND__: The following middlewares work in unison to protect this app:
# - SessionMiddleware: Django sessions will store authenticated user data.
# - CsrfViewMiddleware: Enforces Cross-Site Request Forgery (CSRF) protection.
# - AuthMiddleware: Defined in this app. Validates authenticated session and refreshes token, if needed.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "demo_app.auth_middleware.AuthMiddleware",
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
            # __WRISTBAND__: wristband_auth context processor adds auth data to Django templates
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "demo_app.context_processors.wristband_auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# __WRISTBAND__: Database (stores authenticated user sessions -- change accordingly for your setup!)
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
}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

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
    "dangerously_disable_secure_cookies": False,  # IMPORTANT: Set to True in Production!!
}

# __WRISTBAND__: Django Session Configurations
SESSION_SAVE_EVERY_REQUEST = True  # Keep a rolling session expiration time as long as user is active
SESSION_COOKIE_AGE = 3600  # 1 hour of inactivity
SESSION_COOKIE_SECURE = False  # IMPORTANT: Set to True in Production!!

# __WRISTBAND__: CSRF Configurations
CSRF_COOKIE_AGE = 3600  # 1 hour (same as session); auth middleware ensures session and csrf times stay in sync
CSRF_COOKIE_SECURE = False  # IMPORTANT: Set to True in Production!!
