from django.shortcuts import render, HttpResponse, redirect
from suppliers.forms import NewSupplierForm
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url="/auth/login")
def new_supplier(request):
    if request.method == "POST":
        supplier = NewSupplierForm(request.POST).save(commit=False)
        supplier.user = request.user
        supplier.save()
        return redirect('/')
    if len(request.user.supplier_set.all()):
        return redirect('/')

    return render(request, 'suppliers/new_supplier.html', {'form': NewSupplierForm(), 'url': request.path})
