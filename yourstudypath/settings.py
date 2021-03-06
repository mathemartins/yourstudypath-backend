"""
Django settings for yourstudypath project.

Generated by 'django-admin startproject' using Django 3.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import datetime
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1tn0vanm%#&f=hct$)b!2lvvd!makzu347$xj%fb2zip0qtzwk'  # os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # str(os.environ.get('DEBUG')) == "1"

ENV_ALLOWED_HOST = os.environ.get("ENV_ALLOWED_HOST")
ALLOWED_HOSTS = ['*']
BASE_URL = 'https://api.yourstudypath.com'
if ENV_ALLOWED_HOST:
    ALLOWED_HOSTS = [ENV_ALLOWED_HOST]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Third-party modules
INSTALLED_APPS += [
    'rest_framework',
    'rest_framework_jwt',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_swagger',
    'storages',
    'channels',
    'taggit',
    'taggit_serializer',
]

# Custom apps
INSTALLED_APPS += [
    'accounts',
    'core',
    'analytics',
    'categories',
    'courses',
    'search',
    'videos',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'
FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_ENDSESSION = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yourstudypath.urls'
# CORS_URLS_REGEX = r"^/api/.*"
# CORS_ALLOWED_ORIGINS = []

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = None
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_FRAME_DENY = False

# if DEBUG:
#     CORS_ALLOWED_ORIGINS += [
#         'http://localhost:8000',
#         'https://localhost:8000',
#         'https://ysp-staging.herokuapp.com',
#     ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = 'yourstudypath.asgi.application'
# WSGI_APPLICATION = 'yourstudypath.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DB_USERNAME = 'axrnboaffvbjmg'  # os.environ.get("POSTGRES_USER")
DB_PASSWORD = 'a8e223c11ff013c487c44ce1705f6c577a896a6023276492f45bc52cbdaa19d7'  # os.environ.get("POSTGRES_PASSWORD")
DB_DATABASE = 'd2hf6uiihfbr8b'  # os.environ.get("POSTGRES_DB")
DB_HOST = 'ec2-52-5-110-35.compute-1.amazonaws.com'  # os.environ.get("POSTGRES_HOST")
DB_PORT = '5432'

DB_IS_AVAIL = all([
    DB_USERNAME,
    DB_PASSWORD,
    DB_DATABASE,
    DB_HOST,
    DB_PORT
])

DB_IGNORE_SSL = os.environ.get("DB_IGNORE_SSL") == "true"

if DB_IS_AVAIL:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_DATABASE,
            "USER": DB_USERNAME,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }

    if not DB_IGNORE_SSL:
        DATABASES["default"]["OPTIONS"] = {
            "sslmode": "require"
        }

print(DATABASES)

CELERY_BROKER_URL = "rediss://default:KCAnYINTOypslB2a@private-db-redis-redis-do-user-10904361-0.b.db.ondigitalocean" \
                    ".com:25061 "
BROKER_URL = "rediss://default:KCAnYINTOypslB2a@private-db-redis-redis-do-user-10904361-0.b.db.ondigitalocean.com:25061"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_PASSWORD = "KCAnYINTOypslB2a"

CHANNEL_LAYERS = {
    # queue of messages
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': ["rediss://default:KCAnYINTOypslB2a@private-db-redis-redis-do-user-10904361-0.b.db"
                      ".ondigitalocean.com:25061"],
            'symmetric_encryption_keys': [SECRET_KEY],
        },
    },
}

AUTHENTICATION_BACKENDS = ['accounts.authentication.EmailBackend']

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_root'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# STATIC_ROOT = BASE_DIR / "staticfiles"
#
# STATICFILES_DIRS = [
#     BASE_DIR / "staticfiles"
# ]
# from yourstudypath.cdn.conf import *  # noqa
from yourstudypath.restconf import *  # noqa

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ["Bearer"],
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=30),  # minutes=5
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=30),  # days=1
}
