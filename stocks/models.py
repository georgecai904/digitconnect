from django.db import models
from clients.models import Purchaser, Supplier
# Create your models here.
from copy import deepcopy


class Product(models.Model):
    purchaser = models.ForeignKey(Purchaser, default=None)
    name = models.CharField(max_length=20, default="", verbose_name="名称")
    image = models.CharField(max_length=20, default="", verbose_name="图片")
    category = models.CharField(max_length=20, default="", verbose_name="类型")
    location = models.CharField(max_length=20, default="", verbose_name="地区")

    def __str__(self):
        return self.name

    def add_to_purchaser(self, purchaser):
        new_product = deepcopy(self)
        new_product.pk = None
        new_product.purchaser = purchaser
        new_product.save()