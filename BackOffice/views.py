from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from produits.adminViews import *
from categories.adminViews import *
from region.adminViews import *
from commandes.adminViews import *
from accounts.adminViews import *
from produits.models import *

import datetime
#####---------------------------------------------------------------------------------------------------#####
#--------------------------------------ADMIN-HOME-VIEW--------------------------------------------------#
#####---------------------------------------------------------------------------------------------------#####

class HomeAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        now = datetime.datetime.now()
        year=now.year
        month=now.month
        day=now.day
        commandes_a=Commande.objects.filter(created_at__year=year)
        commandes_m=Commande.objects.filter(created_at__year=year,created_at__month=month)
        commande_annuels=0
        for commande in commandes_a:
            if request.user.is_superuser:
                commande_annuels+=commande.getTotal()
            else:
                commande_annuels+=commande.total_for_user(request.user)
        commande_mensuels=0
        for commande in commandes_m:
            if request.user.is_superuser:
                commande_mensuels+=commande.getTotal()
            else:
                commande_mensuels+=commande.total_for_user(request.user)

        context={
        'commande_annuels':commande_annuels  ,
        'commande_mensuels': commande_mensuels ,
        'total_vendeurs':User.objects.all().count()  ,
        'total_produits':Produit.objects.filter(user=request.user).count() ,
        }
        return render(request,'BackOffice/home.html',context)
                            #------END-ADMIN-HOME-VIEW-----------#






#####---------------------------------------------------------------------------------------------------#####
#-------------------------------------CATEGORIES-ADMIN-VIEWS--------------------------------------------------#
#####---------------------------------------------------------------------------------------------------#####


#
#
# class CategoriesAdmin(LoginRequiredMixin,TemplateView):
#     def get(self,request):
#         return render(request,'BackOffice/home.html',{})

                                #------END-CATEGORIES-ADMIN-VIEWS-----------#
