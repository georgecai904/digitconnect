from django.shortcuts import render, redirect
from django.urls import reverse

from core.views import get_breadcrumb
from directconnect.decorators import PurchaserRequired
from stocks.forms import ProductForm
# Create your views here.
from stocks.models import Product


@PurchaserRequired
def new_product(request):
    if request.method == "POST":
        p = ProductForm(request.POST).save(commit=False)
        purchaser = request.user.purchaser_set.first()
        p.purchaser = purchaser
        p.save()
        return redirect(reverse('products.dashboard'))
    return render(request, 'stocks/products/form.html', {
        'form': ProductForm(),
        'url': '/stocks/products/new',
        'action_url': request.path,
        'header': "登记产品信息",
        'breadcrumb': get_breadcrumb(request)
    })


@PurchaserRequired
def edit_product(request, product_id):
    old_p = Product.objects.get(id=product_id)
    form = ProductForm(instance=old_p)
    if request.method == "POST":
        ProductForm(request.POST, instance=old_p).save()
        return redirect(reverse('products.dashboard'))
    return render(request, 'stocks/products/form.html', {
        'form': form,
        'action_url': request.path,
        'header': '修改产品信息',
        'breadcrumb': get_breadcrumb(request)
    })


@PurchaserRequired
def delete_product(request, product_id):
    p = Product.objects.get(id=product_id)
    p.delete()
    return redirect(reverse('products.dashboard'))


@PurchaserRequired
def products_dashboard(request):
    if len(request.user.purchaser_set.all()) == 0:
        return redirect(reverse('purchasers.new'))
    purchaser = request.user.purchaser_set.first()
    products = purchaser.product_set.all()
    return render(request, "stocks/products/dashboard.html", {
        'products': products,
        'header': '产品列表',
        'breadcrumb': get_breadcrumb(request)
    })




