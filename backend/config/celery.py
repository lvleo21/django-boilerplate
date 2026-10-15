import os
from pathlib import Path

import environ
from celery import Celery

# Como em wsgi.py: o .env pode escolher o módulo de settings, então é lido antes.
environ.Env.read_env(Path(__file__).resolve().parent / "settings/.env")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

app = Celery("config")
app.conf.enable_utc = False

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
