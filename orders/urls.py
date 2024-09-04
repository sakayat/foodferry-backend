from django.urls import path
from .views import CreateOrderAPI, OrderListAPI, UserOrderListAPI, UserOrderStatusAPI

urlpatterns = [
    path("orders/", CreateOrderAPI.as_view(), name="orders"),
    path("order-list/", OrderListAPI.as_view(), name="order-list"),
    path("user-order-list/", UserOrderListAPI.as_view(), name="user-order/"),
    path("order-status/<int:id>/", UserOrderStatusAPI.as_view(), name="order-status")
]
