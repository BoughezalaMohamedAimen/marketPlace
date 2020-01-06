from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from produits.models import *
from .models import *
from django.http import HttpResponse
# Create your views here.

class AddToCart(TemplateView):
    def get(self,request,id):
        produit=Produit.objects.get(id=id)
        cart=Cart.objects.get(user=request.user) if request.user.is_authenticated else Cart.objects.get(session_key = request.session.session_key)
        cart.save()
        try:
            if request.GET.get('attr'):
                attributes=ProductAttribute.objects.get(id=request.GET.get('attr'))
                cartitem=CartItem.objects.get(cart=cart,produit=produit,product_with_attribute=attributes)
            else:
                cartitem=CartItem.objects.get(cart=cart,produit=produit)
            cartitem.qtt+=1
            cartitem.update_total()
            cartitem.save()
            return HttpResponse(status=200)
        except CartItem.DoesNotExist:
            if request.GET.get('attr'):
                try:
                    attributes=ProductAttribute.objects.get(id=request.GET.get('attr'))
                    total=attributes.prix if attributes.prix else produit.prix
                    cartitem=CartItem(cart=cart,produit=produit,qtt=1,product_with_attribute=attributes,total=total)
                except Exception as e:
                     print(e)
                    # return HttpResponse(status=500)
            else:
                cartitem=CartItem(cart=cart,produit=produit,qtt=1,total=produit.prix)
            cartitem.save()
            return render(request,'cart/add_to_cart.html',{'cartItem':cartitem})
#
class UpdateCart(TemplateView):
    def get(self,request,id,qtt):
        produit=Produit.objects.get(id=id)
        cart=Cart.objects.get(user=request.user) if request.user.is_authenticated else Cart.objects.get(session_key = request.session.session_key)
        if request.GET.get('attr'):
            attributes=ProductAttribute.objects.get(id=request.GET.get('attr'))
            cartitem=CartItem.objects.get(cart=cart,produit=produit,product_with_attribute=attributes)
        else:
            cartitem=CartItem.objects.get(cart=cart,produit=produit)
        cartitem.qtt=qtt
        cartitem.update_total()
        cartitem.save()
        return HttpResponse(status=200)

class DeleteCart(TemplateView):
    def get(self,request,id):
        cart=Cart.objects.get(user=request.user) if request.user.is_authenticated else Cart.objects.get(session_key = request.session.session_key)
        try:
            CartItem.objects.get(id=id).delete()
            return render(request,'cart/cart-remove.html')
        except:
            return HttpResponse(status=404)
