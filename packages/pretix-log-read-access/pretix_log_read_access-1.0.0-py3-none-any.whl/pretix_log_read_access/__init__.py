from django.conf import settings
from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = "1.0.0"


class PluginApp(PluginConfig):
    name = "pretix_log_read_access"
    verbose_name = "Log read-only order data access"

    class PretixPluginMeta:
        name = gettext_lazy("Log read-only order data access")
        author = "pretix team"
        description = gettext_lazy("This plugin logs any access to extended information (e.g. question answers) of a specific order, as well as all export jobs. No warranty for completeness given.")
        visible = False
        version = __version__
        category = "FEATURE"
        compatibility = "pretix>=3.10.0"

    def ready(self):
        from . import signals  # NOQA
        settings.MIDDLEWARE.append('pretix_log_read_access.middleware.LogMiddleware')
        settings.CORE_MODULES.add('pretix_log_read_access')


default_app_config = "pretix_log_read_access.PluginApp"
