from django.db import models

# Create your models here.
class Wilaya(models.Model):
    nom=models.CharField(max_length=255)
    code=models.PositiveIntegerField()
    prix=models.PositiveIntegerField()

    def __str__(self):
        return self.nom

class Commune(models.Model):
    nom=models.CharField(max_length=255)
    wilaya=models.ForeignKey(Wilaya,on_delete=models.CASCADE)

    def __str__(self):
        return self.nom
