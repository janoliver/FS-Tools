#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Django settings for vluserver project.

import django
import os

root = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
             'NAME': root + '/fstools.sqlite'}}

FORCE_SCRIPT_NAME = ''

TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'de-de'
SITE_ID = 1
USE_I18N = False
USE_L10N = True
USE_TZ = False
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

PAM_IS_SUPERUSER = True

STATICFILES_DIRS = (root + '/static', )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
    )

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'y1i8evr^^9xouthj0ku#e4*hl!83jp3bdacx(m-8v8zp3g0!v#'

# List of callables that know how to import templates from various sources.
JINJA_CONFIG = {
    'line_statement_prefix': '#',
    'line_comment_prefix'  : '##',
    'extensions' : ['jinja2.ext.autoescape']}

JINGO_EXCLUDE_APPS = ('admin','default','auth',)

TEMPLATE_LOADERS = (
    'jingo.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader')

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
    )

ROOT_URLCONF = 'fstools.urls'

LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = ('fstools.extensions.dpam.backends.PAMBackend', )

INSTALLED_APPS = (  # 'django_extensions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'eval',
    'rhp',
    'protokoll',
    'umfrage',
    'default',
    'ppp'
    )

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'mail_admins': {'level': 'ERROR',
                 'class': 'django.utils.log.AdminEmailHandler'}},
    'loggers': {'django.request': {'handlers': ['mail_admins'],
                'level': 'ERROR', 'propagate': True}},
    }

