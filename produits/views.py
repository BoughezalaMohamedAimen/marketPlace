from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from .models import *
from django.http import HttpResponse
# Create your views here.

#
class SingleProduct(TemplateView):
    def get(self,request,slug):
        try:
            produit=Produit.objects.get(slug=slug)
        except:
            return HttpResponse(status=404)
        random=Produit.objects.order_by('?')[:4]
        return render(request,'produits/single_product.html',{'produit':produit,'random_products':random })


class Shop(TemplateView):
    def get(self,request):
        produits=Produit.objects.filter(valid='True')
        return render(request,'produits/shop/shop.html',{'produits':produits})
