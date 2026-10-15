import django
from django.conf import settings
from django.urls import reverse
from inertia import inertia


@inertia("Welcome")
def welcome(request):
    return {
        "project_name": settings.PROJECT_NAME,
        "django_version": django.get_version(),
        "admin_url": reverse("admin:index"),
    }
