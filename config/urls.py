# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from wrc_reporting_tool.report.views import index, dashboard_list, add_voluntar_to_sesizare, completeaza_raport, export


urlpatterns = [
    path("", index, name="home"),
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path("sesizari/", include("report.urls", namespace="sesizari")),
    path("dashboard/", dashboard_list, name="dash_list"),
    path("dashboard/export", export, name="export"),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    
    # User management
    path("users/", include("wrc_reporting_tool.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    
    # Your stuff: custom urls includes go here
    path("dashboard/<int:pk>/", add_voluntar_to_sesizare, name="preia"),
    path("dashboard/completeaza-raport/<int:pk>/", completeaza_raport, name="completeaza_raport"),
    
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
