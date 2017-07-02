from django.shortcuts import render, redirect
from products.models import Product, PurchaseOrder
from django.contrib.auth import authenticate, login, logout
from core.forms import LoginInForm, NewUserForm, ChangeEmailForm, ChangePasswordForm
from django.contrib.auth.models import User
from urllib import parse
from django.contrib.auth.decorators import login_required
from directconnect.settings import LOGIN_URL, POST_ORDER_STATUS


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
    return render(request, 'auth/login.html', {
        'form': LoginInForm(),
        'action_url': request.get_full_path(),
        'header': "登陆页面"
    })


def handle_signup(request):
    if request.method == "POST":
        user = User.objects.create(username=request.POST["username"], email=request.POST["email"])
        user.set_password(request.POST["password"])
        user.save()
        return redirect('/auth/login?next=/clients/select')
    return render(request, 'auth/signup.html', {
        'form': NewUserForm(),
        'header': "注册页面"
    })


def handle_logout(request):
    if request.user:
        logout(request)
    return redirect("/")


@login_required(login_url=LOGIN_URL)
def personal_info(request):
    user = request.user
    purchasers = user.purchaser_set.all()
    suppliers = user.supplier_set.all()
    return render(request, 'user/personal_info.html', {
        'user': user,
        'purchasers': purchasers,
        'suppliers': suppliers
    })


@login_required(login_url=LOGIN_URL)
def my_posts(request):
    user = request.user

    if user.purchaser_set.all():
        purchaser = user.purchaser_set.all()[0]
        if request.GET:
            p_o = PurchaseOrder.objects.get(id=int(request.GET['order_id']))
            p_o.make_deal()
        return render(request, 'user/my_posts.html', {
            'header': '我的订单',
            'purchase_orders_oc': purchaser.purchaseorder_set.filter(status=POST_ORDER_STATUS[0]),
            'purchase_orders_or': purchaser.purchaseorder_set.filter(status=POST_ORDER_STATUS[1]),
            'purchase_orders_cp': purchaser.purchaseorder_set.filter(status=POST_ORDER_STATUS[2]),
        })
    else:
        return redirect("/purchasers/new")


@login_required(login_url=LOGIN_URL)
def user_center(request):
    return render(request, 'user/center.html', {
        'header': "我的中心",
    })


@login_required(login_url=LOGIN_URL)
def user_change_email(request):
    u = User.objects.get(username=request.user.username)
    form = ChangeEmailForm(instance=u)
    if request.method == "POST":
        u.email = request.POST['email']
        u.save()
        return redirect("/auth/personal-info")
    return render(request, 'auth/change_email.html', {'form': form, 'action_url': '/auth/details/email'})


@login_required(login_url=LOGIN_URL)
def user_change_password(request):
    u = User.objects.get(username=request.user.username)
    form = ChangePasswordForm()
    if request.method == "POST":
        if authenticate(request, username=u.username, password=request.POST['old_password']):
            if request.POST['password'] == request.POST['repeated_password']:
                u.set_password(request.POST['password'])
                u.save()
                return redirect("/auth/personal-info")
        return redirect("/auth/details/password")
    return render(request, 'auth/change_email.html', {'form': form, 'action_url': '/auth/details/password'})