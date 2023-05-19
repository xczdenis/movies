"""
This file contains all the settings that defines the development server.
SECURITY WARNING: don't run with debug turned on in production!
"""

import socket

from adminpanel.config.settings.components.base import INSTALLED_APPS, MIDDLEWARE

# Setting the development status:
DEBUG = True


def _custom_show_toolbar(request):
    """Only show the debug toolbar to users with the superuser flag."""
    return DEBUG and (request.META["REMOTE_ADDR"] in INTERNAL_IPS or request.user.is_superuser)


def _add_to_collection(value, collection: list):
    if value not in collection:
        collection.append(value)


# Installed apps for development only:
_add_to_collection("debug_toolbar", INSTALLED_APPS)

# Django debug toolbar:
# https://django-debug-toolbar.readthedocs.io
_add_to_collection("debug_toolbar.middleware.DebugToolbarMiddleware", MIDDLEWARE)

# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
current_host_name = socket.gethostname()
hostname, aliases, ips = socket.gethostbyname_ex(current_host_name)
INTERNAL_IPS = ["{0}.1".format(ip[: ip.rfind(".")]) for ip in ips]


DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": _custom_show_toolbar}

SECURE_CROSS_ORIGIN_OPENER_POLICY = None
