from django.contrib import admin
from .models import *


class CategorieAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'slug','parent')
    list_filter=('parent',)


# Register your models here.
admin.site.register(Categorie,CategorieAdmin)
