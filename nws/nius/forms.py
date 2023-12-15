from django import forms
from .constants import zrodla



class NewsFilterForm(forms.Form):
    tytul = forms.CharField(required=False)
    data_od = forms.DateField(required=False)
    data_do = forms.DateField(required=False)
    source = forms.MultipleChoiceField(choices=zrodla.items(), required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

