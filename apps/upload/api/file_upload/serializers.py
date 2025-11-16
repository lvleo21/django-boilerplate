from rest_framework import serializers, exceptions

from apps.upload.services import FileUploadService


class UploadSerializer(serializers.Serializer):
    name = serializers.CharField(write_only=True, allow_blank=True)
    url = serializers.CharField(read_only=True)
    pk = serializers.IntegerField(read_only=True)
    path = serializers.CharField(read_only=True)

    def create(self, validated_data):
        try:
            upload, presigned_url = (
                FileUploadService.create_file_upload(
                    name=validated_data.get("name"),
                )
            )
        except Exception:
            raise exceptions.ValidationError()

        return {
            "url": presigned_url,
            "pk": upload.pk,
            "path": upload.path.url
        }
