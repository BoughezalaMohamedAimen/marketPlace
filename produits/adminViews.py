from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .forms import *
from .models import *
from categories.models import *
from django.core.paginator import Paginator
import datetime
import os

#####---------------------------------------------------------------------------------------------------#####
#-------------------------------------PRODUCTS-ADMIN-VIEWS--------------------------------------------------#
#####---------------------------------------------------------------------------------------------------#####



class ProductAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        products_of_user=Produit.objects.filter(user=request.user)
        filter_data={ }
        if request.GET.get('cat'):
            filter_data['categorie__id__in']=request.GET.get('cat').split(',')
        if not request.user.is_superuser:
            filter_data['user']=request.user

        if request.GET.get('etat')=='valid':
            filter_data['valid']=True
        if request.GET.get('etat')=='wait':
            filter_data['motif__isnull']=True
            filter_data['valid']=False


        q = Q()
        if request.GET.get('keyword'):
            for mot_cle in request.GET.get('keyword').split(','):
                q |= Q(nom__contains=mot_cle)
                q |= Q(description__contains=mot_cle)
                q |= Q(seo__contains=mot_cle)
                q |= Q(categorie__nom__contains=mot_cle)
                q |= Q(categorie__nom__contains=mot_cle)
                if request.user.is_superuser:
                    q |= Q(user__username__contains=mot_cle)

        if request.GET.get('etat')=='invalid':
            filter_data['valid']=False
            if q:
                products_list=Produit.objects.all().filter(**filter_data).filter(q).exclude(motif__isnull='True').order_by('-updated')
            else:
                products_list=Produit.objects.all().filter(**filter_data).exclude(motif__isnull='True').order_by('-updated')
        else:
            if q:
                products_list=Produit.objects.all().filter(**filter_data).filter(q).order_by('-updated')
            else:
                products_list=Produit.objects.all().filter(**filter_data).order_by('-updated')


        paginator = Paginator(products_list, 50) # Show 25 contacts per page

        page = request.GET.get('page')
        products = paginator.get_page(page)
        context={
        'search':filter,
        'products':products,
        'products_all_count':products_list.count(),
        'categories':Categorie.objects.all(),
        'valid_products':products_of_user.filter(valid='True').count(),
        'wait_products':products_of_user.filter(valid='False',motif__isnull='True').count(),
        'invalid_products':products_of_user.filter(valid='False').exclude(motif__isnull='True').count(),
        'user_product_count':Produit.objects.filter(user=request.user).count()
        }
        return render(request,'produits/BackOffice/products/home_product.html',context)



class NewProductAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        attributes=Attribute.objects.all()
        return render(request,'produits/BackOffice/products/add_product.html', {'form':ProductForm(),'attributes':attributes,'categories':Categorie.objects.all()})

    def post(self,request):
        postt = request.POST.copy()
        postt.update({ 'user': request.user.id })
        form=ProductForm(postt,request.FILES,request.user)
        if form.is_valid():
            form.save()
            return redirect('HomeProductAdmin')
        else:
            return render(request,'produits/BackOffice/products/add_product.html', {'form':ProductForm()})




class UpdateProduitAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request,id=0):
        produit=Produit.objects.get(id=id)
        if request.user.is_superuser or request.user==produit.user :
            form=ProduitFormUpdate(instance=produit)
            attributes=Attribute.objects.all()
            return render(request,'produits/BackOffice/products/update_produits.html', {'form':form,'product':Produit.objects.get(id=id),'categories':Categorie.objects.all()})
        else:
            return redirect('profile')


    def post(self,request,id=0):
        produit=Produit.objects.get(id=id)
        produitImageOld=produit.image.path
        produitImage2Old=produit.image2.path
        produitImage3Old=produit.image3.path
        produitImage4Old=produit.image4.path
        if request.user.is_superuser or request.user==produit.user :
            produit.updated=datetime.datetime.now()
            form=ProduitFormUpdate(request.POST,request.FILES,instance=produit)
            if form.is_valid():
                if request.FILES:
                    if request.FILES.get('image'):
                        print('image1')
                        try:
                            os.remove(produitImageOld)
                        except Exception as e:
                            print(e)
                    if request.FILES.get('image2'):
                        try:
                            os.remove(produitImage2Old)
                        except:
                            pass
                    if request.FILES.get('image3'):
                        try:
                            os.remove(produitImage3Old)
                        except:
                            pass
                    if request.FILES.get('image4'):
                        try:
                            os.remove(produitImage4Old)
                        except:
                            pass


                form.save()
                return redirect('HomeProductAdmin')
            else:
                return render(request,'produits/BackOffice/products/update_produits.html', {'form':form})
        else:
            return redirect('HomeProductAdmin')


class ProduitCategorieBulkAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        if request.GET.get('elementsBulk'):
            produits=Produit.objects.filter(id__in=request.GET.get('elementsBulk').split(','))
            for produit in produits:
                if request.user.is_superuser or request.user==produit.user :
                    produit.categorie=Categorie.objects.get(id=request.GET.get('catBulk'))
                    produit.save()

            return redirect('HomeProductAdmin')


class DeleteProduitAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        if request.GET.get('elements'):
            produits=Produit.objects.filter(id__in=request.GET.get('elements').split(','))
            for produit in produits:
                if request.user.is_superuser or request.user==produit.user :
                    produit.delete()

            return redirect('HomeProductAdmin')







                            #------END-PRODUCTS-ADMIN-VIEWS-----------#


#####---------------------------------------------------------------------------------------------------#####
#-------------------------------------PRODUCTS-ATTRIBUTES-ADMIN-VIEWS--------------------------------------------------#
#####---------------------------------------------------------------------------------------------------#####


class HomeProductAttributeAdmin(LoginRequiredMixin,TemplateView):

    def get(self,request,id=0):
        produit=Produit.objects.get(id=id)
        productattributes=ProductAttribute.objects.filter(produit=produit)
        # form=ProductAttributeFormset()
        if request.user.is_superuser or request.user==produit.user :
            attributes=Attribute.objects.all()
            return render(request,'produits/BackOffice/attributes/productAttribute.html', {'product':produit,'attributes':attributes,'productattributes':productattributes})
        else:
            return redirect('profile')


    def post(self,request,id=0):
        try:
            produit_exists=Produit.objects.get(id=id)
        except:
            return redirect('updateProductAttribute',id)

        if request.user.is_superuser or request.user==produit_exists.user :
            posted_data = request.POST
            product_attribute_length=int(posted_data.get('lentgh'))
            for prdct_with_attr_no in range(product_attribute_length):
                kwargs={
                'stock':posted_data.get('form-'+str(prdct_with_attr_no)+'-stock'),
                'produit':produit_exists.id,
                'prix':posted_data.get('form-'+str(prdct_with_attr_no)+'-prix'),
                'attributevalues':dict(posted_data).get('form-'+str(prdct_with_attr_no)+'-attributevalues'),
                }

                # print(dict(posted_data).get('form-1-attributevalues'))


                product_with_attribute_exist = produit_exists.getProductAttribute(kwargs['attributevalues'])
                # print('************')
                # print(product_with_attribute_exist)
                if len(product_with_attribute_exist)==1:
                    # print('************')
                    p=product_with_attribute_exist.first()
                    p.stock=kwargs['stock']
                    p.prix=kwargs['prix']
                    p.save()
                else:
                    new_product_with_attribute=ProductAttributeForm(kwargs)
                    if new_product_with_attribute.is_valid():
                        new_product_with_attribute.save()
                    else:
                        print('******** invalid FROM ELSE**************')
                        print(kwargs)
                        print('********** ERRORS ************')
                        print(new_product_with_attribute.errors)

            return redirect('updateProductAttribute',id)

        else:
            return render(request,'produits/BackOffice/products/home_product.html', {})



class DeleteProductAttributeAdmin(LoginRequiredMixin,TemplateView):
    def get(self,request):
        if request.GET.get('elements'):
            products_with_attributes=ProductAttribute.objects.filter(id__in=request.GET.get('elements').split(','))
            produit=products_with_attributes.first().produit.id
            print('******** invalid**************')
            print(produit)
            print('********** invalid ************')
            for product_with_attribute in products_with_attributes:
                if request.user == product_with_attribute.produit.user or request.user.is_superuser:
                    product_with_attribute.delete()
            try:
                return redirect('updateProductAttribute',produit)
            except:
                return redirect('HomeProductAdmin')
                            #------END-PRODUCTS-ATTRIBUTES-ADMIN-VIEWS-----------#
