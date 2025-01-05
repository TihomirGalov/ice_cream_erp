from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class IceCreamTypeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ice_cream_types'
    verbose_name = _("Ice Cream Types")
