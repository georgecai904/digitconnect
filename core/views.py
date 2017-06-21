from django.shortcuts import render, redirect
from products.models import Product
from django.contrib.auth import authenticate, login, logout
from core.forms import LoginInForm, NewUserForm
from django.contrib.auth.models import User
from urllib import parse

# Create your views here.
def index_page(request):
    products = Product.objects.all()
    return render(request, "core/index.html", {
        'mock_list': range(6),
        'url': request.path,
        'products': products
    })


def handle_login(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        query = parse.parse_qs(parse.urlparse(request.get_full_path()).query)
        if user is not None:
            login(request, user)
            return redirect(query.get('next', ['/']).pop())
        else:
            return redirect(request.path)
    return render(request, 'auth/login.html', {'form': LoginInForm(), 'action_url': request.get_full_path()})


def handle_signup(request):
    if request.method == "POST":
        user = User.objects.create(username=request.POST["username"], email=request.POST["email"])
        user.set_password(request.POST["password"])
        user.save()
        return redirect('/auth/login?next=/suppliers/new')
    return render(request, 'auth/signup.html', {'form': NewUserForm()})


def handle_logout(request):
    if request.user:
        logout(request)
    return redirect("/")