from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class familyName(models.Model):
    familyName = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.familyName}"

class commonName(models.Model):
    commonName = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.commonName}"
    
class qrImage(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="qr/")
    
class plantImage(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="plant/")
    
class plant(models.Model):
    name = models.CharField(max_length=100)
    scientificName = models.CharField(max_length=100)
    familyNameList = models.ManyToManyField("familyName", related_name="famName", blank=True)
    commonNameList = models.ManyToManyField("commonName", related_name="comName", blank=True)
    uses = models.TextField(null=True, blank=True)
    characteristic = models.TextField(null=True, blank=True)
    distribution = models.TextField(null=True, blank=True)
    habitat = models.TextField(null=True, blank=True)
    care = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    references = models.URLField()
    qrImageList = models.ManyToManyField("qrImage", related_name="qrImg", blank=True)
    plantImageList = models.ManyToManyField("plantImage", related_name="plantImg", blank=True)

    def __str__(self):
        return f"{self.name}"