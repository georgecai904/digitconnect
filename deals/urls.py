from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^purchase_orders/dashboard', views.purchase_orders_dashboard),
    url(r'^purchase_orders/manage/(?P<purchase_order_id>[0-9]+)$', views.manage_purchase_order),
    url(r'^purchase_orders/new/(?P<product_id>[0-9]+)$', views.new_purchase_order),
    url(r'^purchase_orders/confirm/(?P<product_id>[0-9]+)$', views.confirm_purchase_order),

    url(r'^supply_offers/dashboard', views.supply_offers_dashboard),
    url(r'^supply_offers/new/(?P<purchase_order_id>[0-9]+)$', views.new_supply_offer),
    url(r'^supply_offers/confirm/(?P<purchase_order_id>[0-9]+)$', views.confirm_new_supply_offer),
    url(r'^supply_offers/details/(?P<supply_offer_id>[0-9]+)$', views.supply_offer_details),
    url(r'^supply_offers/edit/confirm/(?P<supply_offer_id>[0-9]+)$', views.confirm_edit_supply_offer),
    url(r'^supply_offers/adopt/(?P<supply_offer_id>[0-9]+)$', views.adopt_supply_offer),
    # url(r'^purchase_orders/edit', views.edit_purchase_order),
    # url(r'^purchase_orders/details', views.purchase_order_details),
]