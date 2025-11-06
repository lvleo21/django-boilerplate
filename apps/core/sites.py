from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class CustomAdminSite(admin.AdminSite):
    site_title = settings.PROJECT_NAME
    index_title = _("Painel de Administração: {}").format(
        settings.PROJECT_NAME
    )

    def each_context(self, request):
        context = super(CustomAdminSite, self).each_context(request)
        context.update({
            "site_header": self.get_site_header(),
        })
        return context

    def get_site_header(self):
        return (
            f"{self.site_title} - {settings.ENVIRONMENT.upper()} "
            f"(v{settings.VERSION})"
        )


admin_site = CustomAdminSite()
# Copia todos os registries do admin padrão
admin_site._registry.update(admin.site._registry)
