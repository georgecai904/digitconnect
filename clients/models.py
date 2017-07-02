from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Purchaser(models.Model):
    user = models.ForeignKey(User, default=None)
    name = models.CharField(max_length=20, default='', verbose_name="名称")
    phone = models.CharField(max_length=20, default='', verbose_name="电话")
    address = models.CharField(max_length=100, default='', verbose_name="地址")
    location = models.CharField(max_length=20, default='', verbose_name="区域")
    license = models.CharField(max_length=20, default='', verbose_name="营业执照")
    area = models.CharField(max_length=20, default='', verbose_name="领域")

    def __str__(self):
        return self.name


class Supplier(models.Model):
    user = models.ForeignKey(User, default=None)
    name = models.CharField(max_length=20, default='', verbose_name="名称")
    phone = models.CharField(max_length=20, default='', verbose_name="电话")
    address = models.CharField(max_length=100, default='', verbose_name="地址")
    location = models.CharField(max_length=20, default='', verbose_name="区域")
    license = models.CharField(max_length=20, default='', verbose_name="营业执照")
    area = models.CharField(max_length=20, default='', verbose_name="领域")

    def __str__(self):
        return self.name

