from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import UserPaymentForm,DemandePayementForm



#####---------------------------------------------------------------------------------------------------#####
#-------------------------------------ACCOUNTS-ADMIN-VIEWS--------------------------------------------------#
#####---------------------------------------------------------------------------------------------------#####

class AccountAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        if request.user.is_superuser:
            q = Q()
            if request.GET.get('keyword'):
                q |= Q(user__username__contains=request.GET.get('keyword'))
                q |= Q(user__first_name__contains=request.GET.get('keyword'))
                q |= Q(user__last_name__contains=request.GET.get('keyword'))
                q |= Q(user__username__contains=request.GET.get('keyword'))
                q |= Q(user__email__contains=request.GET.get('keyword'))
                q |= Q(wilaya__nom__contains=request.GET.get('keyword'))
                q |= Q(adresse__contains=request.GET.get('keyword'))
            if q:
                users_list=UserProfile.objects.filter(q).order_by('-id')
            else:
                users_list=UserProfile.objects.all().order_by('-id')
            paginator = Paginator(users_list, 50) # Show 25 contacts per page
            page = request.GET.get('page')
            users = paginator.get_page(page)
            context={
                    # 'search':filter,
                    'userprofiles':users,
                    'userprofiles_all_count':users_list.count(),
                    'payment_form':UserPaymentForm()
                    }
            return render(request,'accounts/BackOffice/home_users.html',context)
        else:
            return redirect('HomeAdmin')




    def post(self,request):
        if request.user.is_superuser:
            form=UserPaymentForm(request.POST)
            if form.is_valid():
                form.save()

        return redirect('HomeAccountAdmin')



#####---------------------------------------------------------------------------------------------------#####
#-------------------------------------PAYEMENTS-ADMIN-VIEWS--------------------------------------------------#
#####---------------------------------------------------------------------------------------------------#####

class PayementAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        filter_data={ }
        if not request.user.is_superuser:
            filter_data['user']=request.user

        if request.GET.get('mindate'):
            filter_data['created__gt']=datetime.strptime(request.GET.get('mindate')+':00', "%d-%m-%Y %H:%M:%S")
        if request.GET.get('maxdate'):
            filter_data['created__lt']=datetime.strptime(request.GET.get('maxdate')+':00', "%d-%m-%Y %H:%M:%S")

        q = Q()
        if request.user.is_superuser:
            if request.GET.get('keyword'):
                q |= Q(user__username__contains=request.GET.get('keyword'))
                q |= Q(user__email__contains=request.GET.get('keyword'))
                q |= Q(user__userprofile__wilaya__nom__contains=request.GET.get('keyword'))
                q |= Q(observation__contains=request.GET.get('keyword'))

        if q:
            payments_list=Payement.objects.filter(**filter_data).filter(q).order_by('-created')

        else:
            payments_list=Payement.objects.filter(**filter_data).order_by('-created')


        paginator = Paginator(payments_list, 50) # Show 25 contacts per page
        page = request.GET.get('page')
        payments = paginator.get_page(page)
        context={
                # 'search':filter,
                'payments':payments,
                'payments_all_count':payments_list.count(),
                'payment_form':UserPaymentForm()
                }
        return render(request,'accounts/BackOffice/home_payment.html',context)




class DeletePayementAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request,id):
        if request.user.is_superuser :
            payment=Payement.objects.get(id=id)
            payment.delete()
            return redirect('HomePaymentAdmin')
        else:
            return redirect('HomeAdmin')

class DemandePayementAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        form=DemandePayementForm()
        return render(request,'accounts/BackOffice/demande_payement_form.html',{'form':form})

    def post(self,request):
        form=DemandePayementForm(request.POST)
        if form.is_valid():
            demande=form.save(commit=False)
            demande.user=request.user
            demande.save()
            return redirect('HomeAccountAdmin')
        else:
            return render(request,'accounts/BackOffice/demande_payement_form.html',{'form':form})
