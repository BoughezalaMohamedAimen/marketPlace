from django import forms
from .models import *
import datetime

class WilayaForm(forms.ModelForm):
    class Meta:
        model=Wilaya
        fields='__all__'


class WilayaFormUpdate(forms.ModelForm):
    class Meta:
        model=Wilaya
        fields='__all__'
