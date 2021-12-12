from django import forms
import datetime

coarse_CHOICES = (('1', '1'), ('10', '10'), ('20', '20'), ('100', '100'), ('1000', '1000'))
time_CHOICES = (('1', '1h'), ('24', '24h'), ('168', '1 Woche'), ('720', '1 Monat'), ('0', 'Gesamter Zeitraum'))

class coarse(forms.Form):
    Auflösung = forms.TypedChoiceField(choices=coarse_CHOICES, coerce=int)
    Zeitrahmen = forms.TypedChoiceField(choices=time_CHOICES, coerce=int)

class datepicker(forms.Form):
    Anfang = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget())
    Ende = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget())
    Auflösung = forms.TypedChoiceField(choices=coarse_CHOICES, coerce=int)
