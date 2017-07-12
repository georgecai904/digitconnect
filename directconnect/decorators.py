from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from directconnect.settings import LOGIN_URL


class DecoratorBase:
    def __init__(self, func):
        self.func = func

    # def __call__(self, request, *args, **kwargs):


class UserRequired(DecoratorBase):
    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect("{}?next={}".format(reverse("auth.login"), request.get_full_path()))
        else:
            return self.func(request, *args, **kwargs)


class SupplierRequired(DecoratorBase):
    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect("{}?next={}".format(reverse("auth.login"), request.get_full_path()))
        elif request.user.supplier_set.count():
            return self.func(request, *args, **kwargs)
        else:
            return redirect(reverse("suppliers.new"))


class PurchaserRequired(DecoratorBase):
    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect("{}?next={}".format(reverse("auth.login"), request.get_full_path()))
        elif request.user.purchaser_set.count():
            return self.func(request, *args, **kwargs)
        else:
            return redirect(reverse("purchasers.new"))


class SalesRequired(DecoratorBase):
    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect("{}?next={}".format(reverse("auth.login"), request.get_full_path()))
        elif request.user.purchaser_set.count() or request.user.supplier_set.count():
            return self.func(request, *args, **kwargs)
        else:
            return redirect(reverse("clients.select"))


class ManufacturerRequired(DecoratorBase):
    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect("{}?next={}".format(reverse("auth.login"), request.get_full_path()))
        elif request.user.manufacturer.count():
            return self.func(request, *args, **kwargs)
        else:
            return redirect(reverse("manufacturers.new"))