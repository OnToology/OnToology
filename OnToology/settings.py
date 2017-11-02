#
# Copyright 2012-2013 Ontology Engineering Group, Universidad Politecnica de Madrid, Spain
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @author Ahmad Alobaid
#

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
print 'BASE_DIR: '+BASE_DIR

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)

LOGIN_URL = '/login'


#Needed for the tests
TEST_RUNNER = 'OnToology.tests.__init__.NoSQLTestRunner'


#The below 5 lines are used for login with facebook purposes
#SOCIAL_AUTH_MODELS = 'social_auth.db.mongoengine_models'
#SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
GITHUB_APP_ID = 'bbfc39dd5b6065bbe53b'
GITHUB_API_SECRET = '60014ba718601441f542213855607810573c391e'
GITHUB_LOCAL_APP_ID = '3995f5db01f035de44c6'
GITHUB_LOCAL_API_SECRET = '141f896e53db4a4427db177f1ef2c9975e8a3c1f'


try:
    from localwsgi import *
    print "importing environ from local wsgi"
except:
    print "no local wsgi"



# client_id_login = os.environ['client_id_login']       # 'e2ea731b481438fd1675'
# client_id_public = os.environ['client_id_public']     # '878434ff1065b7fa5b92'
# client_id_private = os.environ['client_id_private']   # 'dd002c8587d08edfaf5f'
#
# client_secret_login = os.environ['client_secret_login']        # 'ba0f149934e3d78816cbd89d1f3c5109b82898ab'
# client_secret_public = os.environ['client_secret_public']       # 'c76144cbbbf5df080df0232928af9811d78792dd'
# client_secret_private = os.environ['client_secret_private']      # 'c5fbaa760362ba23f7c8d07c35021ac111ca5418'
# client_id = GITHUB_APP_ID  # 'bbfc39dd5b6065bbe53b'
# client_secret = GITHUB_API_SECRET  # '60014ba718601441f542213855607810573c391e'
# host = 'http://54.172.63.231'


host = 'http://ontoology.linkeddata.es'
local = False
if 'OnToology_home' in os.environ and os.environ['OnToology_home'].lower() == "true":
    local = True
    host = 'http://127.0.0.1:8000'
    client_id = GITHUB_LOCAL_APP_ID
    client_secret = GITHUB_LOCAL_API_SECRET
    print "Going local"
else:
    print "Going remote"
    print os.environ

TEST = False

from mongoengine import connect

MONGO_DATABASE_NAME = "OnToology"
if 'db_username' not in os.environ or os.environ['db_username'].strip() == '':
    print "no auth"
    connect(MONGO_DATABASE_NAME)
else:
    print "with auth"
    connect(MONGO_DATABASE_NAME, host=os.environ['db_host'], port=int(os.environ['db_port']),
            username=os.environ['db_username'], password=os.environ['db_password'],
            )
            #authentication_mechanism='MONGODB-CR')
            #authentication_mechanism='SCRAM-SHA-1')


AUTH_USER_MODEL = 'mongo_auth.MongoUser'
MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'
SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xj1c6fel(z5@=%(br!j)u155a71j*^u_b+2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DEFAULT_FROM_EMAIL = os.environ['email_from']
EMAIL_HOST = os.environ['email_server']
EMAIL_HOST_PASSWORD = os.environ['email_password']
EMAIL_HOST_USER = os.environ['email_username']
SERVER_EMAIL = DEFAULT_FROM_EMAIL
#SERVER_EMAIL = 'ontoology@delicias.dia.fi.upm.es'

print DEFAULT_FROM_EMAIL
print EMAIL_HOST
print EMAIL_HOST_PASSWORD
print EMAIL_HOST_USER
print SERVER_EMAIL

ADMINS = (('Ahmad', 'aalobaid@fi.upm.es'), )

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

TEMPLATE_DIRS = (
    BASE_DIR+'/templates',
)

MEDIA_ROOT = BASE_DIR+'/media/'

MEDIA_URL = '/media/'

    
test_conf = {'local': False  # don't interact with github at all, just mimic
             
             }
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
    #'django.middleware.csrf.CsrfViewMiddleware',
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
