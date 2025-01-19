from django.conf import settings
from django.contrib import admin


class CustomAdminSite(admin.AdminSite):
    site_title = settings.PROJECT_NAME
    version = f"(v{settings.VERSION} - {settings.ENVIRONMENT.upper()})"
    site_header = f"{settings.PROJECT_NAME} {version}"


custom_admin_site = CustomAdminSite()
