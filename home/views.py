from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from produits.models import *
from cart.models import *
# Create your views here.

class HomeView(TemplateView):
    def get(self,request):
        produits=Produit.objects.all()
        cart=Cart.objects.get(user=request.user) if request.user.is_authenticated else Cart.objects.get(session_key = request.session.session_key)
        # print('**********************request.session.session_key***************************************************')
        # print(request.session.session_key)
        # print('*****************************************************************************************************')



        return render(request,'home/home.html',{'produits':produits,'cart':cart})
