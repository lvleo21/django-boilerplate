import boto3

from django.conf import settings

class FileUploadService:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            region_name=getattr(settings, 'AWS_REGION'),
            aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY'),
            endpoint_url=getattr(settings, 'AWS_S3_ENDPOINT_URL'),
        )

    def create_presigned_url(self, object_name):
        ...