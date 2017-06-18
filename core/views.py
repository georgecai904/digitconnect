from django.shortcuts import render
from products.models import Product


# Create your views here.
def index_page(request):
    products = Product.objects.all()
    return render(request, "core/index.html", {
        'mock_list': range(6),
        'url': request.path,
        'products': products
    })