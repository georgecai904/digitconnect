from django.db import models
from django.contrib.auth.models import User
# Create your models here.


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