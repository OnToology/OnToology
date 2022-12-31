#################################################################
#           To make this app compatible with Django             #
#################################################################
import os
import sys


proj_path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
# venv_python = os.path.join(proj_path, '..', '.venv', 'bin', 'python')
# This is so Django knows where to find stuff.
sys.path.append(os.path.join(proj_path, '..'))



def load(setting_module):
    """
    setting_module: (e.g., "OnToology.settings")
    """
    global application
    print("loading setting module: "+setting_module)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_module)
    sys.path.append(proj_path)

    # This is so my local_settings.py gets loaded.
    os.chdir(proj_path)

    # This is so models get loaded.
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()

#################################################################
