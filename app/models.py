from django.db import models

class Codes(models.Model):
    code = models.CharField(max_length=100)

class FormData(models.Model):
    type = models.CharField(max_length=50, blank=False, null=False)
    montant = models.FloatField(default=0)
    devise = models.CharField(max_length=50)
    code = models.ManyToManyField(Codes)
    mail = models.EmailField(blank=False, null=False)