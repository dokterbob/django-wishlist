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

# Disable translations - we're testing the app, not Django's translations
USE_I18N = False

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

TEMPLATE_CONTEXT_PROCESSORS = (
    # Defaults
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',

    # Wishlist context processor
    'wishlist.context_processors.wishlist_items'
)

WISHLIST_ITEM_MODEL = 'tests.TestItemModel'
