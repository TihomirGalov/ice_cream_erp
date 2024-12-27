from constance import config
from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from reports.models import Report, ReportItem
from reports.forms import SelectStoreForm, ReportForm, ReportItemInlineFormSet


def store_form_view(request):
    if request.method == 'POST':
        form = SelectStoreForm(request.POST)
        form.user = request.user
        if form.is_valid():
            store_instance = form.cleaned_data['store_instance']
            report = Report.objects.create(store=store_instance)
            for ice_cream in store_instance.ice_creams.all():
                ReportItem.objects.create(report=report, ice_cream=ice_cream, quantity=0)
            return redirect(f'/reports/create_report/{report.id}/')
    else:
        form = SelectStoreForm()

    context = {'form': form, }
    return render(request, 'admin/action_form/run_action.html', context)


def create_report_view(request, pk):
    report_instance = get_object_or_404(Report, pk=pk)

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report_instance)
        formset = ReportItemInlineFormSet(request.POST, instance=report_instance)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            for item in report_instance.items.all():
                report_instance.price += item.quantity * Decimal(config.ICE_CREAM_PRICE / 100)
            report_instance.save()
            return HttpResponseRedirect(reverse("admin:reports_report_change", args=(pk,)))
    else:

        form = ReportForm(instance=report_instance)

        formset = ReportItemInlineFormSet(instance=report_instance)

    context = {'form': form, 'formset': formset, 'report_instance': report_instance, }
    return render(request, 'admin/action_form/run_action.html', context)
