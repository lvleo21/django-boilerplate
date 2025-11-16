from django.urls import path, include


urlpatterns = [
    path('upload/', include('apps.upload.urls')),
]
