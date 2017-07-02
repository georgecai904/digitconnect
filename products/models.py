from django.db import models
from clients.models import Purchaser
from directconnect.settings import POST_ORDER_STATUS
# Create your models here.


class Product(models.Model):
    purchaser = models.ForeignKey(Purchaser, default=None)
    name = models.CharField(max_length=20, default="", verbose_name="名称")
    image = models.CharField(max_length=20, default="", verbose_name="图片")
    category = models.CharField(max_length=20, default="", verbose_name="类型")
    location = models.CharField(max_length=20, default="", verbose_name="地区")

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    title = models.CharField(max_length=20, default="", verbose_name="标题", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    product = models.ForeignKey(Product, null=False, blank=False, default=None)
    status = models.CharField(max_length=10, default=POST_ORDER_STATUS[0], verbose_name="状态")

    def __init__(self, *args, **kwargs):
        super(PurchaseOrder, self).__init__(*args, **kwargs)
        self.title = "{}采购单".format(self.product.name)

    def add_purchaser(self, purchaser, amount):
        PurchaseOrderLine.objects.get_or_create(
            purchase_order=self,
            purchaser=purchaser,
            amount=amount
        )


class PurchaseOrderLine(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, null=False, blank=False, default=None)
    purchaser = models.ForeignKey(Purchaser, null=False, blank=False, default=None)
    amount = models.CharField(max_length=20, default="", verbose_name="地区")

    # TODO：当出现拼购后，拼购用户的产品库内会自动添加他拼购过的商品，并且是独立与原产品发布者
