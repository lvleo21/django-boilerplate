from django.db.models import signals
from django.dispatch import receiver

from apps.core.services.account import AccountService
from apps.core.apps import CoreConfig


@receiver(signals.post_migrate)
def craete_default_account(sender, **kwargs):
    if sender.name == CoreConfig.name:
        AccountService.create_default_user()
