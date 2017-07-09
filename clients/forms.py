
from clients.models import Purchaser, Supplier, Manufacturer
from django import forms
from directconnect.forms import BasicForm


class NewPurchaserForm(BasicForm):
    class Meta:
        model = Purchaser
        # fields = '__all__'
        exclude = ('user',)


class NewSupplierForm(BasicForm):
    class Meta:
        model = Supplier
        # fields = '__all__'
        exclude = ('user',)


class ManufacturerForm(BasicForm):
    username = forms.CharField(label="登陆账号")
    password = forms.CharField(widget=forms.PasswordInput, label="登陆密码")

    class Meta:
        model = Manufacturer
        exclude = ('user', 'supplier', )

#
# class PostPriceForm(BasicForm):
#     class Meta:
#         model = PostPrice
#         exclude = ('product', 'supplier', )