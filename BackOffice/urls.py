from django.contrib import admin
from django.urls import path,include,re_path
from .views import *


urlpatterns = [
        # path('', HomeAdmin.as_view(),name='HomeAdmin'),
        #       PRODUCT ADMIN  URLS
        path('products/', ProductAdmin.as_view(),name='HomeProductAdmin'),
        path('products/add', NewProductAdmin.as_view(),name='NewProduct'),
        path('products/update/<int:id>', UpdateProduitAdmin.as_view(),name='UpdateProduit'),
        path('product/categorie-bulk/', ProduitCategorieBulkAdmin.as_view(),name='ProduitCategorieBulk'),
        path('products/delete/', DeleteProduitAdmin.as_view(),name='DeleteProduct'),
        path('products/update/attribute/<int:id>', HomeProductAttributeAdmin.as_view(),name='updateProductAttribute'),
        path('products-with-attribute/delete/', DeleteProductAttributeAdmin.as_view(),name='DeleteProductAttribute'),



        #       COMMANDES ADMIN  URLS
        path('commandes/', CommandeAdmin.as_view(),name='HomeCommandeAdmin'),
        path('commandes/passe', CommandePasseAdmin.as_view(),name='HomeCommandePasseAdmin'), 
        path('commandes/<int:id>', SingleCommande.as_view(),name='SingleCommande'),
        path('commandes/delete/', DeleteCommande.as_view(),name='DeleteCommande'),
        path('commandes/etat-bulk/', CommandeEtatBulk.as_view(),name='CommandeEtatBulk'),
        path('commandes/pdf/', CommandePDF.as_view(),name='CommandePDF'),

        #       ACCOUNTS ADMIN  URLS

        path('accounts/', AccountAdmin.as_view(),name='HomeAccountAdmin'),
        path('payments/', PayementAdmin.as_view(),name='HomePaymentAdmin'),
        path('payments/delete/<int:id>', DeletePayementAdmin.as_view(),name='DeletePaymentAdmin'),


        # #       REGIONS ADMIN  URLS
        # path('regions/', WilayaAdmin.as_view(),name='HomeWilayaAdmin'),
        # path('regions/add', NewWilayaAdmin.as_view(),name='NewWilaya'),
        # path('regions/update/<int:id>', UpdateWilayaAdmin.as_view(),name='UpdateWilaya'),
        # path('regions/delete/', DeleteWilayaAdmin.as_view(),name='DeleteWilaya'),
        #
        # #       CATEGORIES ADMIN  URLS
        # path('categories/', CategorieAdmin.as_view(),name='HomeCategorieAdmin'),
        # path('categories/add', NewCategorieAdmin.as_view(),name='NewCategorie'),
        # path('categories/update/<int:id>', UpdateCategorieAdmin.as_view(),name='UpdateCategorie'),
        # path('categories/delete/', DeleteCategorieAdmin.as_view(),name='DeleteCategorie'),
]
