
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from deals.forms import PurchaseOrderForm, SupplyOfferForm, JoinPurchaseForm, ProductionRecordForm
from deals.models import PurchaseOrder, SupplyOffer, Production, ProductionRecord
from directconnect.settings import POST_ORDER_STATUS, LOGIN_URL
from stocks.models import Product


def purchase_order_details(request, purchase_order_id):
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    supply_offers = purchase_order.supplyoffer_set.all()
    join_purchases = purchase_order.purchaseorderline_set.exclude(purchaser=purchase_order.initiator)
    if request.GET:
        for id in request.GET['id']:
            supply_offer = SupplyOffer.objects.get(id=id)
            supply_offer.is_noticed = True
            supply_offer.save()
    return render(request, "purchase_orders/details.html", {
        'header': "{}采购单细节".format(purchase_order.product.name),
        'breadcrumb': [{"href": '/deals/purchase_orders/dashboard', "name": "我的发布"}],
        'purchase_order': purchase_order,
        'supply_offers': supply_offers,
        'join_purchases': join_purchases,
    })


def on_road_purchase_order(request, purchase_order_id):
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    pol = purchase_order.purchaseorderline_set.get(purchaser=request.user.purchaser_set.first())
    return render(request, "purchase_orders/on_road.html", {
        "header": "待收货订单详情",
        "purchase_order_line": pol,
        "production": purchase_order.production_set.first(),
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
            'purchase_order_lines_oc': purchaser.purchaseorderline_set.filter(purchase_order__status=POST_ORDER_STATUS[0]),
            'purchase_order_lines_or': purchaser.purchaseorderline_set.filter(purchase_order__status=POST_ORDER_STATUS[1]),
            'purchase_order_lines_cp': purchaser.purchaseorderline_set.filter(purchase_order__status=POST_ORDER_STATUS[2]),
        })
    else:
        return redirect(reverse('purchasers.new'))


def new_purchase_order(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        purchaser = request.user.purchaser_set.all()[0]
        purchase_order = PurchaseOrder.objects.create(initiator=purchaser, product=product)
        purchase_order.add_purchaser(purchaser=purchaser, amount=request.POST['amount'])
        purchase_order.save()
        return redirect(reverse('purchase_orders.dashboard'))

    return render(request, "purchase_orders/form.html", {
        "header": "发布采购订单",
        "product": product,
        "form": PurchaseOrderForm(),
        "action_url": reverse('purchase_orders.confirm.new', args=(product_id,))
    })


def confirm_purchase_order(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        return render(request, "purchase_orders/form.html", {
            "header": "确认采购订单",
            "product": product,
            "amount": request.POST["amount"],
            "action_url": reverse('purchase_orders.new', args=(product_id,))
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
        return redirect(reverse('supply_offers.dashboard'))

    return render(request, "supply_offers/form.html", {
        "header": "报价页面",
        "purchase_order": purchase_order,
        "form": SupplyOfferForm(),
        "action_url": reverse('supply_offers.confirm.new', args=(purchase_order_id,))
    })


def confirm_new_supply_offer(request, purchase_order_id):
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    if request.method == "POST":
        return render(request, "supply_offers/form.html", {
            "header": "确认报价",
            "purchase_order": purchase_order,
            "price": request.POST["price"],
            "action_url": reverse('supply_offers.new', args=(purchase_order_id,))
        })


def supply_offer_details(request, supply_offer_id):
    supply_offer = SupplyOffer.objects.get(id=supply_offer_id)

    if request.method == "POST":
        supply_offer.price = request.POST['price']
        supply_offer.offer_amount = supply_offer.purchase_order.total_amount
        supply_offer.save()
        return redirect(reverse('supply_offers.dashboard'))

    return render(request, "supply_offers/details.html", {
        "header": "报价详情",
        "purchase_order": supply_offer.purchase_order,
        "supply_offer": supply_offer,
        "form": SupplyOfferForm(instance=supply_offer),
        "action_url": reverse('supply_offers.confirm.edit', args=(supply_offer_id, ))
    })


def confirm_edit_supply_offer(request, supply_offer_id):
    supply_offer = SupplyOffer.objects.get(id=supply_offer_id)
    if request.method == "POST":
        return render(request, "supply_offers/details.html", {
            "header": "确认报价修改",
            "purchase_order": supply_offer.purchase_order,
            "supply_offer": supply_offer,
            "price": request.POST["price"],
            "action_url": reverse('supply_offers.details', args=(supply_offer_id,)),
            "btn_content": "确认修改"
        })


def adopt_supply_offer(request, supply_offer_id):
    supply_offer = SupplyOffer.objects.get(id=supply_offer_id)

    if request.method == "POST":
        supply_offer.purchase_order.status = POST_ORDER_STATUS[2]
        supply_offer.save()
        supplier = supply_offer.supplier
        if supplier.manufacturer_set.count() == 0:
            return redirect(reverse('manufacturers.new', args=(supply_offer.purchase_order.id,)))
        production = Production.objects.create(
            purchase_order=supply_offer.purchase_order,
            manufacturer=supplier.manufacturer_set.first()
        )
        return redirect(reverse('production.details', args=(production.id,)))

    return render(request, "supply_offers/details.html", {
        "header": "确认生产",
        "purchase_order": supply_offer.purchase_order,
        "supply_offer": supply_offer,
        "price": supply_offer.price,
        "action_url": request.path,
        "btn_content": "确认生产",
    })


@login_required(login_url=LOGIN_URL)
def new_join_purchase(request, purchase_order_id):
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)

    if request.method == "POST":
        purchaser = request.user.purchaser_set.all()[0]
        purchase_order.add_purchaser(purchaser=purchaser, amount=request.POST["amount"])
        return redirect(reverse('purchase_orders.dashboard'))

    return render(request, "join_purchases/new.html", {
        "header": "拼购采购",
        "form": JoinPurchaseForm(),
        "purchase_order": purchase_order,
        "action_url": reverse('join_purchases.confirm.new', args=(purchase_order_id,))
    })


def confirm_new_join_purchase(request, purchase_order_id):
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    if request.method == "POST":
        return render(request, "join_purchases/new.html", {
            "header": "确认拼购",
            "purchase_order": purchase_order,
            "amount": request.POST["amount"],
            "action_url": reverse('join_purchases.new', args=(purchase_order_id,))
        })


def production_details(request, production_id):
    production = Production.objects.get(id=production_id)
    return render(request, "production/details.html", {
        "header": "生产信息",
        "production": production,
    })


def production_dashboard(request):
    manufacturer = request.user.manufacturer_set.first()
    if not manufacturer:
        manufacturer = request.user.supplier_set.first().manufacturer_set.first()
    productions = Production.objects.filter(manufacturer=manufacturer)
    return render(request, "production/dashboard.html", {
        "header": "生产管理",
        "productions": productions
    })


def new_production_record(request, production_id):
    production = Production.objects.get(id=production_id)
    if request.method == "POST":
        pr = ProductionRecordForm(request.POST).save(commit=False)
        pr.production = production
        pr.save()
        return redirect(reverse('production.details', args=(production_id,)))
    return render(request, "production/records/form.html", {
        "header": "登记生产记录",
        "action_url": request.path,
        "form": ProductionRecordForm()
    })


def edit_production_record(request, record_id):
    pr = ProductionRecord.objects.get(id=record_id)
    if request.method == "POST":
        pr = ProductionRecordForm(request.POST, instance=pr).save()
        return redirect(reverse('production.details', args=(pr.production.id,)))
    return render(request, "production/records/form.html", {
        "header": "修改生产记录",
        "action_url": request.path,
        "form": ProductionRecordForm(instance=pr)
    })
