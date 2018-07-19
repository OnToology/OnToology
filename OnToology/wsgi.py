
try:
    import OnToology.localwsgi
    print("local wsgi is imported")
except Exception as e:
    print("local wsgi is not imported")
    print("WSGI error is: <%s>" % str(e))

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OnToology.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()