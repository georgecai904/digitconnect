from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^purchase_orders/dashboard', views.purchase_orders_dashboard, name="purchase_order.dashboard"),
    url(r'^purchase_orders/details/(?P<purchase_order_id>[0-9]+)$', views.purchase_order_details,
        name="purchase_order.details"),
    url(r'^purchase_orders/on_road/(?P<purchase_order_id>[0-9]+)$', views.on_road_purchase_order,
        name="purchase_order.on_road"),
    url(r'^purchase_orders/new/(?P<product_id>[0-9]+)$', views.new_purchase_order, name="purchase_order.new"),
    url(r'^purchase_orders/new/confirm/(?P<product_id>[0-9]+)$', views.confirm_purchase_order,
        name="purchase_order.confirm.new"),

    url(r'^supply_offers/dashboard', views.supply_offers_dashboard, name="supply_offer.dashboard"),
    url(r'^supply_offers/new/(?P<purchase_order_id>[0-9]+)$', views.new_supply_offer, name="supply_offer.new"),
    url(r'^supply_offers/new/confirm/(?P<purchase_order_id>[0-9]+)$', views.confirm_new_supply_offer,
        name="supply_offer.confirm.new"),
    url(r'^supply_offers/details/(?P<supply_offer_id>[0-9]+)$', views.supply_offer_details,
        name="supply_offer.details"),
    url(r'^supply_offers/edit/confirm/(?P<supply_offer_id>[0-9]+)$', views.confirm_edit_supply_offer,
        name="supply_offer.confirm.edit"),
    url(r'^supply_offers/adopt/(?P<supply_offer_id>[0-9]+)$', views.adopt_supply_offer, name="supply_offer.adopt"),

    url(r'^join_purchases/new/(?P<purchase_order_id>[0-9]+)$', views.new_join_purchase, name="join_purchase.new"),
    url(r'^join_purchases/new/confirm/(?P<purchase_order_id>[0-9]+)$', views.confirm_new_join_purchase,
        name="join_purchase.confirm.new"),

    url(r'^production/details/(?P<production_id>[0-9]+)$', views.production_details, name="production.details"),
    url(r'^production/dashboard', views.production_dashboard, name="production.dashboard"),
    url(r'^production/records/new/(?P<production_id>[0-9]+)$', views.new_production_record,
        name="production.records.new"),
    url(r'^production/records/edit/(?P<record_id>[0-9]+)$', views.edit_production_record,
        name="production.records.edit"),
]
