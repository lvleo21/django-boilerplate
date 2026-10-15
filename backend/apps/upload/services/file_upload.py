
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.db import transaction


from apps.upload.models import FileUpload
from apps.upload.services import Boto3Service


class FileUploadService:

    @classmethod
    @transaction.atomic
    def create_file_upload(cls, name):
        upload = FileUpload.objects.create(
            name=name
        )
        object_name = upload.get_object_name()
        response = Boto3Service.create_presigned_post(object_name)
        if not response:
            return (None, None)
        upload.path = object_name
        upload.save()
        return (upload, response)
