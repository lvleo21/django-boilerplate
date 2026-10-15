from celery import Celery

# Sem padrão para o DJANGO_SETTINGS_MODULE: este módulo roda em todo import de
# `config` (config/__init__.py), inclusive pelo manage.py, e um padrão aqui
# venceria o dele. O worker usa o do ambiente ou do .env.
app = Celery("config")
app.conf.enable_utc = False

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
