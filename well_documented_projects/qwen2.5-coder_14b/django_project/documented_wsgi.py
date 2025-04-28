```python
"""
WSGI config for django_project project.

This module configures the WSGI application for the Django project named 'django_project'.
It exposes the WSGI callable as a module-level variable named 'application'.

For more information on this file, see:
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the Django project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# Get the WSGI application instance for the Django project.
application = get_wsgi_application()
```