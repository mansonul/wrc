import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "wrc_reporting_tool.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import wrc_reporting_tool.users.signals  # noqa: F401
