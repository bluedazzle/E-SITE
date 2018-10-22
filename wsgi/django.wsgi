import os
import sys
import django.core.handlers.wsgi
from django.core.wsgi import get_wsgi_application

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'esite.settings'

sys.stdout = sys.stderr

DEBUG = True

application = get_wsgi_application()
