from django.db import models
from clients.models import Purchaser
# Create your models here.


class Product(models.Model):
    purchaser = models.ForeignKey(Purchaser, default=None)
    name = models.CharField(max_length=20, default="", verbose_name="名称")
    image = models.CharField(max_length=20, default="", verbose_name="图片")
    category = models.CharField(max_length=20, default="", verbose_name="类型")
    location = models.CharField(max_length=20, default="", verbose_name="地区")
    amount = models.CharField(max_length=20, default="", verbose_name="采购数量")


