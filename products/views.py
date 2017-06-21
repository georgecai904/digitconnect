from django.shortcuts import render, redirect
from products.forms import NewProductForm
from django.contrib.auth.decorators import login_required
from directconnect.settings import LOGIN_URL
# Create your views here.
from products.models import Product


@login_required(login_url=LOGIN_URL)
def new_product(request):
    if request.method == "POST":
        p = NewProductForm(request.POST).save(commit=False)
        supplier = request.user.supplier_set.first()
        p.supplier = supplier
        p.save()
        return redirect('/products/list')
    return render(request, 'products/product_form.html', {'form': NewProductForm(), 'url': '/products/new', 'action_url': '/products/new'})


@login_required(login_url=LOGIN_URL)
def edit_product(request, product_id):
    old_p = Product.objects.get(id=product_id)
    form = NewProductForm(instance=old_p)
    if request.method == "POST":
        NewProductForm(request.POST, instance=old_p).save()
        # p.supplier = old_p.supplier
        # p.save()
        return redirect('/products/list')
    return render(request, 'products/product_form.html', {'form': form, 'action_url': '/products/edit/'+product_id})


def delete_product(request, product_id):
    p = Product.objects.get(id=product_id)
    p.delete()
    return redirect("/products/list")


@login_required(login_url=LOGIN_URL)
def product_list(request):
    supplier = request.user.supplier_set.first()
    products = Product.objects.filter(supplier=supplier)
    return render(request, "products/product_list.html", {'products': products})