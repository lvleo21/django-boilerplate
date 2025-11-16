from storages.backends.s3boto3 import (
    S3Boto3Storage,
    S3StaticStorage
)


class StaticRootS3BotoStorage(S3StaticStorage):
    location = "static"
    file_overwrite = True
    default_acl = "public-read"


class MediaRootS3BotoStorage(S3Boto3Storage):
    location = "media"
