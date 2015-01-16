"""
Django settings for orca project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from orca.tools import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0@u(nff$0&g&ml3#sznrix3cg60_4^5reknu+%8^m=_&y%b(7w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'madlee',
    'orca',
    'pyxis',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'orca.urls'

WSGI_APPLICATION = 'orca.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db/orca.db'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (r'C:/Madlee/Incoming/Program/HTML5/static/', r'D:/Incoming/Program/HTML5/static/', r'/home/lifeng/html/static/', '../../html/static/')

REST_FRAMEWORK = {
    'PAGINATE_BY': 50,                 # Default to 10
    'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100,            # Maximum--0 limit allowed when using `?page_size=xxx`.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ), 
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

#Base folder for all databases. Should been created before execute.
ORCA_DB_PATH = r"db"

ORCA_CACHE_PATH = r"cache"

# Tune for performance
ORCA_DB_PRAGMA = """PRAGMA synchronous=OFF;
PRAGMA journal_mode=MEMORY;
PRAGMA cache_size=-100000;
PRAGMA locking_mode=EXCLUSIVE;
"""

ORCA_KDAY_SOURCE = 'jydb/jydb@jydb'

ORCA_NLS_LANG = 'AMERICAN_AMERICA.UTF8'

ORCA_REFRESH_HINTS = {
    'SDAY': ORCA_KDAY_SOURCE
}

ORCA_DATE_0 = Date(2000, 1, 1)
