from django.db import models
from django.contrib.auth.models import User
from cart.models import Cart
from produits.models import *
from datetime import datetime
from django.utils import timezone
from region.models import *
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User


COMMISSION_FIX=50

class Etat(models.Model):
    nom=models.CharField(max_length=55)


    def __str__(self):
        return str(self.nom)


class Commande(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    etat=models.ForeignKey(Etat,on_delete=models.CASCADE,default=Etat.objects.get(id=1))
    nom=models.CharField(max_length=255)
    adresse=models.CharField(max_length=325)
    wilaya=models.ForeignKey(Wilaya,on_delete=models.CASCADE)
    commune=models.ForeignKey(Commune,on_delete=models.CASCADE)
    email=models.EmailField()
    telephone=models.CharField(max_length=10)
    info=models.TextField(null='True',blank='True')
    remise=models.PositiveIntegerField(default=0)
    livraison=models.PositiveIntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank='True',null='True')
    def __str__(self):
        return str(self.created_at)

    def getTotal(self):
            items=CommandeItem.objects.filter(Commande=self)
            total=0
            for item in items:
                total+=item.total
            total+=self.livraison
            # print("***************************get  total")
            return total


    def getTotalProduis(self):
        items=CommandeItem.objects.filter(Commande=self)
        total=0
        for item in items:
            total+=item.total
        return total


    def readeablePhone(self):
        return "%s%s%s%s-%s%s%s-%s%s%s" % tuple(self.telephone)

    def has_product_of_user(self,user):
        for item in  CommandeItem.objects.filter(Commande=self):
            if item.get_vendor()==user:
                return True;
        return False

    def total_for_user(self,user):
            total=0;
            for item in CommandeItem.objects.filter(Commande=self,user=user.username):
                total+=item.total
            return total

    def update_solde(self):

        if self.etat.nom=='livré' and Commande.objects.get(id=self.id).etat.nom!='livré':
            for item in CommandeItem.objects.filter(Commande=self):
                user=item.get_vendor().userprofile
                user.solde+=item.total-COMMISSION_FIX-(item.total*item.commission/100)
                user.save()
        elif self.etat.nom!='livré' and Commande.objects.get(id=self.id).etat.nom=='livré':
            for item in CommandeItem.objects.filter(Commande=self):
                user=item.get_vendor().userprofile
                user.solde-=item.total-COMMISSION_FIX-(item.total*item.commission/100)
                user.save()

    def barre_code(self):
        barre_code=str(self.id)
        id_len=len(barre_code)
        for i in range (id_len,13):
            barre_code='0'+barre_code
        return barre_code







class CommandeItem(models.Model):
    total=models.PositiveIntegerField()
    produit=models.CharField(max_length=255)
    reference=models.CharField(max_length=255)
    prix=models.PositiveIntegerField()
    user=models.CharField(max_length=255)
    commission=models.PositiveIntegerField()
    qtt=models.PositiveIntegerField()
    Commande=models.ForeignKey(Commande,on_delete=models.CASCADE)

    def __str__(self):
        return " produit : %s qtt : %d , total: %d" %(self.produit,self.qtt,self.total)

    def get_vendor(self):
        try:
            return User.objects.get(username=self.user)
        except:
            return



@receiver(pre_save, sender=Commande)
def my_handler(sender, **kwargs):
    kwargs['instance'].livraison=kwargs['instance'].wilaya.prix
