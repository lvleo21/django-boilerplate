from config.settings.base import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}


# Storage

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL")

AWS_S3_SIGNATURE_VERSION = env("AWS_S3_SIGNATURE_VERSION")

AWS_REGION = env("AWS_REGION")

AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")

AWS_S3_USE_SSL = env.bool("AWS_S3_USE_SSL", default=True)

AWS_S3_MAX_AGE = env.int("AWS_S3_MAX_AGE", default=86400)

OPTIONS = {
    "access_key": AWS_ACCESS_KEY_ID,
    "secret_key": AWS_SECRET_ACCESS_KEY,
    "bucket_name": AWS_STORAGE_BUCKET_NAME,
    "endpoint_url": AWS_S3_ENDPOINT_URL,
    "signature_version": AWS_S3_SIGNATURE_VERSION,
    "use_ssl": AWS_S3_USE_SSL,
}

STORAGES = {
    "default": {
        "BACKEND": "apps.core.storages.MediaRootS3BotoStorage",
        "OPTIONS": {
            **OPTIONS,
            "object_parameters": {
                "CacheControl": f"max-age={AWS_S3_MAX_AGE}",
            }
        },
    },
    "staticfiles": {
        "BACKEND": "apps.core.storages.StaticRootS3BotoStorage",
        "OPTIONS": {
            **OPTIONS
        }
    }
}

# Static

STATIC_URL = f"http://{AWS_S3_ENDPOINT_URL}/static/"

# Media

MEDIA_URL = f"http://{AWS_S3_ENDPOINT_URL}/media/"
