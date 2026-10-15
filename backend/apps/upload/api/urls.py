from django.urls import include, path

urlpatterns = [
    path("upload/", include("apps.upload.api.file_upload.urls")),
]
