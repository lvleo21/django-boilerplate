from django.utils.translation import gettext as _

from rest_framework import serializers, exceptions

from apps.upload.utils import create_file_upload


class UploadSerializer(serializers.Serializer):
    name = serializers.CharField(write_only=True, allow_blank=True)
    url = serializers.CharField(read_only=True)
    pk = serializers.IntegerField(read_only=True)
    path = serializers.CharField(read_only=True)

    def create(self, validated_data):
        try:
            upload, response = create_file_upload(
                name=validated_data.get("name"),
            )
        except Exception:
            raise exceptions.ValidationError()

        return {
            "url": response,
            "pk": upload.pk,
            "path": upload.path.url
        }
