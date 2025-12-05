from django.urls import path

from .views import OrderListView, create_order
urlpatterns = [
    path("order/list/", OrderListView.as_view()),
    path("order/create/", create_order)
]