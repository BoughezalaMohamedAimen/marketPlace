"""commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from region.views import GetCommune
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *

sitemaps={
    'produits':ProduitSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap,{'sitemaps':sitemaps}),
    path('robots.txt', include('robots.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^account/', include('accounts.urls')),
    re_path(r'^cart/',include('cart.urls')),
    re_path(r'^produits/',include('produits.urls')),
    re_path(r'^commande/',include('commandes.urls')),
    re_path(r'^BackOffice/',include('BackOffice.urls')),
    path('',include('home.urls')),
    path('commune/<int:id>',GetCommune,name='get_commune'),
]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header='Administration du Site'
