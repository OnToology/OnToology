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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'OnToology.db',
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
environ["github_username"] = "TEST_GITHUB_USERNAME"
environ["github_email"] = "test@example.com"
environ["publish_dir"] = "publish"
environ["github_repos_dir"] = "repos"
environ["previsual_dir"] = "prev"

environ['client_id_login'] = ""
environ['client_id_public'] = ""
environ['client_id_private'] = ""

environ['client_secret_login'] = ""
environ['client_secret_public'] = ""
environ['client_secret_private'] = ""

environ['SECRET_KEY'] = "ONTOOLOGY"

environ["test_local"] = ""

environ['setting_module'] = "OnToology.settings-tests"