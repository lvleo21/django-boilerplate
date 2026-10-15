import hashlib
import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# Raiz do repositório: guarda o frontend/ e o build do Vite.
ROOT_DIR = BASE_DIR.parent.parent

env = environ.Env()

environ.Env.read_env(os.path.join(BASE_DIR, "settings/.env"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG", default=True, cast=bool)

VERSION = env("VERSION", default="0.1.0")

PROJECT_NAME = env("PROJECT_NAME", default="PROJECT NAME")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS", default=["https://0.0.0.0:8000"]
)

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

EXTERNAL_APPS = [
    "rest_framework",
    "rosetta",
    "drf_yasg",
    "django_celery_beat",
    "django_vite",
    "inertia",
]

PROJECT_APPS = [
    "apps.account",
    "apps.core",
    "apps.upload",
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "inertia.middleware.InertiaMiddleware",
    "apps.core.middlewares.inertia.inertia_share",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.NumericPasswordValidator"),
    },
]

# Locale

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

LANGUAGES = [
    ("pt-br", "PT-BR"),
    ("en", "EN"),
]

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Recife"

USE_I18N = True

USE_TZ = True

# Static

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Saída do build do Vite (vite.config.ts: build.outDir).
STATICFILES_DIRS = [ROOT_DIR / "frontend" / "dist"]

# frontend/dist/ só existe depois do `yarn build`.
SILENCED_SYSTEM_CHECKS = ["staticfiles.W004"]

# Vite
# https://github.com/MrBin99/django-vite

VITE_MANIFEST_PATH = ROOT_DIR / "frontend" / "dist" / "manifest.json"

DJANGO_VITE = {
    "default": {
        # Com DEBUG, os assets vêm do servidor do Vite (`yarn dev`); sem,
        # do manifest gerado pelo `yarn build`.
        "dev_mode": DEBUG,
        "manifest_path": VITE_MANIFEST_PATH,
    }
}

# Inertia
# https://inertiajs.github.io/inertia-django/

INERTIA_LAYOUT = "core/layouts/base.html"

# A versão dos assets muda a cada build para que clientes com assets antigos
# recebam um reload completo da página. Constante sem build (modo dev do Vite).
try:
    INERTIA_VERSION = hashlib.md5(
        VITE_MANIFEST_PATH.read_bytes(), usedforsecurity=False
    ).hexdigest()
except FileNotFoundError:
    INERTIA_VERSION = "dev"

# Media

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Account

AUTH_USER_MODEL = "account.Account"

# Swagger

USE_SWAGGER = env("USE_SWAGGER", default=False, cast=bool)

if USE_SWAGGER:
    SWAGGER_SETTINGS = {"SECURITY_DEFINITIONS": {"Basic": {"type": "basic"}}}

    SWAGGER_OPENAPI_TERM_OF_SERVICE = env(
        "SWAGGER_OPENAPI_TERM_OF_SERVICE", default="Insert term"
    )

    SWAGGER_OPENAPI_CONTACT = env("SWAGGER_OPENAPI_CONTACT", default="Insert contact")

    SWAGGER_OPENAPI_LICENSE = env("SWAGGER_OPENAPI_LICENSE", default="Insert license")

# SMTP

USE_SMTP = env("USE_SMTP", default=False, cast=bool)

if USE_SMTP:
    EMAIL_FILE_PATH = BASE_DIR / "sent_emails"
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

# Database
# Formato: DATABASE_URL=postgres://user:password@host:port/name
# Sem a variável definida, usa SQLite no arquivo db.sqlite3 na raiz do projeto.

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    )
}

# Celery

USE_CELERY = env("USE_CELERY", default=False, cast=bool)
if USE_CELERY:
    CELERY_BROKER_URL = env("CELERY_BROKER")
    CELERY_RESULT_BACKEND = env("CELERY_BACKEND")
