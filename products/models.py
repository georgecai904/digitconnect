from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=20, default="")
    image = models.CharField(max_length=20, default="")
    category = models.CharField(max_length=20, default="")
    location = models.CharField(max_length=20, default="")
    amount = models.CharField(max_length=20, default="")