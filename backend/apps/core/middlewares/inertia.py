from django.utils.translation import get_language
from inertia import share


def inertia_share(get_response):
    """Compartilha com toda página Inertia as props usadas pelo frontend.

    Deve vir depois de `InertiaMiddleware` em `MIDDLEWARE`. Os tipos ficam em
    `frontend/types/inertia.d.ts`; manter os dois em sincronia.
    """

    def middleware(request):
        share(
            request,
            # O cliente Inertia espera `errors` em toda página; views com erros
            # de validação o sobrescrevem com a própria prop.
            errors={},
            language=get_language(),
        )
        return get_response(request)

    return middleware
