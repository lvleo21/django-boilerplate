import uuid
import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class FileUpload(BaseModel):
    path = models.FileField(
        _('Path'),
        blank=True,
        null=True,
        editable=False,
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

    class Meta:
        verbose_name = _('Upload de arquivo')
        verbose_name_plural = _('Upload de arquivos')

    def __str__(self):
        return self.name

    @property
    def extension(self):
        if self.path:
            _, extension = os.path.splitext(self.path.name)
        else:
            splited_name = self.name.split(".")
            extension = (
                f".{splited_name[-1]}"
                if len(splited_name) > 1
                else None
            )
        return extension

    def get_object_name(self):
        uuid_part = str(uuid.uuid4())
        return (
            f"upload/{self.pk}/{uuid_part}{self.extension}"
        )
