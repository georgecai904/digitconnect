
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from deals.forms import NewPurchaseOrderForm, NewSupplyOfferForm
from deals.models import PurchaseOrder, SupplyOffer, PurchaseOrderLine
from directconnect.settings import POST_ORDER_STATUS, LOGIN_URL
from stocks.models import Product


def manage_purchase_order(request, purchase_order_id):
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    supply_offers = purchase_order.supplyoffer_set.all()
    join_purchases = purchase_order.purchaseorderline_set.exclude(purchaser=purchase_order.initiator)
    if request.GET:
        for id in request.GET['id']:
            supply_offer = SupplyOffer.objects.get(id=id)
            supply_offer.is_noticed = True
            supply_offer.save()
    return render(request, "purchase_orders/manage.html", {
        'header': "{}采购单细节".format(purchase_order.product.name),
        'breadcrumb': [{"href": '/deals/purchase_orders/dashboard', "name": "我的发布"}],
        'purchase_order': purchase_order,
        'supply_offers': supply_offers,
        'join_purchases': join_purchases,
    })


def purchase_orders_dashboard(request):
    user = request.user

    if user.purchaser_set.all():
        purchaser = user.purchaser_set.all()[0]
        if request.GET:
            p_o = PurchaseOrder.objects.get(id=int(request.GET['order_id']))
            p_o.make_deal()
        return render(request, 'purchase_orders/dashboard.html', {
            'header': '我的订单',
            'purchase_orders_oc': purchaser.purchaseorder_set.filter(status=POST_ORDER_STATUS[0]),
            'purchase_orders_or': purchaser.purchaseorder_set.filter(status=POST_ORDER_STATUS[1]),
            'purchase_orders_cp': purchaser.purchaseorder_set.filter(status=POST_ORDER_STATUS[2]),
        })
    else:
        return redirect("/clients/purchasers/new")


def new_purchase_order(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        purchaser = request.user.purchaser_set.all()[0]
        purchase_order = PurchaseOrder.objects.create(initiator=purchaser, product=product)
        purchase_order.add_purchaser(purchaser=purchaser, amount=request.POST['amount'])
        purchase_order.save()
        return redirect("/deals/purchase_orders/dashboard")

    return render(request, "purchase_orders/new.html", {
        "header": "发布采购订单",
        "product": product,
        "form": NewPurchaseOrderForm(),
        "action_url": "/deals/purchase_orders/confirm/{}".format(product.id)
    })


def confirm_purchase_order(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        return render(request, "purchase_orders/new.html", {
            "header": "确认采购订单",
            "product": product,
            "amount": request.POST["amount"],
            "action_url": "/deals/purchase_orders/new/{}".format(product.id)
        })


def supply_offers_dashboard(request):
    supplier = request.user.supplier_set.all()[0]
    return render(request, "supply_offers/dashboard.html", {
        "header": "我的报价",
        "adopted_supply_offers": SupplyOffer.objects.filter(purchase_order__status=POST_ORDER_STATUS[1]).filter(supplier=supplier),
        "ongoing_supply_offers": SupplyOffer.objects.filter(purchase_order__status=POST_ORDER_STATUS[0]).filter(supplier=supplier)
    })


@login_required(login_url=LOGIN_URL)
def new_supply_offer(request, purchase_order_id):
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)

    if request.method == "POST":
        supplier = request.user.supplier_set.all()[0]
        purchase_order.add_supplier(supplier=supplier, price=request.POST["price"])
        return redirect("/deals/supply_offers/dashboard")

    return render(request, "supply_offers/new.html", {
        "header": "报价页面",
        "purchase_order": purchase_order,
        "form": NewSupplyOfferForm(),
        "action_url": "/deals/supply_offers/confirm/{}".format(purchase_order_id)
    })


def confirm_new_supply_offer(request, purchase_order_id):
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    if request.method == "POST":
        return render(request, "supply_offers/new.html", {
            "header": "确认报价",
            "purchase_order": purchase_order,
            "price": request.POST["price"],
            "action_url": "/deals/supply_offers/new/{}".format(purchase_order_id)
        })


def supply_offer_details(request, supply_offer_id):
    supply_offer = SupplyOffer.objects.get(id=supply_offer_id)

    if request.method == "POST":
        supply_offer.price = request.POST['price']
        supply_offer.offer_amount = supply_offer.purchase_order.total_amount
        supply_offer.save()
        return redirect("/deals/supply_offers/dashboard")

    return render(request, "supply_offers/details.html", {
        "header": "报价详情",
        "purchase_order": supply_offer.purchase_order,
        "supply_offer": supply_offer,
        "form": NewSupplyOfferForm(instance=supply_offer),
        "action_url": "/deals/supply_offers/edit/confirm/{}".format(supply_offer.id)
    })


def confirm_edit_supply_offer(request, supply_offer_id):
    supply_offer = SupplyOffer.objects.get(id=supply_offer_id)
    if request.method == "POST":
        return render(request, "supply_offers/details.html", {
            "header": "确认报价修改",
            "purchase_order": supply_offer.purchase_order,
            "supply_offer": supply_offer,
            "price": request.POST["price"],
            "action_url": "/deals/supply_offers/details/{}".format(supply_offer.id),
            "btn_content": "确认修改"
        })


def adopt_supply_offer(request, supply_offer_id):
    supply_offer = SupplyOffer.objects.get(id=supply_offer_id)

    if request.method == "POST":
        supply_offer.purchase_order.status = POST_ORDER_STATUS[2]
        supply_offer.save()
        return redirect("/deals/production_orders/dashboard")

    return render(request, "supply_offers/details.html", {
        "header": "确认生产",
        "purchase_order": supply_offer.purchase_order,
        "supply_offer": supply_offer,
        "price": supply_offer.price,
        "action_url": "/deals/supply_offers/adopt/{}".format(supply_offer.id),
        "btn_content": "确认生产",
    })