from django.contrib import admin

from .models import IceCreamType


@admin.register(IceCreamType)
class IceCreamTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
