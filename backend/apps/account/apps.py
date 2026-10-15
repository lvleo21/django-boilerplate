from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.account'
    verbose_name = _("Usuário")

    def ready(self):
        import apps.account.signals.account  # noqa: F401
        return super().ready()
