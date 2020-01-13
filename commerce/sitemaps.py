from django.contrib.sitemaps import Sitemap
from produits.models import Produit



class ProduitSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Produit.objects.all()

    def lastmod(self, obj):
        return obj.updated
