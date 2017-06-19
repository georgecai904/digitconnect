from django.shortcuts import render, redirect
from products.forms import NewProductForm
# Create your views here.


def new_product(request):
    if request.method == "POST":
        NewProductForm(request.POST).save()
        return redirect('/')
    return render(request, 'products/new_product.html', {'form': NewProductForm(), 'url': '/products/new'})