"""
Staging settings.
"""
from .production import *

# Staging is like production but with debug enabled for troubleshooting
DEBUG = True

# Less strict security for staging
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False