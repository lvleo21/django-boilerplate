from django.urls import include, path

urlpatterns = [
    path("", include("apps.core.urls")),
    path("upload/", include("apps.upload.urls")),
]
