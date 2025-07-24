from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm
)

from apps.account.admin.profile import ProfileInline
from apps.account.models import Account
from apps.core.admin import BaseAdmin
from apps.core.sites import custom_admin_site


admin.site.unregister(Group)


@admin.register(Account, site=custom_admin_site)
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
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    search_fields = ["email", "username"]
    ordering = ["username"]
    inlines = [ProfileInline]
    readonly_fields = [
        "last_login",
        "date_joined",
    ]


@admin.register(Group, site=custom_admin_site)
class GroupAdmin(GroupAdmin, admin.ModelAdmin):
    ...
