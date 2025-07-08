from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.account.models import Profile


@receiver(post_save, sender="account.Account")
def create_account_profile(sender, instance, created, **kwargs):
    """
    Signal to create a profile when an account is created.
    """

    if not hasattr(instance, "profile"):
        Profile.objects.create(
            account=instance
        )
