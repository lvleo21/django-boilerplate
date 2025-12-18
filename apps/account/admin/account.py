from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from apps.account.admin.profile import ProfileInline
from apps.account.models import Account
from apps.core.admin import BaseAdmin
from apps.core.sites import admin_site


admin_site.unregister(Group)


@admin.register(Account, site=admin_site)
class AccountAdmin(UserAdmin, BaseAdmin):
    list_display = [
        "username",
        "email",
        "is_staff",
        "is_active",
        "created_at",
    ]
    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active"
    ]
    search_fields = ["email", "username"]
    ordering = ["username"]
    inlines = [ProfileInline]
    readonly_fields = [
        "last_login",
        "date_joined",
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "usable_password",
                    "is_staff",
                    "is_superuser",
                )
            }
        )
    ]


@admin.register(Group, site=admin_site)
class GroupAdmin(GroupAdmin, BaseAdmin):
    ...
