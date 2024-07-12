"""
WSGI config for django_smartcar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/opt/bitnami/projects/smartcar')
os.environ['PYTHON_EGG_CACHE'] = '/opt/bitnami/projects/smartcar/egg_cache'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_smartcar.settings')

application = get_wsgi_application()
