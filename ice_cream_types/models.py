from django.db import models
from django.utils.translation import gettext_lazy as _


class IceCreamType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Ice cream type")
        verbose_name_plural = _("Ice cream types")
