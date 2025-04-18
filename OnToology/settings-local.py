"""
Django settings for OnToology project.

This is for running automated tests
"""

from .settings import *

os.environ['OnToology_home'] = "true"
local = True
host = 'http://127.0.0.1:8000'
client_id = GITHUB_LOCAL_APP_ID
client_secret = GITHUB_LOCAL_API_SECRET
print("Going local")
DEBUG = True

print("environ: ")
print(os.environ)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'OnToology.db',
#     }
# }

test_conf = {'local': False,  # doing test
             'fork': False,  # perform fork
             'clone': False,  # perform clone
             'push': False,  # push the changes to GitHub
             'pull': False,  # to create a pull request from the forked on
             }


GITHUB_LOCAL_APP_ID = '3995f5db01f035de44c6'
GITHUB_LOCAL_API_SECRET = '141f896e53db4a4427db177f1ef2c9975e8a3c1f'

environ['setting_module'] = "OnToology.settings-local"



os.environ['test_local'] = "false"