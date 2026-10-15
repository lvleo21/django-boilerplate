from pathlib import Path

import environ

# Todo ponto de entrada (manage.py, wsgi, asgi, celery, pytest) importa `config`
# antes de carregar as settings, então o .env é lido uma vez só, aqui. Lido
# antes de escolher as settings, para que o DJANGO_SETTINGS_MODULE possa vir
# dele; variáveis já definidas no ambiente têm prioridade.
environ.Env.read_env(Path(__file__).resolve().parent / "settings/.env")

from .celery import app as celery_app  # noqa: E402

__all__ = ["celery_app"]
