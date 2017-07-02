from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^select', views.select_type),

    # url(r'^purchasers/dashboard', views.purchasers_dashboard),
    url(r'^purchasers/new', views.new_purchaser),
    url(r'^purchasers/edit/(?P<purchaser_id>[0-9]+)$', views.edit_purchaser),
    # url(r'^purchasers/details', views.purchaser_details),

    # url(r'^suppliers/dashboard', views.suppliers_dashboard),
    url(r'^suppliers/new', views.new_supplier),
    url(r'^suppliers/edit/(?P<supplier_id>[0-9]+)$', views.edit_supplier),
    url(r'^suppliers/details/(?P<supplier_id>[0-9]+)$', views.supplier_details),
]
