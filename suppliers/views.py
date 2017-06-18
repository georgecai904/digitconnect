from django.shortcuts import render, HttpResponse, redirect
from suppliers.forms import NewSupplierForm

# Create your views here.


def new_supplier(request):
    if request.method == "POST":
        NewSupplierForm(request.POST).save()
        return redirect('/')
    return render(request, 'suppliers/new_supplier.html', {'form': NewSupplierForm(), 'url': request.path})


def hello(s):
    print(s)


def now(s):
    print(s)