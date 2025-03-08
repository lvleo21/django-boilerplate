from django.conf import settings

from unfold.sites import UnfoldAdminSite


class CustomAdminSite(UnfoldAdminSite):

    def each_context(self, request):
        context = super(CustomAdminSite, self).each_context(request)
        context.update({
            "environment": self._get_environment_callback(),
        })
        return context

    def _get_environment_callback(self):
        COLOR = "success"
        return [
            "{} - v{}".format(settings.ENVIRONMENT, settings.VERSION),
            COLOR
        ]


custom_admin_site = CustomAdminSite()
