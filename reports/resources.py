from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.fields import Field
from reports.models import Report


class ReportResource(resources.ModelResource):
    store = Field(column_name=_("Store"))
    date = Field(column_name=_("Date"))
    report_items_col = Field(column_name=f"{_('Report items')} ({_('Ice cream')}, {_('Quantity')})")
    price = Field(column_name=_("Total"))
    is_rainy = Field(column_name=_("Is Rainy"))
    cones = Field(column_name=_("Cones"), attribute='cones')
    cups = Field(column_name=_("Cups"), attribute='cups')

    def dehydrate_title(self, obj):
        return str(obj.store.name)

    def dehydrate_report_items_col(self, obj):
        report_items_str = ""
        for item in obj.items.all():
            report_items_str += f"\n{item.ice_cream.type.name} {item.quantity}"
        return report_items_str

    def dehydrate_date(self, obj):
        return obj.date.strftime('%d/%m/%Y')

    def dehydrate_price(self, obj):
        return obj.price

    def dehydrate_is_rainy(self, obj):
        return _("Yes") if obj.is_rainy else _("No")

    class Meta:
        model = Report
