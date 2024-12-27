from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from ice_cream_types.models import IceCreamType


class Store(models.Model):
    name = models.CharField(max_length=100, unique=True, default='ice_cream_erp\'s Ice Cream', verbose_name=_('Name'))
    cones = models.IntegerField(verbose_name=_('Cones'))
    cups = models.IntegerField(verbose_name=_('Cups'))
    worker = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='store', verbose_name=_('Worker'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')


class IceCream(models.Model):
    type = models.ForeignKey(IceCreamType, on_delete=models.CASCADE, related_name='ice_creams', verbose_name=_('Type'))
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='ice_creams', verbose_name=_('Store'))
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name=_('Quantity'))

    def __str__(self):
        return f'{self.type.name} - {self.quantity}'

    class Meta:
        verbose_name = _('Ice Cream')
        verbose_name_plural = _('Ice Creams')
