from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve

from apps.core.sites import custom_admin_site

from .settings.swagger import schema_view


urlpatterns = [
    # Unfold Admin
    path("staff/", custom_admin_site.urls),

    # Rosetta
    re_path("rosetta/", include('rosetta.urls')),

    # Swagger
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc"
    ),

    # Media
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT}
    ),

    # Static
    re_path(
        r'^static/(?P<path>.*)$',
        serve,
        {'document_root': settings.STATIC_ROOT}
    ),
]

if settings.DEBUG:
    # Debug Toolbar
    urlpatterns.extend([
        path("__debug__/", include("debug_toolbar.urls")),
    ])
