from django.conf import settings
from django.templatetags.static import static

from unfold.sites import UnfoldAdminSite
from unfold.utils import hex_to_rgb


class CustomAdminSite(UnfoldAdminSite):
    site_title = settings.PROJECT_NAME
    site_header = settings.PROJECT_NAME
    site_symbol = "settings"  # Material Symbols & Icons
    show_history = True
    sidebar_show_search = True
    sidebar_show_all_applications = True
    colors = {
        "primary": {
            "50": "232 236 255",
            "100": "208 218 255",
            "200": "174 190 255",
            "300": "125 152 255",
            "400": "84 121 255",
            "500": "68 102 255",
            "600": "58 89 229",
            "700": "49 76 204",
            "800": "42 65 178",
            "900": "35 54 151",
            "950": "18 28 102"
        }
    }

    def each_context(self, request):
        context = super(CustomAdminSite, self).each_context(request)
        context.update({
            "site_symbol": getattr(self, "site_symbol", "settings"),
            "show_history": getattr(self, "show_history", False),
            "environment": self._get_environment_callback(),
            "sidebar_show_all_applications": getattr(
                self,
                "sidebar_show_all_applications",
                False
            ),
            "sidebar_show_search": getattr(
                self,
                "sidebar_show_search",
                False
            ),
            "colors": self._get_colors("colors", request),
        })
        return context

    def _get_environment_callback(self):
        color = "danger" if settings.DEBUG else "success"
        return [
            "{} - v{}".format(settings.ENVIRONMENT, settings.VERSION), color
        ]

    # def _get_colors(self, key: str, *args) -> dict[str, dict[str, str]]:
    #     colors = self.colors

    #     def rgb_to_values(value: str) -> str:
    #         return " ".join(
    #             list(
    #                 map(
    #                     str.strip,
    #                     value.removeprefix("rgb(").removesuffix(")").split(","),
    #                 )
    #             )
    #         )

    #     def hex_to_values(value: str) -> str:
    #         return " ".join(str(item) for item in hex_to_rgb(value))

    #     for name, weights in colors.items():
    #         weights = self._get_value(weights, *args)
    #         colors[name] = weights

    #         for weight, value in weights.items():
    #             if value[0] == "#":
    #                 colors[name][weight] = hex_to_values(value)
    #             elif value.startswith("rgb"):
    #                 colors[name][weight] = rgb_to_values(value)

    #     return colors


custom_admin_site = CustomAdminSite()
