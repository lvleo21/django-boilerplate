from django.conf import settings


def environment_flag(request):
    return dict(
        environment_flag={
            "is_active": settings.ENVIRONMENT_FLAG,
            "version": settings.VERSION,
        }
    )
