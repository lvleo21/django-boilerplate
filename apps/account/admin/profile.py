from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.account.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = _("Perfil")
    fk_name = "account"
    extra = 0
    can_delete = False
