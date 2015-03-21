"""
WSGI config for Auton project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Auton.settings")

from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()


#The below is to fix environment variables with apache
#resource http://ericplumb.com/blog/passing-apache-environment-variables-to-django-via-mod_wsgi.html

_application = get_wsgi_application()

env_variables_to_pass = ['github_username', 'github_password', 'github_repos_dir' ,'ar2dtool_dir', 'ar2dtool_config']
def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    for var in env_variables_to_pass:
        os.environ[var] = environ.get(var, '')
    return _application(environ, start_response)

