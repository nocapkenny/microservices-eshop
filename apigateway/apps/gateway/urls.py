from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^user/.*', views.proxy_view, name='users-proxy'),
    re_path(r'^products/.*', views.proxy_view, name='products-proxy'),
    re_path(r'^categories/.*', views.proxy_view, name='categories-proxy'),
    re_path(r'^cart/.*', views.proxy_view, name='cart-proxy'),
    re_path(r'^order/.*', views.proxy_view, name='orders-proxy'),
]