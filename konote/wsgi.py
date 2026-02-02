"""WSGI config for KoNote Web."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "konote.settings.production")
application = get_wsgi_application()
