from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title=settings.PROJECT_NAME,
        default_version=f"v{getattr(settings, 'VERSION', '0.1.0')}",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email=settings.SWAGGER_OPENAPI_CONTACT),
        license=openapi.License(name=settings.SWAGGER_OPENAPI_LICENSE),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
