from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .forms import *
import os
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from commandes.models import *

from django.contrib.auth import authenticate, login
# Create your views here.

class HomeAccount(LoginRequiredMixin,TemplateView):
    def get(self,request):
        return render(request,'accounts/profile.html')

class Login(TemplateView):
    def get(self,request):
        return render(request,'accounts/login.html')

class Register(TemplateView):
    def get(self,request):
        form=RegistrationForm()
        profile_form=UserProfileRgistrationForm()
        return render(request,'accounts/register.html',{'form':form,'profile_form':profile_form})
    def post(self,request):
            form=RegistrationForm(request.POST or None,prefix='user')
            if form.is_valid():
                form.save()
                user=User.objects.get(email=form.cleaned_data['email'])
                account=UserProfile.objects.get(user=user)
                profile_form=UserProfileRgistrationForm(request.POST or None,prefix='profile',instance=account)
                if profile_form.is_valid():
                    profile_form.save()
                    send_mail('activation du compte','http://127.0.0.1:8000/account/activate/'+user.username+'/'+account.activate,'aaaa@mailmail.com',[user.email])
                else:
                    user.delete()
                    return render(request,'accounts/register.html',{'form':form,'profile_form':profile_form})

                return redirect('login')
            else:
                return render(request,'accounts/register.html',{'form':form,'profile_form':UserProfileRgistrationForm(request.POST)})

class Profile(LoginRequiredMixin,TemplateView):
    def get(self,request):
        return render (request,'accounts/profile.html')





class EditProfile(LoginRequiredMixin,TemplateView):
    def get(self,request):
        form=EditProfileForm(instance=request.user.userprofile)
        userForm=EditUserForm(instance=request.user)
#--------------------------------- GETTING THE USER MONTHLY COMMANDS -----------------------------------------##############
        now = datetime.now()
        year=now.year
        month=now.month
        day=now.day
        commandes_list=Commande.objects.filter(created_at__year=year,created_at__month=month)
        for commande in commandes_list:
            if not commande.has_product_of_user(request.user):
                commandes_list=commandes_list.exclude(id=commande.id)

#-----------------------------------------------------------------------------------------------------


        return render (request,'accounts/edit_profile.html',{'form':form,'userForm':userForm,'commande_m':commandes_list})
    def post(self,request):
    ##---------------------------------------- GETTING THE USER MONTHLY COMMANDS ##################################################################
        now = datetime.now()
        year=now.year
        month=now.month
        day=now.day
        commandes_list=Commande.objects.filter(created_at__year=year,created_at__month=month)
        for commande in commandes_list:
            if not commande.has_product_of_user(request.user):
                commandes_list=commandes_list.exclude(id=commande.id)

#------------------------------------------------------------------------------
        form=EditProfileForm(request.POST, prefix='profile',instance=request.user.userprofile)
        userForm=EditUserForm(request.POST,prefix='user',instance=request.user)

        if userForm.is_valid():
            print('saved user')
            userForm.save()
        else:
            return render (request,'accounts/edit_profile.html',{'form':form,'userForm':userForm,'commande_m':commandes_list})

        if form.is_valid():
            print('saved profile')
            form.save()
            return redirect('edit_profile')
        else:
            print(form.errors)
            return render (request,'accounts/edit_profile.html',{'form':form,'userForm':userForm,'message':'profile','commande_m':commandes_list})



class ChangePassword(LoginRequiredMixin,TemplateView):
    def get(self,request):
        form=PasswordChangeForm(user=request.user)
        return render (request,'accounts/change_password.html',{'form':form})
    def post(self,request):
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render (request,'accounts/change_password.html',{'form':form})


def  ActivateAccount(request,username,activate):
    user=User.objects.get(username=username)
    account=UserProfile.objects.get(user=user)
    print(activate)
    print(account.activate)
    if activate==account.activate:
        user.is_active=True
        user.save()
        new_user = authenticate(username=user.email,
                                    password=user.password,
                                    )
        login(request, user)
        return redirect('edit_profile')
    else:
        return redirect('activate_account_form')

class ActivateAccountForm(TemplateView):
    def get(self,request):
        form=activateAccountForm()
        return render (request,'accounts/activate_account_form.html',{'form':form})
    def post(self,request):
        form=activateAccountForm(request.POST or None)
        if form.is_valid():
            try:
                user=User.objects.get(email=form.cleaned_data['email'])
                account=UserProfile.objects.get(user=user)
                send_mail('activation du compte','/account/activate/'+user.username+'/'+account.activate,'aaaa@mailmail.com',[user.email])
                return render(request,'accounts/activate_account_form.html',{'message':'un e-mail de confirmation e bien été envoyé'})
            except User.DoesNotExist:
                return render (request,'accounts/activate_account_form.html',{'form':form})

        return render (request,'accounts/activate_account_form.html',{'form':form})
