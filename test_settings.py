DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django_nose',
    'wishlist.tests',
    'wishlist',
]

ROOT_URLCONF = 'wishlist.urls'

SITE_ID = 1

# Enable time-zone support for Django 1.4 (ignored in older versions)
USE_TZ = True

# Generate random secret key
import random
SECRET_KEY = ''.join([
    random.SystemRandom().choice(
        'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    ) for i in range(50)
])

# Use nose for tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Nose defaults
NOSE_ARGS = [
    '--detailed-errors', '--logging-level=INFO', '--with-yanc',
    '--with-coverage', '--cover-package=wishlist'
]

# Required for django-webtest to work
STATIC_URL = '/static/'

WISHLIST_ITEM_MODEL = 'tests.TestItemModel'
