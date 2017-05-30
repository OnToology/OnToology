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
WSGI config for Auton project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OnToology.settings")

from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()


#The below is to fix environment variables with apache
#resource http://ericplumb.com/blog/passing-apache-environment-variables-to-django-via-mod_wsgi.html

_application = get_wsgi_application()

env_variables_to_pass = ['github_username', 'github_password', 'github_repos_dir', 'ar2dtool_dir', 'previsual_dir',
                         'wget_dir', 'tools_config_dir', 'widoco_dir', 'owl2jsonld_dir', 'SECRET_KEY',
                         'client_id_login', 'client_id_public', 'client_id_private',
                         'client_secret_login', 'client_secret_public', 'client_secret_private',
                         'publish_dir', 'tool_token', 'db_username', 'db_password', 'db_host', 'db_port'
                         ]


def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    print "wsgi environ"
    print os.environ
    for var in env_variables_to_pass:
        os.environ[var] = environ.get(var, '')
    return _application(environ, start_response)

