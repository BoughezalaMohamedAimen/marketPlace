from django import forms
from .models import *


class CategorieForm(forms.ModelForm):

    class Meta:
        model=Categorie
        fields='__all__'


class CategorieFormUpdate(forms.ModelForm):

    class Meta:
        model=Categorie
        fields='__all__'
