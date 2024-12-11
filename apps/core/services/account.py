from django.conf import settings
from django.db import transaction

from apps.core.models import Account


class AccountService:
    ACCOUNT_DEFAULT_EMAIL = settings.ACCOUNT_DEFAULT_EMAIL
    ACCOUNT_DEFAULT_PASSWORD = settings.ACCOUNT_DEFAULT_PASSWORD
    ACCOUNT_DEFAULT_USERNAME = settings.ACCOUNT_DEFAULT_USERNAME

    @classmethod
    def create_default_user(cls):
        with transaction.atomic():
            params = {
                "username": cls.ACCOUNT_DEFAULT_USERNAME,
                "email": cls.ACCOUNT_DEFAULT_EMAIL,
                "is_staff": True,
                "email_is_confirmed": True,
                "is_superuser": True,
            }
            try:
                Account.objects.select_for_update().get(**params)
            except Account.DoesNotExist:
                account = Account.objects.create(**params)
                account.set_password(cls.ACCOUNT_DEFAULT_PASSWORD)
                account.save()
