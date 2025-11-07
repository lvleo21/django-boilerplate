import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.core.storages import UUIDS3Storage


class FileUpload(BaseModel):
    path = models.FileField(
        _('Path'),
        blank=True,
        null=True,
        editable=False,
        storage=UUIDS3Storage(),
        max_length=255,
    )
    name = models.CharField(
        _('Nome'),
        max_length=255,
        editable=False
    )
    owner = models.ForeignKey(
        "account.Account",
        verbose_name=_("Usuário responsável"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        editable=False
    )

    @property
    def extension(self):
        _, extension = os.path.splitext(self.path.name)
        return extension

    class Meta:
        verbose_name = _('Upload de arquivo')
        verbose_name_plural = _('Upload de arquivos')

    def __str__(self):
        return self.name
