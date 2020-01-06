from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .forms import *
from .models import *
from django.core.paginator import Paginator
import datetime
from django.http import HttpResponse
from .utils import render_to_pdf


#####---------------------------------------------------------------------------------------------------#####
#-------------------------------------COMMANDES-ADMIN-VIEWS--------------------------------------------------#
#####---------------------------------------------------------------------------------------------------#####


class CommandeAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        filter_data={ }
        # FOR DJANGO 3# if not request.user.is_superuser:
        #     filter_data['CartItem__produit__user']=request.user

        if request.GET.get('mindate'):
            filter_data['updated_at__gt']=datetime.datetime.strptime(request.GET.get('mindate')+':00', "%d-%m-%Y %H:%M:%S")
        if request.GET.get('maxdate'):
            filter_data['updated_at__lt']=datetime.datetime.strptime(request.GET.get('maxdate')+':00', "%d-%m-%Y %H:%M:%S")
        q = Q()
        if request.GET.get('keyword'):
            for mot_cle in request.GET.get('keyword').split(','):
                q |= Q(nom__contains=mot_cle)
                q |= Q(email__contains=mot_cle)
                q |= Q(adresse__contains=mot_cle)
                q |= Q(info__contains=mot_cle)
                q |= Q(wilaya__nom__contains=mot_cle)
                q |= Q(etat__nom__contains=mot_cle)


        if q:
            commandes_list=Commande.objects.filter(**filter_data).filter(q).order_by('-created_at')
        else:
            commandes_list=Commande.objects.filter(**filter_data).order_by('-created_at')
        if not request.user.is_superuser:
            for commande in commandes_list:
                if not commande.has_product_of_user(request.user):
                    commandes_list=commandes_list.exclude(id=commande.id)






        paginator = Paginator(commandes_list, 50) # Show 25 contacts per page

        page = request.GET.get('page')
        commandes = paginator.get_page(page)
        context={
        'search':filter,
        'commandes':commandes,
        'commandes_all_count':commandes_list.count(),
        'etats':Etat.objects.all(),
        }
        return render(request,'commandes/BackOffice/home_commande.html',context)



class CommandePasseAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        commandes_list=Commande.objects.filter(user=request.user).order_by('-created_at')
        paginator = Paginator(commandes_list, 50) # Show 25 contacts per page

        page = request.GET.get('page')
        commandes = paginator.get_page(page)
        context={
        'commandes':commandes,
        'commandes_all_count':commandes_list.count(),
        }
        return render(request,'commandes/BackOffice/home_commande_passe.html',context)


class SingleCommande(LoginRequiredMixin,TemplateView):
    def get(self,request,id):
        return render(request,'commandes/BackOffice/update_commande.html',{'commande':Commande.objects.get(id=id)})




class DeleteCommande(LoginRequiredMixin,TemplateView):
    def get(self,request):
        if request.GET.get('elements'):
            commandes=Commande.objects.filter(id__in=request.GET.get('elements').split(','))
            for commande in commandes:
                if request.user.is_superuser :
                    commande.delete()
        return redirect('HomeCommandeAdmin')




class CommandeEtatBulk(LoginRequiredMixin,TemplateView):
    def post(self,request):
        if request.POST.get('elementsBulk'):
            commandes=Commande.objects.filter(id__in=request.POST.get('elementsBulk').split(','))
            for commande in commandes:
                if request.user.is_superuser :
                    commande.etat=Etat.objects.get(id=request.POST.get('etatBulk'))
                    commande.updated_at=datetime.datetime.now()
                    commande.update_solde()
                    commande.save()

            return redirect('HomeCommandeAdmin')

##############################################################################################################################
#                                      GENERATING PDF
###############################################################################################################################
class CommandePDF(LoginRequiredMixin,TemplateView):
        def get(self,request):
            if request.user.is_superuser:
                filter_data={ }
                    # FOR DJANGO 3# if not request.user.is_superuser:
                    #     filter_data['CartItem__produit__user']=request.user

                if request.GET.get('mindate'):
                    filter_data['updated_at__gt']=datetime.datetime.strptime(request.GET.get('mindate')+':00', "%d-%m-%Y %H:%M:%S")
                if request.GET.get('maxdate'):
                    filter_data['updated_at__lt']=datetime.datetime.strptime(request.GET.get('maxdate')+':00', "%d-%m-%Y %H:%M:%S")
                q = Q()
                if request.GET.get('keyword'):
                    for mot_cle in request.GET.get('keyword').split(','):
                        q |= Q(nom__contains=mot_cle)
                        q |= Q(email__contains=mot_cle)
                        q |= Q(adresse__contains=mot_cle)
                        q |= Q(info__contains=mot_cle)
                        q |= Q(wilaya__nom__contains=mot_cle)
                        q |= Q(etat__nom__contains=mot_cle)


                if q:
                    commandes_list=Commande.objects.filter(**filter_data).filter(q).order_by('-created_at')
                else:
                    commandes_list=Commande.objects.filter(**filter_data).order_by('-created_at')
                    pdf = render_to_pdf('commandes/BackOffice/commande_pdf.html',{'commandes':commandes_list})
                    return HttpResponse(pdf, content_type='application/pdf')
            else:
                return redirect('HomeCommandeAdmin')
