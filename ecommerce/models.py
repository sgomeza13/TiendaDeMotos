from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    price = models.IntegerField()
    stock = models.IntegerField()
    
class CustomerUser(AbstractUser):
    username = None
    email = models.EmailField( unique=True)
    city = models.CharField(max_length=20)  
    address = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'address',
        'city'
    ]

    def __str__(self):
        return self.email