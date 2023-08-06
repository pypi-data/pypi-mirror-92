# -*- coding: utf-8 -*-


import os
import sys


# tweak PYTHONPATH if needed (usually if project is deployed outside site-packages)
# sys.path.append("/var/www/django")

os.environ['DJANGO_SETTINGS_MODULE'] = '{{ project_name }}.settings'
import django.core.handlers.wsgi


application = django.core.handlers.wsgi.WSGIHandler()
