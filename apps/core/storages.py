import os
import uuid

from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3BotoStorage(S3Boto3Storage):
    location = "static"


class MediaRootS3BotoStorage(S3Boto3Storage):
    location = "media"


class UUIDS3Storage(S3Boto3Storage):

    def get_valid_name(self, name):
        filename, extension = os.path.splitext(name)
        return f"{uuid.uuid4()}{extension.lower()}"
