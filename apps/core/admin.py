from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from apps.core.models import Account
from apps.core.sites import custom_admin_site

admin.site.unregister(Group)


class BaseAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_filter = ['is_active']


@admin.register(Account, site=custom_admin_site)
class AccountAdmin(UserAdmin, BaseAdmin):
    list_display = [
        "email", "username", "is_staff", "email_is_confirmed", "created_at",
        "is_active"
    ]
    list_filter = ["email", "is_staff", "is_active"]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "email",
                    "username",
                    "password",
                ]
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "email_is_confirmed",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        )
    ]

    list_editable = ["email_is_confirmed", "is_active"]
    search_fields = ["email"]
    ordering = ["username"]


@admin.register(Group, site=custom_admin_site)
class GroupAdmin(GroupAdmin, admin.ModelAdmin):
    ...
