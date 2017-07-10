from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^purchase_orders/dashboard', views.purchase_orders_dashboard, name="purchase_orders.dashboard"),
    url(r'^purchase_orders/details/(?P<purchase_order_id>[0-9]+)$', views.purchase_order_details,
        name="purchase_orders.details"),
    url(r'^purchase_orders/on_road/(?P<purchase_order_id>[0-9]+)$', views.on_road_purchase_order,
        name="purchase_orders.on_road"),
    url(r'^purchase_orders/new/(?P<product_id>[0-9]+)$', views.new_purchase_order, name="purchase_orders.new"),
    url(r'^purchase_orders/new/confirm/(?P<product_id>[0-9]+)$', views.confirm_purchase_order,
        name="purchase_orders.confirm.new"),

    url(r'^supply_offers/dashboard', views.supply_offers_dashboard, name="supply_offers.dashboard"),
    url(r'^supply_offers/new/(?P<purchase_order_id>[0-9]+)$', views.new_supply_offer, name="supply_offers.new"),
    url(r'^supply_offers/new/confirm/(?P<purchase_order_id>[0-9]+)$', views.confirm_new_supply_offer,
        name="supply_offers.confirm.new"),
    url(r'^supply_offers/details/(?P<supply_offer_id>[0-9]+)$', views.supply_offer_details,
        name="supply_offers.details"),
    url(r'^supply_offers/edit/confirm/(?P<supply_offer_id>[0-9]+)$', views.confirm_edit_supply_offer,
        name="supply_offers.confirm.edit"),
    url(r'^supply_offers/adopt/(?P<supply_offer_id>[0-9]+)$', views.adopt_supply_offer, name="supply_offers.adopt"),

    url(r'^join_purchases/new/(?P<purchase_order_id>[0-9]+)$', views.new_join_purchase, name="join_purchases.new"),
    url(r'^join_purchases/new/confirm/(?P<purchase_order_id>[0-9]+)$', views.confirm_new_join_purchase,
        name="join_purchases.confirm.new"),

    url(r'^production/details/(?P<production_id>[0-9]+)$', views.production_details, name="production.details"),
    url(r'^production/dashboard', views.production_dashboard, name="production.dashboard"),
    url(r'^production/records/new/(?P<production_id>[0-9]+)$', views.new_production_record,
        name="production.records.new"),
    url(r'^production/records/edit/(?P<record_id>[0-9]+)$', views.edit_production_record,
        name="production.records.edit"),
]
