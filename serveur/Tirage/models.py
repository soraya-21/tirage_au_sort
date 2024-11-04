from django.db import models

# Create your models here.
class NameModel(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

class Pays(NameModel):
    pass

class Championnat(NameModel):
    pass

class Chapeau(models.Model):
    numero_de_chapeau = models.IntegerField()

    def __str__(self):
        return self.numero_de_chapeau

class Equipe(NameModel):
    quel_pays = models.ForeignKey(Pays, on_delete=models.CASCADE)
    quel_championat = models.ForeignKey(Championnat, on_delete=models.CASCADE)
    quel_chapeau = models.ForeignKey(Chapeau, on_delete=models.CASCADE)
    logo = models.ImageField()
