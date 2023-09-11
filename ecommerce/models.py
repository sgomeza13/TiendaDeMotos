from django.db import models
from account.models import CustomerUser
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=300)
    reference = models.CharField(max_length=50)
    price = models.IntegerField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)


class Rating(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)