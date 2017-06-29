from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# from products.models import Product


class Purchaser(models.Model):
    user = models.ForeignKey(User, default=None)
    name = models.CharField(max_length=20, default='')
    phone = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=100, default='')
    location = models.CharField(max_length=20, default='')
    license = models.CharField(max_length=20, default='')
    area = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name


class Supplier(models.Model):
    user = models.ForeignKey(User, default=None)
    name = models.CharField(max_length=20, default='')
    phone = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=100, default='')
    location = models.CharField(max_length=20, default='')
    license = models.CharField(max_length=20, default='')
    area = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name


class PostPrice(models.Model):
    product = models.ForeignKey("products.Product", default=None)
    supplier = models.ForeignKey(Supplier, default=None)
    price = models.CharField(max_length=20, default="")
    amount = models.CharField(max_length=20, default="")

