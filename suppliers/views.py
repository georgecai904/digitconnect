from django.shortcuts import render, HttpResponse, redirect
from suppliers.forms import NewSupplierForm

# Create your views here.


def new_supplier(request):
    if request.method == "POST":
        supplier = NewSupplierForm(request.POST).save(commit=False)
        supplier.user = request.user
        supplier.save()
        return redirect('/')
    return render(request, 'suppliers/new_supplier.html', {'form': NewSupplierForm(), 'url': request.path})
