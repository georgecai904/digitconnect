import csv, os, sys

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "directconnect.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


def create_user():
    from django.contrib.auth.models import User
    u, created = User.objects.update_or_create(username="georgecai904", email="test@test.com")
    u.set_password("testpassword")
    u.save()
    return u


def create_purchaser():
    u = create_user()
    from purchasers.models import Purchaser
    p, created = Purchaser.objects.update_or_create(
        user=u,
        name="山姆采购商",
        phone="13868892809",
        address="上海市浦东新区罗山路1502号10号楼502室",
        location="江浙沪",
        license="G92719234",
        area="IT行业"
    )
    return p


def create_product():
    purchaser = create_purchaser()
    from products.models import Product
    p, created = Product.objects.update_or_create(
        purchaser=purchaser,
        name='B&O音响',
        image='/images/product.jpg',
        category='高档音响',
        amount='100',
        location='江浙沪',
    )

    return p


def create_post_price():
    p = create_product()
    from products.models import PostPrice
    pp, created = PostPrice.objects.update_or_create(
        product=p,
        name="华少供应",
        phone="12839991231",
        email="supplier@supplier.com",
        price="1000",

    )

create_post_price()