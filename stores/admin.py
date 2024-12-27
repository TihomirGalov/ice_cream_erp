from django.contrib import admin

from .models import Store, IceCream
from .forms import IceCreamForm


class IceCreamAdmin(admin.TabularInline):
    form = IceCreamForm
    model = IceCream
    extra = 1


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'worker')
    inlines = [IceCreamAdmin]
