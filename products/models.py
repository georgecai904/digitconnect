from django.db import models
from suppliers.models import Supplier
# Create your models here.


class Product(models.Model):
    supplier = models.ForeignKey(Supplier, default=None)
    name = models.CharField(max_length=20, default="")
    image = models.CharField(max_length=20, default="")
    category = models.CharField(max_length=20, default="")
    location = models.CharField(max_length=20, default="")
    amount = models.CharField(max_length=20, default="")