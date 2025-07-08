from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Profile(BaseModel):
    account = models.OneToOneField(
        "account.Account",
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("Usuário"),
    )
    name = models.CharField(
        verbose_name=_("Nome"),
        max_length=255,
        help_text=_("Nome completo do usuário."),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Perfil")
        verbose_name_plural = _("Perfis")
