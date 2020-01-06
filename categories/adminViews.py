from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from django.core.paginator import Paginator
#####---------------------------------------------------------------------------------------------------#####
#-------------------------------------categories-ADMIN-VIEWS--------------------------------------------------#
#####---------------------------------------------------------------------------------------------------#####



class CategorieAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        categories_list=Categorie.objects.all()
        paginator = Paginator(categories_list, 25) # Show 25 contacts per page

        page = request.GET.get('page')
        categories = paginator.get_page(page)
        return render(request,'categories/BackOffice/categories/home_categorie.html', {'search':filter,'categories':categories,'categories_all_count':categories_list.count()})



class NewCategorieAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        return render(request,'categories/BackOffice/categories/add_categorie.html', {'form':CategorieForm()})

    def post(self,request):
        postt = request.POST.copy()
        postt.update({ 'user': request.user.id })
        form=CategorieForm(postt,request.FILES,request.user)
        if form.is_valid():
            form.save()
            return redirect('HomeCategorieAdmin')
        else:
            return render(request,'categories/BackOffice/categories/add_categorie.html', {'form':CategorieForm()})




class UpdateCategorieAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request,id=0):
        categorie=Categorie.objects.get(id=id)
        if request.user.is_superuser :
            form=CategorieFormUpdate(instance=categorie)
            return render(request,'categories/BackOffice/categories/update_categorie.html', {'form':form})
        else:
            return redirect('profile')


    def post(self,request,id=0):
        categorie=Categorie.objects.get(id=id)
        # categorieImageOld=categorie.image.path
        if request.user.is_superuser :
            form=CategorieFormUpdate(request.POST,request.FILES,instance=categorie)
            if form.is_valid():
                # if request.FILES:
                #     try:
                #         os.remove(categorieImageOld)
                #     except:
                #         pass
                # else:
                #     print('none')
                form.save()
                return redirect('HomeCategorieAdmin')
            else:
                return render(request,'categories/update_categories.html', {'form':form})
        else:
            return redirect('HomeCategorieAdmin')



class DeleteCategorieAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        if request.GET.get('elements'):
            produits=Categorie.objects.filter(id__in=request.GET.get('elements').split(','))
            for produit in produits:
                if request.user.is_superuser :
                    produit.delete()

            return redirect('HomeCategorieAdmin')

                            #------END-categories-ADMIN-VIEWS-----------#
