from django.db import models
from django.utils.translation import gettext_lazy as _
from stores.models import Store, IceCream


class Report(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='reports', verbose_name=_('Store'))
    date = models.DateField(auto_now_add=True, verbose_name=_('Date'))
    is_rainy = models.BooleanField(default=False, verbose_name=_('Rainy'))
    cones = models.IntegerField(default=0, verbose_name=_('Cones'))
    cups = models.IntegerField(default=0, verbose_name=_('Cups'))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Price'))

    notes = models.TextField(null=True, blank=True, verbose_name=_('Notes'))

    def __str__(self):
        return f'{self.store.name} - {self.date}'

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')


class ReportItem(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='items', verbose_name=_('Report'))
    ice_cream = models.ForeignKey(IceCream, on_delete=models.CASCADE, related_name='report_items', verbose_name=_('Ice cream'))
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Quantity'))
    need_refill = models.BooleanField(default=False, verbose_name=_('Need refill'))

    @property
    def name(self):
        return self.ice_cream.type.name

    def __str__(self):
        return f'{self.name} - {self.quantity}'

    class Meta:
        verbose_name = _('Report item')
        verbose_name_plural = _('Report items')
