from django.utils.translation import gettext_lazy as _

from unfold.admin import StackedInline

from apps.account.models import Profile


class ProfileInline(StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = _("Perfil")
    fk_name = "account"
    extra = 0
    can_delete = False
