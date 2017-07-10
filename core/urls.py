from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.handle_login, name="auth.login"),
    url(r'^signup$', views.handle_signup, name="auth.signup"),
    url(r'^logout$', views.handle_logout, name="auth.logout"),
    url(r'^account$', views.account_details, name="auth.account"),
    url(r'^reset/email$', views.reset_email, name="auth.reset.email"),
    url(r'^reset/password$', views.reset_password, name="auth.reset.password"),
    url(r'^center$', views.user_center, name="auth.center"),
]