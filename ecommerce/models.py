from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    reference = models.CharField(max_length=50)
    price = models.IntegerField()
    stock = models.IntegerField()


