from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^select', views.select_type, name="clients.select"),

    url(r'^purchasers/new', views.new_purchaser, name="purchasers.new"),
    url(r'^purchasers/edit/(?P<purchaser_id>[0-9]+)$', views.edit_purchaser, name="purchasers.edit"),

    url(r'^suppliers/new', views.new_supplier, name="suppliers.new"),
    url(r'^suppliers/edit/(?P<supplier_id>[0-9]+)$', views.edit_supplier, name="suppliers.edit"),
    url(r'^suppliers/details/(?P<supplier_id>[0-9]+)$', views.supplier_details, name="suppliers.details"),

    url(r'^manufacturers/new/(?P<purchase_order_id>[0-9]+)$', views.new_manufacturer, name="manufacturers.new"),
]
