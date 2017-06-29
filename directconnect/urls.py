"""digitconnect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import core.views
import clients.views
import products.views

urlpatterns = [
    url(r'^$', core.views.index_page),
    url(r'^admin/', admin.site.urls),

    url(r'^clients/select$', clients.views.select_type),
    url(r'^purchasers/new$', clients.views.new_purchaser),
    url(r'^purchasers/edit/(?P<purchaser_id>[0-9]+)$', clients.views.edit_purchaser),
    url(r'^suppliers/new$', clients.views.new_supplier),
    url(r'^suppliers/edit/(?P<supplier_id>[0-9]+)$', clients.views.edit_supplier),
    url(r'^suppliers/post-price/(?P<product_id>[0-9]+)', clients.views.post_price),
    # url(r'^purchasers/delete/(?P<product_id>[0-9]+)$', purchasers.views.delete_product),

    url(r'^products/new$', products.views.new_product),
    url(r'^products/edit/(?P<product_id>[0-9]+)$', products.views.edit_product),
    url(r'^products/delete/(?P<product_id>[0-9]+)$', products.views.delete_product),
    url(r'^products/list$', products.views.product_list),

    url(r'^auth/login$', core.views.handle_login),
    url(r'^auth/signup$', core.views.handle_signup),
    url(r'^auth/logout$', core.views.handle_logout),
    url(r'^auth/details$', core.views.user_details),
    url(r'^auth/details/email', core.views.user_change_email),
    url(r'^auth/details/password', core.views.user_change_password),
]
