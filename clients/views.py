from django.shortcuts import render, HttpResponse, redirect
from clients.forms import NewPurchaserForm, PostPriceForm, NewSupplierForm
from django.contrib.auth.decorators import login_required
from directconnect.settings import LOGIN_URL
from clients.models import Purchaser, Supplier
# Create your views here.
from products.models import Product


@login_required(login_url=LOGIN_URL)
def select_type(request):
    return render(request, 'clients/select_type.html', {
        'header': '入驻身份选择'
    })


@login_required(login_url=LOGIN_URL)
def new_purchaser(request):
    if request.method == "POST":
        purchaser = NewPurchaserForm(request.POST).save(commit=False)
        purchaser.user = request.user
        purchaser.save()
        return redirect('/')
    if len(request.user.purchaser_set.all()):
        return redirect('/')
    return render(request, 'purchasers/purchaser_form.html', {'form': NewPurchaserForm(),
                                                              'url': request.path,
                                                              'header': '登记采购商信息',
                                                              'action_url': '/purchasers/new'})


@login_required(login_url=LOGIN_URL)
def edit_purchaser(request, purchaser_id):
    purchaser = Purchaser.objects.get(id=purchaser_id)
    form = NewPurchaserForm(instance=purchaser)
    if request.method == "POST":
        NewPurchaserForm(request.POST, instance=purchaser).save()
        return redirect("/auth/details")
    return render(request, 'purchasers/purchaser_form.html', {'form': form,
                                                              'action_url': '/purchasers/edit/{0}'.format(
                                                                  purchaser_id),
                                                              'header': '修改采购商信息',
                                                              })


@login_required(login_url=LOGIN_URL)
def new_supplier(request):
    if request.method == "POST":
        supplier = NewSupplierForm(request.POST).save(commit=False)
        supplier.user = request.user
        supplier.save()
        return redirect('/')
    if len(request.user.supplier_set.all()):
        return redirect('/')
    return render(request, 'suppliers/supplier_form.html', {'form': NewSupplierForm(),
                                                            'url': request.path,
                                                            'action_url': '/suppliers/new',
                                                            'header': '登记供应商信息',
                                                            })


@login_required(login_url=LOGIN_URL)
def edit_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    form = NewSupplierForm(instance=supplier)
    if request.method == "POST":
        NewSupplierForm(request.POST, instance=supplier).save()
        return redirect("/auth/details")
    return render(request, 'suppliers/supplier_form.html', {'form': form,
                                                            'action_url': '/suppliers/edit/{0}'.format(
                                                                supplier_id),
                                                            'header': '修改供应商信息',
                                                            })


@login_required(login_url=LOGIN_URL)
def post_price(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.supplier_set.count() == 0:
        return redirect("/suppliers/new")
    if request.method == "POST":
        pp = PostPriceForm(request.POST).save(commit=False)
        pp.product = product
        pp.supplier = request.user.supplier_set.all()[0]
        pp.save()
        return render(request, "suppliers/post_price_success.html", {
            "success_msg": "您的报价已提交，若采购商感兴趣，会进一步与您联系",
            "pp": pp,
            'header': "报价成功"
        })
    return render(request, "suppliers/post_price.html", {
        "product": product,
        "action_url": "/suppliers/post-price/{}".format(product_id),
        "form": PostPriceForm(),
        'header': "报价登记"
    })
