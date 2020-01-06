from django.contrib import admin
from django.urls import path,include,re_path
from .views import *


urlpatterns = [
        path('', HomeCommande.as_view(),name='HomeCommande'),
        
]
