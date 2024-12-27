from django import forms
from django.utils.translation import gettext_lazy as _
from .models import IceCream, Store
from django.forms.models import inlineformset_factory


class IceCreamForm(forms.ModelForm):
    quantity = forms.IntegerField(label=_('Available'), required=False)
    increment = forms.IntegerField(label=_('Increment'), required=False)

    def clean(self):
        self.cleaned_data['increment'] = self.cleaned_data['increment'] or 0
        if not self.cleaned_data.get('quantity'):
            self.cleaned_data['quantity'] = 0
        self.cleaned_data['quantity'] += self.cleaned_data['increment']

        if self.cleaned_data['increment'] < 0:
            raise forms.ValidationError(_('Increment must be a positive number'))

    class Meta:
        model = IceCream
        fields = ['type', 'quantity', 'increment']
