from django.db import models
from clients.models import Purchaser, Supplier
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
    initiator = models.ForeignKey(Purchaser, null=False, blank=False, default=None, verbose_name="发起人")
    title = models.CharField(max_length=20, default="", verbose_name="标题", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    product = models.ForeignKey(Product, null=False, blank=False, default=None)
    status = models.CharField(max_length=10, default=POST_ORDER_STATUS[0], verbose_name="状态")

    offer_price = models.DecimalField(verbose_name="成交价格", max_digits=10, decimal_places=2, default=0)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, default=None, verbose_name="制定供应商")

    def add_purchaser(self, purchaser, amount):
        PurchaseOrderLine.objects.get_or_create(
            purchase_order=self,
            purchaser=purchaser,
            amount=amount
        )
        if len(self.purchaseorderline_set.all()) > 1:
            # self.status = POST_ORDER_STATUS[2]
            for supply_offer in self.supplyoffer_set.all():
                supply_offer.is_updated = False
                supply_offer.save()

    def add_supplier(self, supplier, price):
        a = SupplyOffer.objects.get_or_create(
            purchase_order=self,
            supplier=supplier,
            price=price,
            offer_amount=self.total_amount
         )

    def get_amount_by_purchaser(self, purchaser):
        return int(self.purchaseorderline_set.get(purchaser=purchaser).amount)

    def supplier_update_price(self, supplier, price):
        supply_offer = self.supplyoffer_set.get(id=supplier.id)
        supply_offer.price = price
        supply_offer.is_updated = True
        supply_offer.offer_amount = self.total_amount
        supply_offer.save()
        # if set([p.is_updated for p in self.purchaseofferline_set.all()]) == {True}:
            # self.status = POST_ORDER_STATUS[3]

    def make_deal(self):
        # TODO: 先暂时默认价格最低的为最后的交易价格
        self.status = POST_ORDER_STATUS[1]
        supply_offer = SupplyOffer.objects.all().order_by('price')[0]
        self.offer_price = supply_offer.price
        self.supplier = supply_offer.supplier
        self.save()

    def get_all_purchasers(self):
        return [i.purhcaser for i in self.purchaseorderline_set.all()]

    @property
    def total_amount(self):
        return sum(int(i.amount) for i in self.purchaseorderline_set.all())

    @property
    def offer_amount(self):
        return len(self.supplyoffer_set.all())

    @property
    def amount(self):
        # TODO: 到时候需要修改成除了发起人以外找到对应的数目
        return self.purchaseorderline_set.get(purchaser=self.initiator).amount


class PurchaseOrderLine(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, null=False, blank=False, default=None)
    purchaser = models.ForeignKey(Purchaser, null=False, blank=False, default=None)
    amount = models.CharField(max_length=20, default="", verbose_name="数量")

    # TODO：当出现拼购后，拼购用户的产品库内会自动添加他拼购过的商品，并且是独立与原产品发布者


class SupplyOffer(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, null=False, blank=False, default=None)
    supplier = models.ForeignKey(Supplier, null=False, blank=False, default=None)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="报价")
    offer_amount = models.CharField(max_length=10, default=0)
    is_updated = models.BooleanField(default=True)
    is_noticed = models.BooleanField(default=False)
