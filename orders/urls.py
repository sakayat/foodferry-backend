from django.urls import path
from .views import CreateOrderAPI, OrderListAPI

urlpatterns = [
    path("orders/", CreateOrderAPI.as_view(), name="orders"),
    path("order-list/", OrderListAPI.as_view(), name="order-list"),
]
