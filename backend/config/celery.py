from celery import Celery

app = Celery("config")
app.conf.enable_utc = False

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
