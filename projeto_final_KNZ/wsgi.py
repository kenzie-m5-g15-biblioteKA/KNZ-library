"""
WSGI config for projeto_final_KNZ project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from lendings.scheduler import run_scheduler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projeto_final_KNZ.settings")

application = get_wsgi_application()

run_scheduler()
