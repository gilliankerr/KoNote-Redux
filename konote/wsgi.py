"""WSGI config for KoNote Web."""
import os
from django.core.wsgi import get_wsgi_application


def get_default_settings():
    """Auto-detect environment and return appropriate settings module."""
    # If explicitly set, respect that
    if "DJANGO_SETTINGS_MODULE" in os.environ:
        return os.environ["DJANGO_SETTINGS_MODULE"]

    # Auto-detect Railway (has RAILWAY_ENVIRONMENT variable)
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        return "konote.settings.production"

    # Auto-detect Docker/production (has DATABASE_URL but not local dev)
    if os.environ.get("DATABASE_URL") and not os.environ.get("KONOTE_LOCAL_DEV"):
        return "konote.settings.production"

    # Default to production for WSGI (gunicorn)
    return "konote.settings.production"


os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_default_settings())
application = get_wsgi_application()
