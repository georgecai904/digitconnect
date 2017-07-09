from django.shortcuts import render, redirect
from clients.forms import NewPurchaserForm, NewSupplierForm, ManufacturerForm
from django.contrib.auth.decorators import login_required

from deals.models import Production, PurchaseOrder
from directconnect.settings import LOGIN_URL
from clients.models import Purchaser, Supplier, Manufacturer
from django.contrib.auth.models import User
# Create your views here.


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
                                                              'action_url': '/clients/purchasers/new'})


@login_required(login_url=LOGIN_URL)
def edit_purchaser(request, purchaser_id):
    purchaser = Purchaser.objects.get(id=purchaser_id)
    form = NewPurchaserForm(instance=purchaser)
    if request.method == "POST":
        NewPurchaserForm(request.POST, instance=purchaser).save()
        return redirect("/auth/account")
    return render(request, 'purchasers/purchaser_form.html', {'form': form,
                                                              'action_url': '/clients/purchasers/edit/{0}'.format(
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
                                                            'action_url': '/clients/suppliers/new',
                                                            'header': '登记供应商信息',
                                                            })


@login_required(login_url=LOGIN_URL)
def edit_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    form = NewSupplierForm(instance=supplier)
    if request.method == "POST":
        NewSupplierForm(request.POST, instance=supplier).save()
        return redirect("/auth/account")
    return render(request, 'suppliers/supplier_form.html', {'form': form,
                                                            'action_url': '/clients/suppliers/edit/{0}'.format(
                                                                supplier_id),
                                                            'header': '修改供应商信息',
                                                            })


def supplier_details(request, supplier_id):
    return render(request, 'suppliers/details.html', {
        'header': '供应商信息',
        'supplier': Supplier.objects.get(id=supplier_id)
    })


def new_manufacturer(request, purchase_order_id):
    if request.method == "POST":
        supplier = request.user.supplier_set.first()
        user = User.objects.create(username=request.POST["username"])
        user.set_password(request.POST["password"])
        user.save()
        manufacturer = Manufacturer.objects.create(
            name=request.POST['name'],
            address=request.POST['address'],
            user=user,
            supplier=supplier
        )
        production = Production.objects.create(
            purchase_order=PurchaseOrder.objects.get(id=purchase_order_id),
            manufacturer=manufacturer
        )
        return redirect("/deals/production/details/{}".format(production.id))

    return render(request, "manufacturers/form.html", {
        "header": "登记工厂信息",
        "action_url": "/clients/manufacturers/new/{}".format(purchase_order_id),
        "form": ManufacturerForm()
    })