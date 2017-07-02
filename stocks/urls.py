from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^products/new$', views.new_product),
    url(r'^products/edit/(?P<product_id>[0-9]+)$', views.edit_product),
    url(r'^products/delete/(?P<product_id>[0-9]+)$', views.delete_product),
    url(r'^products/dashboard', views.products_dashboard),
]