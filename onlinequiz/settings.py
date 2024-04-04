"""
Django settings for onlinequiz project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from django.http import HttpResponse
import os
from . info import *
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR=os.path.join(BASE_DIR,'static')
MEDIA_ROOT=os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = os.path.join(BASE_DIR, 'static')   #added later for deployment by ap
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# emailable settings
EMAIL_USE_TLS=EMAIL_USE_TLS
EMAIL_HOST=EMAIL_HOST
EMAIL_HOST_USER=EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=EMAIL_HOST_PASSWORD
EMAIL_PORT=EMAIL_PORT


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '@k0#p3kidu)yaaa3u1hplxz)f@^6xiy384*(+n@@s5x#1bx@m5'
SECRET_KEY = 'CHROMASTONE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['.vercel.app','localhsot','127.0.0.1','.new.sh']
ALLOWED_HOSTS = ['.vercel.app','localhost','127.0.0.1','.new.sh']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quiz',
    'teacher',
    'student',
    'widget_tweaks',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CSRF_COOKIE_SECURE=False
ROOT_URLCONF = 'onlinequiz.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'onlinequiz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

#Vercel Server
# Load environment variables from .env file
# DATABASE_URL = os.environ.get('DATABASE_URL')
# load_dotenv()
# DATABASES = {
#     'default': dj_database_url.config(default='DATABASE_URL')
#     }

DATABASE_URL = os.environ.get('DATABASE_URL')
load_dotenv()
DATABASES = {
    'default': dj_database_url.config(default='DATABASE_URL')
    }


# SuperBase Server
# DATABASES = {
#     'default': dj_database_url.config(default='postgres://postgres.bqskrvcdmroshhnjblwb:_mjM$xt$i79E8&r@aws-0-ap-south-1.pooler.supabase.com:6543/postgres')
# }

#postgresql-by arunanshu
# load_dotenv()
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('POSTGRES_DATABASE'),
#         'USER': os.getenv('POSTGRES_USER'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#         'HOST': os.getenv('POSTGRES_HOST'),
#         'PORT': os.getenv('POSTGRES_DB_PORT'),
#     }
# }

# Local Server
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# STATICFILES_DIRS=[
# STATIC_DIR,
#  ]

LOGIN_REDIRECT_URL='/afterlogin'
