"""ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from pathlib import Path

import environ
from django.core.asgi import get_asgi_application

# Lido antes de escolher as settings, para que o DJANGO_SETTINGS_MODULE
# possa vir do .env. Sem a variável, servidores sobem com as de produção.
environ.Env.read_env(Path(__file__).resolve().parent / "settings/.env")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

application = get_asgi_application()
