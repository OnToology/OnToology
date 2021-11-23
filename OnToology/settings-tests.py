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


DATABASES = {
    'default': {

    }
}



try:
    from OnToology.localwsgi import environ  # as environabc
    print("\\\\*****\\\\\\*****\n\n\n\n\n****")
    for k in environ:
        print(k+" abc--> "+str(environ[k]))
    test_conf = {
        'local': environ['test_local'].strip().lower() =="true",  # doing test
        'fork': environ['test_fork'].strip().lower() =="true",  # perform fork
        'clone': environ['test_clone'].strip().lower() =="true",  # perform clone
        'push': environ['test_push'].strip().lower() =="true",  # push the changes to GitHub
        'pull': environ['test_pull'].strip().lower() =="true",  # to create a pull request from the forked on
    }
    print("importing environ from local wsgi")
except Exception as e:
    print("settings> no1 OnToology.local wsgi")
    print(e)
    import traceback
    traceback.print_exc()

    test_conf = {'local': False,  # doing test
                 'fork': False,  # perform fork
                 'clone': False,  # perform clone
                 'push': False,  # push the changes to GitHub
                 'pull': False,  # to create a pull request from the forked on
    }
    try:
        from OnToology.localwsgi import *
    except Exception as e:
        print("settings> no2 local_wsgi")
        raise Exception("Force local wsgi load")

environ = os.environ
print("environ: ")


db_name = environ['db_name']
if DEBUG:
    db_name_parts = db_name.split('.')
    db_name = ".".join(db_name_parts[:-1] + ["test"] + [db_name_parts[-1]])
    # db_name += "test"
DATABASES['default']['NAME'] = db_name

DATABASES['default']['ENGINE'] = environ['db_engine']
if 'db_password' in environ:
    DATABASES['default']['PASSWORD'] = environ['db_password']

if 'db_username' in environ:
    DATABASES['default']['USER'] = environ['db_username']

if 'db_host' in environ:
    print("yes db_host in environ")
    host_db = environ['db_host']
    DATABASES['default']['HOST'] = host_db
    if 'db_port' in environ:
        DATABASES['default']['PORT'] = environ['db_port']
else:
    print("db_host is not in environ")


environ['setting_module'] = "OnToology.settings-tests"