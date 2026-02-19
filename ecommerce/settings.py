"""
Django settings for ecommerce project.
"""

from pathlib import Path
from datetime import timedelta
from decouple import config

# --------------------------------------------------
# BASE DIR
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# SECURITY
# --------------------------------------------------
SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = config("DJANGO_DEBUG", cast=bool)

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS").split(",")

# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    "corsheaders",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",

    "users",
    "products",
    "cart",
    "wishlist",
   'orders.apps.OrdersConfig',
    "admin_manage"
]

# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------
# URLS / WSGI
# --------------------------------------------------
ROOT_URLCONF = "ecommerce.urls"
WSGI_APPLICATION = "ecommerce.wsgi.application"

# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --------------------------------------------------
# DATABASE (PostgreSQL)
# --------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# STATIC & MEDIA
# --------------------------------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------
# DEFAULT PRIMARY KEY
# --------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------
# DJANGO REST FRAMEWORK
# --------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# --------------------------------------------------
# SIMPLE JWT
# --------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        days=config("ACCESS_TOKEN_LIFETIME_DAYS", cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config("REFRESH_TOKEN_LIFETIME_DAYS", cast=int)
    ),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "BLACKLIST_AFTER_ROTATION": True,
}

# --------------------------------------------------
# RAZORPAY
# --------------------------------------------------
RAZORPAY_KEY_ID = config("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = config("RAZORPAY_KEY_SECRET")

# --------------------------------------------------
# CORS
# --------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", cast=bool)
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# --------------------------------------------------
# EMAIL (SMTP - GMAIL)
# --------------------------------------------------
EMAIL_BACKEND = config("EMAIL_BACKEND")

EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)

EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_USE_SSL = False

EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
EMAIL_TIMEOUT = 30

import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

cloudinary.config(
  cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
  api_key=os.getenv("CLOUDINARY_API_KEY"),
  api_secret=os.getenv("CLOUDINARY_API_SECRET")
)
