from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.handle_login),
    url(r'^signup$', views.handle_signup),
    url(r'^logout$', views.handle_logout),
    url(r'^account$', views.account_details),
    url(r'^reset/email$', views.reset_email),
    url(r'^reset/password$', views.reset_password),
    url(r'^center$', views.user_center),
]