# -*- coding: utf-8 -*-
import django.conf
import environ
import os
import warnings

# Env file setup
ROOT = environ.Path(__file__) - 2   # 2 directories up = tarteel.io/
BASE_DIR = ROOT()

# Defaults
USE_DEV_DB = False
USE_PROD_DB = False
USE_LOCAL_DB = False
LOCAL_DEV = False

env = environ.Env()
env.read_env(str(ROOT.path('tarteel/.env')))


ALLOWED_HOSTS = ['www.tarteel.io', 'tarteel.io', '.tarteel.io', '0.0.0.0', '127.0.0.1',
                 'www.api-dev.tarteel.io', 'api-dev.tarteel.io', 'apiv1.tarteel.io',
                 'www.apiv1.tarteel.io',
                 env('EC2_IP', str, default=''), env('EC2_IP1', str, default=''),
                 env('EC2_IP2', str, default=''), env('ELB_IP', str, default=''),
                 env('PROD_GW_IP', str, default=''), env('DEV_GW_IP', str, default=''),
                 'testserver', 'localhost']


# GENERAL
# ------------------------------------------------------------------------------
SECRET_KEY = env('SECRET_KEY', str, default='development_security_key')
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# DEBUG = env('DEBUG', bool, default=True)
# Get the settings from zappa_settings.json
if 'SERVERTYPE' in os.environ and os.environ['SERVERTYPE'] == 'AWS Lambda':
    # Don't use the local DB if in dev/prod
    USE_LOCAL_DB = False
    # In dev and prod environments, DEBUG is always False. Local is True
    DEBUG = False
    # Use dev or prod DB accordingly
    if "DEV_DB" in os.environ and (os.environ.get("DEV_DB") == "true"):
        USE_DEV_DB = True
    elif "PROD_DB" in os.environ and (os.environ.get("PROD_DB") == "true"):
        USE_PROD_DB = True
# Local development instead
else:
    LOCAL_DEV = True
    USE_DEV_DB = True

# Local time zone: http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = env('TIME_ZONE', str, default='UTC')
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = env('LANGUAGE_CODE', str, default='en-us')
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = env('USE_I18N', bool, default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = env('USE_L10N', bool, default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = env('USE_TZ', bool, default=True)
# Main site (1, tarteel.io) if local env, else (2, 127.0.0.1/localhost)
SITE_ID = 2 if DEBUG else 1

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/howto/initial-data/
# Use this to set JSON files which initialize defaults (usually for testing)
# FIXTURE_DIRS = [
#     ROOT('tarteel/fixtures'),
# ]

# Set the sites migration folders locally to create default site changes for
# authentication testing. socialaccount added b/c it it depends on sites.
MIGRATION_MODULES = {
    'sites': 'tarteel.fixtures.sites_migrations',
    'socialaccount': 'tarteel.fixtures.socialaccount_migrations'
}

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'django_filters',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.github',
]
LOCAL_APPS = [
    'restapi',
    'evaluation',
    'iqra',
    'quran',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',        # CORS
    'django.middleware.csrf.CsrfViewMiddleware',    # CSRF
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'tarteel.urls'
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'tarteel.wsgi.application'


# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
if USE_PROD_DB:
    DATABASES = {'default': env.db('PSQL_URL')}
elif USE_DEV_DB:
    DATABASES = {'default': env.db('PSQL_DEV_URL')}
elif USE_LOCAL_DB:
    DATABASES = {'default': env.db('SQLITE_URL')}


# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
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
# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Django Allauth Configs
# https://django-allauth.readthedocs.io/en/latest/configuration.html
# Dictionary containing provider specific settings.
""" Commented out until regular auth fully setup
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
            'read:user'
        ],
    },
    # https://django-allauth.readthedocs.io/en/latest/providers.html#facebook
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'default'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'en_US',  # Temp return just US
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.12',
    }
}
"""
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
# LOGIN_URL = env('LOGIN_URL')
# LOGOUT_URL = env('LOGOUT_URL')
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = env('LOGIN_REDIRECT_URL', str, '/accounts/profile/')
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# Development env. has email printed to console. Production uses actual email server
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST', str, 'smtp.gmail.com')
EMAIL_PORT = env('EMAIL_PORT', int, 465)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', str, 'contact.tarteel@gmail.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', str, 'mysupersecretpassword')

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = ROOT('static')
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = ROOT('media')
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'


# AWS
# --------------------------------------
# https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', str, 'tarteel-frontend-dev')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', str, '')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', str, '')
AWS_QUERYSTRING_EXPIRE = env('AWS_QUERYSTRING_EXPIRE', str, '157784630')
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE', str,
                           'django.core.files.storage.FileSystemStorage')

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ROOT('templates')],
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

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        # 'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# django-corsheader
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# SECURITY
PREPEND_WWW = env('PREPEND_WWW', bool, default=False)
# HTTPS Redirect
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Different settings for local env due to https/CSRF issues
if LOCAL_DEV:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT', bool, default=False)
    SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE', bool, default=False)
    CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', bool, default=False)
