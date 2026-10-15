import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(
        verbose_name=_("Criado em"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Atualizado em"),
        auto_now=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Está ativo?"),
        default=True
    )

    class Meta:
        abstract = True
