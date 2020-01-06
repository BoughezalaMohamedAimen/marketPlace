from django.db import models
from django.contrib.auth.models import User
from produits.models import *
from datetime import datetime
from django.utils import timezone
# Create your models here.
class Cart(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    user=models.OneToOneField(User,on_delete=models.CASCADE,null='True',default=None)
    session_key = models.CharField(max_length=40)

    class Meta:
        unique_together = ('user', 'session_key',)


class CartItem(models.Model):
    total=models.PositiveIntegerField()
    produit=models.ForeignKey(Produit,on_delete=models.CASCADE)
    product_with_attribute=models.ForeignKey(ProductAttribute,on_delete=models.CASCADE,null='true',blank='true')
    qtt=models.PositiveIntegerField()
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)

    def update_total(self):
        try:
            self.total=self.qtt*self.product_with_attribute.prix if self.product_with_attribute.prix_promotionel==0 else self.qtt*self.product_with_attribute.prix_promotionel
        except:
            self.total=self.qtt*self.produit.prix if self.produit.prix_promotionel==0 else self.qtt*self.produit.prix_promotionel
        return self.total
