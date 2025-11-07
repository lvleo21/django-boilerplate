from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.upload.api.file_upload.serializers import UploadSerializer


class UploadView(generics.CreateAPIView):
    serializer_class = UploadSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self, **kwargs):
        context = super().get_serializer_context(**kwargs)
        context['entity'] = self.request.user.entity
        context['user'] = self.request.user
        return context
