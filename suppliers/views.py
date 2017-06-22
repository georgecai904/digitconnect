from django.shortcuts import render, HttpResponse, redirect
from suppliers.forms import NewSupplierForm
from django.contrib.auth.decorators import login_required
from directconnect.settings import LOGIN_URL
from suppliers.models import Supplier
# Create your views here.


@login_required(login_url=LOGIN_URL)
def new_supplier(request):
    if request.method == "POST":
        supplier = NewSupplierForm(request.POST).save(commit=False)
        supplier.user = request.user
        supplier.save()
        return redirect('/')
    if len(request.user.supplier_set.all()):
        return redirect('/')
    return render(request, 'suppliers/supplier_form.html', {'form': NewSupplierForm(), 'url': request.path,
                                                           'action_url': '/suppliers/new'})


@login_required(login_url=LOGIN_URL)
def edit_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    form = NewSupplierForm(instance=supplier)
    if request.method == "POST":
        NewSupplierForm(request.POST, instance=supplier).save()
        return redirect("/auth/details")
    return render(request, 'suppliers/supplier_form.html', {'form': form,
                                                            'action_url': '/suppliers/edit/{0}'.format(supplier_id)})
