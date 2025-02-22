from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    help = "Command to generate django secret key"

    def handle(self, *args, **options):
        print(get_random_secret_key())
