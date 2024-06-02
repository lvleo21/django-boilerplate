from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin

from apps.core.models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ["email", "username", "is_staff", "email_is_confirmed", "created_at"]
    list_filter = ["email", "is_staff"]

    fieldsets = [
        (
            None,
            {"fields": ("email", "username", "password", "first_name", "last_name")},
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
                    "password1",
                    "password2",
                ),
            },
        )
    ]

    list_editable = ["email_is_confirmed"]
    search_fields = ["email"]
    ordering = ["email"]


# Custom admin name

title = settings.PROJECT_NAME
full_title = "{} (v{})".format(
    title,
    getattr(settings, "VERSION", "0.1.0"),
)
admin.site.site_title = "Django Admin"
admin.site.site_header = full_title
admin.site.index_title = title
