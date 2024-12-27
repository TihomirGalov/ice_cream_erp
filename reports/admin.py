import csv

from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import path
from django.http import HttpResponse

from rangefilter.filter import DateRangeFilter
from import_export.admin import ExportMixin

from .models import ReportItem, Report
from .resources import ReportResource


class ReportItemInline(admin.TabularInline):
    model = ReportItem
    extra = 0
    min_num = 1  # can add items to the report


@admin.register(Report)
class ReportAdmin(ExportMixin, admin.ModelAdmin):
    inlines = (ReportItemInline,)
    resource_class = ReportResource
    list_display = ('date', 'store', 'worker', 'cones', 'cups', 'price', 'need_refill', 'is_rainy', 'report_actions')
    list_filter = (('date', DateRangeFilter), 'store__name', 'is_rainy')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__worker=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user
        return form

    def export_single_report(self, *args, **kwargs):
        obj = Report.objects.get(id=kwargs['report_id'])
        response = HttpResponse(content_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="report_{obj.date}_{obj.store}.csv"'}, )

        writer = csv.writer(response)
        writer.writerow(['Магазин', 'Дата', 'Дъждовно', 'Фунийки', 'Купички', 'Общо'])
        writer.writerow([obj.store.name, obj.date, 'Да' if obj.is_rainy else 'Не', obj.cones, obj.cups, obj.price])
        writer.writerow(['Сладолед', 'Количество'])

        for item in obj.items.all():
            writer.writerow([item.ice_cream.type.name, item.quantity])

        return response

    def need_refill(self, obj):
        for item in obj.items.all():
            if item.need_refill:
                return True

        if obj.notes is None:
            return False
        return len(obj.notes) != 0

    def worker(self, obj):
        return obj.store.worker

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<int:report_id>/export/", self.admin_site.admin_view(self.export_single_report), name="export", )]
        return custom_urls + urls

    def report_actions(self, obj):
        return format_html('<a class="button" href="{}">' + _("Export") + "</a>",
            reverse("admin:export", args=[obj.pk]), )

    need_refill.boolean = True
    need_refill.short_description = _('Need refill')
    report_actions.short_description = _('Actions')

    class Media:
        css = {'all': ('css/admin.css',)}
