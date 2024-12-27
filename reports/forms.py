from django import forms
from reports.models import Report, ReportItem
from django.utils.translation import gettext_lazy as _
from stores.models import Store


class SelectStoreForm(forms.Form):
    store_instance = forms.ModelChoiceField(queryset=Store.objects.all(), label=_('Store'), required=True)

    def clean(self):
        if not self.user.is_superuser and self.user != self.cleaned_data.get('store_instance').worker:
            raise forms.ValidationError('You cannot create a report for this store')


class ReportForm(forms.ModelForm):
    is_rainy = forms.BooleanField(label=_('Is rainy'), required=False)

    def save(self, commit=True):
        store = self.instance.store
        self.instance.cones = store.cones - self.instance.cones
        self.instance.cups = store.cups - self.instance.cups

        store.cones -= self.instance.cones
        store.cups -= self.instance.cups
        store.save()

        return super().save(commit=commit)

    class Meta:
        model = Report
        fields = ['store', 'cones', 'cups', 'is_rainy', 'notes']
        widgets = {'store': forms.HiddenInput(), }


class ReportItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ice_cream'].disabled = True

    def clean(self):
        self.cleaned_data['report'] = self.cleaned_data['id'].report
        if self.cleaned_data['quantity'] > self.cleaned_data['id'].ice_cream.quantity:
            raise forms.ValidationError('You cannot sell more ice cream than you have in stock')

    def save(self, commit=True):
        self.instance.quantity = self.instance.ice_cream.quantity - self.instance.quantity
        self.instance.report.save()
        self.instance.ice_cream.quantity -= self.instance.quantity
        self.instance.ice_cream.save()
        return super().save(commit=commit)

    class Meta:
        model = ReportItem
        fields = ['ice_cream', 'quantity', 'need_refill']


ReportItemInlineFormSet = forms.inlineformset_factory(Report, ReportItem, form=ReportItemForm, extra=0,
                                                      can_delete=False)
