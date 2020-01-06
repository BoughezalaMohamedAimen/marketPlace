from django.db import models
from categories.models import *
from datetime import datetime
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Count



class Motif(models.Model):
    description=models.CharField(max_length=255)

    def __str__(self):
        return self.description

# Create your models here.
class Produit(models.Model):
    created= models.DateTimeField(default=datetime.now, blank='True')
    updated= models.DateTimeField(default=datetime.now, blank='True')
    reference=models.CharField(max_length=255,default='reference',blank='True')
    nom=models.CharField(max_length=255)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    slug = models.SlugField(blank='True',max_length=255)
    valid=models.BooleanField(default=False)
    description= RichTextField(config_name='awesome_ckeditor')
    motif=models.ForeignKey(Motif,on_delete=models.CASCADE,blank='True',null='True')
    categorie=models.ForeignKey(Categorie,on_delete=models.CASCADE)
    seo=models.CharField(max_length=255,null='True',blank='True')
    prix=models.PositiveIntegerField(default=0)
    stock=models.PositiveIntegerField(null='True')
    prix_promotionel=models.PositiveIntegerField(default=0)
    # attribut=models.ManyToManyField(Attribut,null='True')
    image=models.ImageField(upload_to='product',blank='True',null='True')
    image2=models.ImageField(upload_to='product',blank='True',null='True')
    image3=models.ImageField(upload_to='product',blank='True',null='True')
    image4=models.ImageField(upload_to='product',blank='True',null='True')

    def __str__(self):
        return self.nom



    def get_absolute_url(self):
        return reverse('single_product',args=[str(self.slug)])

    def getProductAttribute(self,attribute_values):
        product_with_attribute_exist = ProductAttribute.objects.annotate(count=Count('attributevalues')).filter(count=len(attribute_values))

        for pk in attribute_values:
            product_with_attribute_exist = product_with_attribute_exist.filter(attributevalues__pk=pk,produit=self)
        return product_with_attribute_exist;


    def save(self, *args, **kwargs):
        self.slug=slugify(self.nom)+'-'+slugify(self.categorie.nom)+'-'+self.user.userprofile.wilaya.nom+'-algerie-annonce-vente-en-ligne-livraison-a-domicile'
        if self.id:
            self.slug+='-'+str(self.id)
        super().save(*args, **kwargs)
        if self.slug.split('-')[-1]!=str(self.id):
            print(self.slug.split('-')[-1])
            self.slug+='-'+str(self.id)
            super().save(*args, **kwargs)








class Attribute(models.Model):
    nom=models.CharField(max_length=255)
    def __str__(self):
        return self.nom

class AttributeValue(models.Model):
    value=models.CharField(max_length=255)
    attribute=models.ForeignKey(Attribute,on_delete=models.CASCADE)
    def __str__(self):
        return self.value


class ProductAttribute(models.Model):
    produit=models.ForeignKey(Produit,on_delete=models.CASCADE)
    reference=models.CharField(max_length=255,default='reference',blank='True')
    prix=models.PositiveIntegerField(blank='True',null='True')
    stock=models.PositiveIntegerField(blank='True',default=0)
    attributevalues=models.ManyToManyField(AttributeValue)

    def getValues(self):
        values=''
        for attributevalue in self.attributevalues.all():
            values+= attributevalue.value+','
        return values[0:-1]

    def allattributevalues(self):
        return self.attributevalues.all()


    # class Meta:
    #     unique_together = ('produit', 'attributevalues',)


from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver


@receiver(pre_save, sender=ProductAttribute)
def my_handler(sender, **kwargs):
    if not kwargs['instance'].prix:
        kwargs['instance'].prix=kwargs['instance'].produit.prix
