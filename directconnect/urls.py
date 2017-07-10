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
from django.conf.urls import url, include
from django.contrib import admin
import core.views

urlpatterns = [

    # Home Page
    url(r'^$', core.views.index_page, name="homepage"),

    # [Module] admin
    url(r'^admin/', admin.site.urls),

    # [Module] core
    url(r'^auth/', include("core.urls")),

    # [Module] deals
    url(r'deals/', include("deals.urls")),

    # [Module] stocks
    url(r'stocks/', include("stocks.urls")),

    # [Module] clients
    url(r'clients/', include("clients.urls")),

    # url(r'^purchase_order/manage/(?P<purchase_order_id>[0-9]+)$', deals.views.manage_purchase_order),
]
