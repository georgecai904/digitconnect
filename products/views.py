from django.shortcuts import render, redirect
from products.forms import NewProductForm
from django.contrib.auth.decorators import login_required
from directconnect.settings import LOGIN_URL
# Create your views here.
from products.models import Product, PurchaseOrder, SupplyOffer


@login_required(login_url=LOGIN_URL)
def new_product(request):
    if request.method == "POST":
        p = NewProductForm(request.POST).save(commit=False)
        purchaser = request.user.purchaser_set.first()
        p.purchaser = purchaser
        p.save()
        return redirect('/products/list')
    return render(request, 'products/product_form.html', {
        'form': NewProductForm(),
        'url': '/products/new',
        'action_url': '/products/new',
        'header': "登记产品信息"
    })


@login_required(login_url=LOGIN_URL)
def edit_product(request, product_id):
    old_p = Product.objects.get(id=product_id)
    form = NewProductForm(instance=old_p)
    if request.method == "POST":
        NewProductForm(request.POST, instance=old_p).save()
        # p.supplier = old_p.supplier
        # p.save()
        return redirect('/products/list')
    return render(request, 'products/product_form.html', {
        'form': form,
        'action_url': '/products/edit/'+product_id,
        'header': '修改产品信息'
    })


def delete_product(request, product_id):
    p = Product.objects.get(id=product_id)
    p.delete()
    return redirect("/products/list")


@login_required(login_url=LOGIN_URL)
def product_list(request):
    if len(request.user.purchaser_set.all()) == 0:
        return redirect('/purchasers/new')
    purchaser = request.user.purchaser_set.first()
    products = Product.objects.filter(purchaser=purchaser)
    return render(request, "products/product_list.html", {
        'products': products,
        'header': '产品列表'
    })


def manage_purchase_order(request, purchase_order_id):
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    supply_offers = purchase_order.supplyoffer_set.all()
    join_purchases = purchase_order.purchaseorderline_set.exclude(purchaser=purchase_order.initiator)
    if request.GET:
        for id in request.GET['id']:
            supply_offer = SupplyOffer.objects.get(id=id)
            supply_offer.is_noticed = True
            supply_offer.save()
    return render(request, "purchase_orders/manage.html", {
        'header': "{}采购单细节".format(purchase_order.product.name),
        'breadcrumb': [{"href": '/auth/my-posts', "name": "我的发布"}],
        'purchase_order': purchase_order,
        'supply_offers': supply_offers,
        'join_purchases': join_purchases,
    })

