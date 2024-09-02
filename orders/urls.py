from django.urls import path
from .views import CreateOrderAPI, OrderListAPI, UserOrderAPI

urlpatterns = [
    path("orders/", CreateOrderAPI.as_view(), name="orders"),
    path("order-list/", OrderListAPI.as_view(), name="order-list"),
    path("user-order/<slug:slug>/", UserOrderAPI.as_view(), name="user-order/"),
]
