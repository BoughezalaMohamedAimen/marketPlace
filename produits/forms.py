from django import forms
from django.forms import modelformset_factory
from .models import *
import datetime


class ProductForm(forms.ModelForm):
    class Meta:
        model=Produit
        fields='__all__'


class ProduitFormUpdate(forms.ModelForm):
    class Meta:
        model=Produit
        exclude=['user']

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model=ProductAttribute
        fields='__all__'

ProductAttributeFormset=modelformset_factory(ProductAttribute,fields='__all__')
