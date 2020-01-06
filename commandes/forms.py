from django import forms
from django.forms import ModelForm
from .models import *
import operator
# from django_countries.fields import CountryField
from django_countries.data import COUNTRIES











class CommandeForm(ModelForm):
    info=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':'4'}),required=False)
    class Meta:
        model=Commande
        exclude=['etat','remise','created_at','updated_at','livraison']
