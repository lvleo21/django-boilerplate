
import boto3
from botocore.exceptions import ClientError

from django.conf import settings


class Boto3Service:
    client = boto3.client(
        "s3",
        region_name=getattr(settings, 'AWS_REGION'),
        aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY'),
        endpoint_url=getattr(settings, 'AWS_S3_ENDPOINT_URL'),
    )
    prefix = "media/"

    @classmethod
    def create_presigned_post(
        cls,
        object_name,
        fields=None,
        conditions=None,
        expiration=3600
    ):
        try:
            return cls.client.generate_presigned_post(
                getattr(settings, 'AWS_STORAGE_BUCKET_NAME'),
                f"{cls.prefix}{object_name}",
                Fields=fields,
                Conditions=conditions,
                ExpiresIn=expiration,
            )
        except ClientError:
            return None
