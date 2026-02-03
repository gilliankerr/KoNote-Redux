#!/usr/bin/env python
"""Django management command entry point."""
import os
import sys


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

    # Default to development for local work
    return "konote.settings.development"


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_default_settings())
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and "
            "available on your PYTHONPATH environment variable."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
