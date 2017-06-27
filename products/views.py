from django.shortcuts import render, redirect
from products.forms import NewProductForm, PostPriceForm
from django.contrib.auth.decorators import login_required
from directconnect.settings import LOGIN_URL
# Create your views here.
from products.models import Product


@login_required(login_url=LOGIN_URL)
def new_product(request):
    if request.method == "POST":
        p = NewProductForm(request.POST).save(commit=False)
        purchaser = request.user.purchaser_set.first()
        p.purchaser = purchaser
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
    purchaser = request.user.purchaser_set.first()
    products = Product.objects.filter(purchaser=purchaser)
    return render(request, "products/product_list.html", {'products': products})


def post_price(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        pp = PostPriceForm(request.POST).save(commit=False)
        pp.product = product
        pp.save()
        return render(request, "products/post_price_success.html", {
            "success_msg": "您的报价已提交，若采购商感兴趣，会进一步与您联系",
            "pp": pp
        })
    return render(request, "products/post_price.html", {
        "product": product,
        "action_url": "/products/{}/post-price".format(product_id),
        "form": PostPriceForm(),
    })