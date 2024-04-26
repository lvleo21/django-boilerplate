from .base import *


MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

#* Django Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

#* Swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        }
    }
}

SWAGGER_OPENAPI_TITLE = env("SWAGGER_OPENAPI_TITLE", default="Insert title")

SWAGGER_OPENAPI_VERSION = env("SWAGGER_OPENAPI_VERSION", default="Insert version")

SWAGGER_OPENAPI_TERM_OF_SERVICE = env("SWAGGER_OPENAPI_TERM_OF_SERVICE", default="Insert term")

SWAGGER_OPENAPI_CONTACT = env("SWAGGER_OPENAPI_CONTACT", default="Insert contact")

SWAGGER_OPENAPI_LICENSE = env("SWAGGER_OPENAPI_LICENSE", default="Insert license")

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
