from django.db import models

# Create your models here.


class Supplier(models.Model):
    name = models.TextField(default='')
    phone = models.TextField(default='')
    address = models.TextField(default='')
    location = models.TextField(default='')
    license = models.TextField(default='')
    area = models.TextField(default='')