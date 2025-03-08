from django.conf import settings
from django.utils.translation import gettext_lazy as _


def environment_callback(request):
    color = "danger" if settings.DEBUG else "success"
    return [
        _("{} - v{}").format(settings.ENVIRONMENT, settings.VERSION), color
    ]
