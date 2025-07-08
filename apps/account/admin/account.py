from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from apps.account.models import Account
from apps.core.admin import BaseAdmin

from apps.account.admin.profile import ProfileInline


@admin.register(Account)
class AccountAdmin(UserAdmin, BaseAdmin):
    list_display = [
        "email",
        "username",
        "is_staff",
        "created_at",
        "is_active"
    ]
    list_filter = ["email", "is_staff", "is_superuser", "is_active"]
    fieldsets = [
        (None, {"fields": ("email", "username", "password")}),
        (
            _("Permissões"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
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
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        )
    ]
    search_fields = ["email"]
    ordering = ["username"]
    inlines = [ProfileInline]


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(GroupAdmin, admin.ModelAdmin):
    ...
