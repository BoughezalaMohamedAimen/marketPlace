from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from django.core.paginator import Paginator
#####---------------------------------------------------------------------------------------------------#####
#-------------------------------------WILAYAS-ADMIN-VIEWS--------------------------------------------------#
#####---------------------------------------------------------------------------------------------------#####



class WilayaAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        wilayas_list=Wilaya.objects.all()
        paginator = Paginator(wilayas_list, 25) # Show 25 contacts per page

        page = request.GET.get('page')
        wilayas = paginator.get_page(page)
        return render(request,'region/BackOffice/wilayas/home_wilayas.html', {'search':filter,'wilayas':wilayas,'wilayas_all_count':wilayas_list.count()})



class NewWilayaAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        return render(request,'region/BackOffice/wilayas/add_wilayas.html', {'form':WilayaForm()})

    def post(self,request):
        postt = request.POST.copy()
        postt.update({ 'user': request.user.id })
        form=WilayaForm(postt,request.FILES,request.user)
        if form.is_valid():
            form.save()
            return redirect('HomeWilayaAdmin')
        else:
            return render(request,'region/BackOffice/wilayas/add_wilayas.html', {'form':WilayaForm()})




class UpdateWilayaAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request,id=0):
        wilaya=Wilaya.objects.get(id=id)
        if request.user.is_superuser :
            form=WilayaFormUpdate(instance=wilaya)
            return render(request,'region/BackOffice/wilayas/update_wilayas.html', {'form':form})
        else:
            return redirect('profile')


    def post(self,request,id=0):
        wilaya=Wilaya.objects.get(id=id)
        # wilayaImageOld=wilaya.image.path
        if request.user.is_superuser :
            form=WilayaFormUpdate(request.POST,request.FILES,instance=wilaya)
            if form.is_valid():
                # if request.FILES:
                #     try:
                #         os.remove(wilayaImageOld)
                #     except:
                #         pass
                # else:
                #     print('none')
                form.save()
                return redirect('HomeWilayaAdmin')
            else:
                return render(request,'region/BackOffice/wilayas/update_wilayas.html', {'form':form})
        else:
            return redirect('HomeWilayaAdmin')


class DeleteWilayaAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        if request.GET.get('elements'):
            wilayas=Wilaya.objects.filter(id__in=request.GET.get('elements').split(','))
            for wilaya in wilayas:
                if request.user.is_superuser :
                    wilaya.delete()

            return redirect('HomeWilayaAdmin')







                            #------END-WILAYAS-ADMIN-VIEWS-----------#



#####---------------------------------------------------------------------------------------------------#####
#-------------------------------------PRODUCTS-ATTRIBUTES-ADMIN-VIEWS--------------------------------------------------#
#####---------------------------------------------------------------------------------------------------#####


class AttributesAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        return render(request,'BackOffice/home.html',{})

                                #------END-PRODUCTS-ATTRIBUTES-ADMIN-VIEWS-----------#
