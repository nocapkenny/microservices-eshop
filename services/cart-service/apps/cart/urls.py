from django.urls import path

from . import views

urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart-view"),
    path("cart/add/", views.CartAddItemView.as_view(), name="cart-add"),
    path("cart/update/<int:pk>/", views.CartItemUpdateView.as_view(), name="cart-update"),
    path("cart/delete/<int:pk>/", views.CartItemDestroyView.as_view(), name="cart-delete"),
    path("cart/clear/", views.CartClearAPIView.as_view(), name="cart-clear"),
]
