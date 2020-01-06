from django.contrib import admin
from django.urls import path,include,re_path
from .views import *


urlpatterns = [
        path('add/<int:id>', AddToCart.as_view(),name='add_to_cart'),
        path('delete/<int:id>',DeleteCart.as_view(),name='delete_from_cart'),
        path('update/<int:id>/<int:qtt>/', UpdateCart.as_view(),name='update_cart'),
]
