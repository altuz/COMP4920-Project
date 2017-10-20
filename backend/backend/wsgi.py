"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
#from backend.views import graph_setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

#graph_setup()

application = get_wsgi_application()
