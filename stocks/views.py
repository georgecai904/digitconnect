from django.shortcuts import render, redirect
from django.urls import reverse

from core.views import get_breadcrumb
from stocks.forms import ProductForm
from django.contrib.auth.decorators import login_required
from directconnect.settings import LOGIN_URL
# Create your views here.
from stocks.models import Product


@login_required(login_url=LOGIN_URL)
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


@login_required(login_url=LOGIN_URL)
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


def delete_product(request, product_id):
    p = Product.objects.get(id=product_id)
    p.delete()
    return redirect(reverse('products.dashboard'))


@login_required(login_url=LOGIN_URL)
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




