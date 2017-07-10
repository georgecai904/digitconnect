from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^products/new$', views.new_product, name='products.new'),
    url(r'^products/edit/(?P<product_id>[0-9]+)$', views.edit_product, name='products.edit'),
    url(r'^products/delete/(?P<product_id>[0-9]+)$', views.delete_product, name='products.delete'),
    url(r'^products/dashboard', views.products_dashboard, name='products.dashboard'),
]