import re

from django.core import validators
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.managers import AccountManager
from apps.core.models import BaseModel


class Account(BaseModel, AbstractUser):
    username = models.CharField(
        _("Nome de usuário"),
        max_length=15,
        unique=True,
        help_text=_(
            "Obrigatório. Máximo de 15 caracteres. Letras, números e "
            "caracteres @/./+/-/_ permitidos."
        ),
        validators=[
            validators.RegexValidator(
                re.compile(r"^[\w.@+-]+$"),
                _("Insira um nome de usuário válido."),
                "invalid",
            )
        ],
    )
    email = models.EmailField(
        _("E-mail"),
        max_length=255,
        unique=True
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = AccountManager()

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")
