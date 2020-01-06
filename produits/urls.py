from django.contrib import admin
from django.urls import path,include,re_path
from .views import *


urlpatterns = [
        path('<str:slug>/', SingleProduct.as_view(),name='single_product'),
        path('', Shop.as_view(),name='shop'),
]
