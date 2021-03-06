"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

from .common import *
from boto3.session import Session
import boto3
from boto3.dynamodb.conditions import Key, Attr
import django_filters
import environ

DEBUG = True
# 環境変数でDJANGO_READ_ENV_FILEをTrueにしておくと.envを読んでくれる。
# READ_ENV_FILE = env.bool('DJANGO_READ_ENV_FILE', default=False)
BASE_DIR = environ.Path(__file__) - 3
env = environ.Env()
env_file = str(BASE_DIR.path('.env'))
env.read_env(env_file)

ALLOWED_HOSTS = ['*']
SECRET_KEY = env('SECRET_KEY')

CORS_ORIGIN_WHITELIST = (
    'localhost:1234/',
    'localhost:1234',
    '127.0.0.1:1234/',
    '127.0.0.1:1234',
)

DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE'),
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'OPTIONS': env.json('DATABASE_OPTIONS', default={'charset': 'utf8'}),
        'ATOMIC_REQUESTS': env('DATABASE_ATOMIC_REQUESTS')
    }
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# client = boto3.resource('dynamodb')
#
# response = client.Table('Users')
# print(response.scan())