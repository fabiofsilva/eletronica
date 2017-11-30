# coding: utf-8
from production import *

DEBUG = True
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

INSTALLED_APPS.append('django_nose')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = ['--with-coverage', '--cover-package=eletronica.core']
