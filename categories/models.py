from django.db import models
from django.utils.text import slugify


# Create your models here.
class Categorie(models.Model):
    nom=models.CharField(max_length=255)
    slug = models.SlugField(unique='True')
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null='True',blank='True')
    image=models.ImageField(null='True',blank='True',upload_to='categories')
    commission=models.PositiveIntegerField(default=5)

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.nom]                  # post.  use __unicode__ in place of
                                                 # __str__ if you are using python 2
        k = self.parent

        while k is not None:
            full_path.append(k.nom)
            k = k.parent

        return ' -> '.join(full_path[::-1])

        #    TODO SEO CATEGORIE
    # def get_absolute_url(self):
    #     return reverse('single_categorie',args=[str(self.slug)])


    def save(self, *args, **kwargs):
            self.slug=slugify(self.nom)
            super().save(*args, **kwargs)



    def update(self, *args, **kwargs):
            self.slug=slugify(self.nom)+' '+str(self.id)
            super().update(*args, **kwargs)
