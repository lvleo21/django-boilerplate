from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_filter = ['is_active']
