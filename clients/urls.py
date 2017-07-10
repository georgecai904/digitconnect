from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^select', views.select_type, name="client.select"),

    url(r'^purchasers/new', views.new_purchaser, name="purchaser.new"),
    url(r'^purchasers/edit/(?P<purchaser_id>[0-9]+)$', views.edit_purchaser, name="purchaser.edit"),

    url(r'^suppliers/new', views.new_supplier, name="supplier.new"),
    url(r'^suppliers/edit/(?P<supplier_id>[0-9]+)$', views.edit_supplier, name="supplier.edit"),
    url(r'^suppliers/details/(?P<supplier_id>[0-9]+)$', views.supplier_details, name="supplier.details"),

    url(r'^manufacturers/new/(?P<purchase_order_id>[0-9]+)$', views.new_manufacturer, name="manufacturer.new"),
]
