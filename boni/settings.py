import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-zt2=b#$pdi21fg_$8o@tgk_a1^ae2$4@_z4%%3035@561!!=64'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['188.166.156.212']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CUstom apps
    'account',
    'events',
    'mainapp',
    'qr_code',
]

AUTH_USER_MODEL = 'account.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'boni.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'boni.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bonspy2',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT=os.path.join(BASE_DIR,"media")
MEDIA_URL='/media/'


LOGIN_REDIRECT_URL="mainapp:home"
LOGIN_URL="mainapp:home"
LOGOUT_URL = 'account:logout'


EMAIL_BACKEND= 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT= 587
EMAIL_USE_TLS= True
EMAIL_HOST_USER = "netrobeweb@gmail.com"
EMAIL_HOST_PASSWORD = "wpcgtxfwmiqnlbwv"
# Custom user defined mail username
DEFAULT_FROM_EMAIL = "bonspiels@gmail.com"
DEFAULT_COMPANY_EMAIL = "bonspiels@gmail.com"


# Field conf
INFORMATION_TOOLS_REQUIRED_SUFFIX = '-R1'
INFORMATION_TOOLS = [
    {
        'name': 'Team name',
        'form_name': 'team_name',
        'type': 'text',
    },
    {
        'name': 'Team email',
        'form_name': 'team_email',
        'type': 'email',
    },
    {
        'name': 'Team phone',
        'form_name': 'team_phone',
        'type': 'text',
    },
    # {
    #     'name': 'Team id card',
    #     'form_name': 'team_id_card',
    #     'type': 'file',
    # },
    {
        'name': 'Region/Country',
        'form_name': 'region_country',
        'type': 'text',
    },
    {
        'name': 'Curling club',
        'form_name': 'curling_club',
        'type': 'text',
    },
    {
        'name': 'Line up',
        'form_name': 'line_up',
        'type': 'multiple_text_box',
    },
]