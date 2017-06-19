from django.shortcuts import render, redirect
from products.models import Product
from django.contrib.auth import authenticate, login
from core.forms import LoginInForm, NewUserForm
from django.contrib.auth.models import User


# Create your views here.
def index_page(request):
    products = Product.objects.all()
    return render(request, "core/index.html", {
        'mock_list': range(6),
        'url': request.path,
        'products': products
    })


def handle_login(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            if len(user.supplier_set.all()):
                return redirect("/")
            return redirect('/suppliers/new')
        else:
            return redirect('/auth/login')
    return render(request, 'auth/login.html', {'form': LoginInForm()})


def handle_signup(request):
    if request.method == "POST":
        user = User.objects.create(username=request.POST["username"], email=request.POST["email"])
        user.set_password(request.POST["password"])
        user.save()
        return redirect('/auth/login')
    return render(request, 'auth/signup.html', {'form': NewUserForm()})