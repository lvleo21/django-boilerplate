import boto3

from django.conf import settings
from django.db import transaction

from apps.upload.models import FileUpload


def _create_presigned_url(object_name, expiration=3600):
    s3_client = boto3.client(
        's3',
        region_name=getattr(settings, 'AWS_REGION', ''),
        aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID', ''),
        aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', ''),
        endpoint_url=getattr(settings, 'AWS_S3_ENDPOINT_URL', ''),
    )

    return s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', ''),
            'Key': object_name
        },
        ExpiresIn=expiration
    )


@transaction.atomic
def create_file_upload(name):
    upload = FileUpload.objects.create(
        name=name
    )
    name_parts = name.split('.')
    name_ext = name_parts[-1] if len(name_parts) > 1 else None
    name_short = '.'.join(name_parts[:-1])[:10]
    if name_ext:
        name_short += '.' + name_ext[-5:]
    key = "uploads/{}/{}".format(
        upload.pk,
        name_short
    )
    response = _create_presigned_url(key)
    upload.path = key
    upload.save()
    return (upload, response)
