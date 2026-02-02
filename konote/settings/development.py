"""Development settings — local use only."""
from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Relax security for local dev
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
