"""
Django settings for OnToology project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)

LOGIN_URL = '/login'




#Needed for the tests
TEST_RUNNER = 'OnToology.tests.NoSQLTestRunner'



#The below 5 lines are used for login with facebook purposes
#SOCIAL_AUTH_MODELS = 'social_auth.db.mongoengine_models'
#SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
GITHUB_APP_ID = 'bbfc39dd5b6065bbe53b'
GITHUB_API_SECRET = '60014ba718601441f542213855607810573c391e'
GITHUB_LOCAL_APP_ID = '3995f5db01f035de44c6'
GITHUB_LOCAL_API_SECRET = '141f896e53db4a4427db177f1ef2c9975e8a3c1f'



client_id = GITHUB_APP_ID#'bbfc39dd5b6065bbe53b'
client_secret = GITHUB_API_SECRET#'60014ba718601441f542213855607810573c391e'
host = 'http://54.172.63.231'
local=False
if 'OnToology_home' in os.environ and os.environ['OnToology_home'].lower()=="true":
    local=True
    host = 'http://127.0.0.1:8000'
    client_id = GITHUB_LOCAL_APP_ID
    client_secret = GITHUB_LOCAL_API_SECRET




from mongoengine import connect
connect("OnToology")




AUTH_USER_MODEL = 'mongo_auth.MongoUser'
MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'
SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xj1c63qiywswa67s))0$fel(z5@=%(br!j)u155a71j*^u_b+2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    BASE_DIR+'/templates',
)

MEDIA_ROOT = BASE_DIR+'/media/'

MEDIA_URL = '/media/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mongoengine.django.mongo_auth',
    'OnToology',
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


TEMPLATE_CONTEXT_PROCESSORS=(
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request"
)

ROOT_URLCONF = 'OnToology.urls'

WSGI_APPLICATION = 'OnToology.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
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
