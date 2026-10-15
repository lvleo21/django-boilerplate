from django.contrib import admin

from apps.core.admin import BaseAdmin
from apps.core.sites import admin_site
from apps.upload.models import FileUpload


@admin.register(FileUpload, site=admin_site)
class FileUploadAdmin(BaseAdmin):
    model = FileUpload
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = (
        'name',
        'path',
        'owner',
        'created_at',
        'updated_at'
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
