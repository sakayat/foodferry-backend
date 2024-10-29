from django.urls import path
from .views import (
    CreateOrderAPI,
    OrderListAPI,
    UserOrderListAPI,
    UserOrderStatusAPI,
    PaymentAPI,
    PaymentSuccessAPI,
    PaymentFailedAPI
)

urlpatterns = [
    path("orders/", CreateOrderAPI.as_view(), name="orders"),
    path("order-list/", OrderListAPI.as_view(), name="order-list"),
    path("user-order-list/", UserOrderListAPI.as_view(), name="user-order"),
    path("order-status/<int:id>/", UserOrderStatusAPI.as_view(), name="order-status"),
    path("payment/<int:user_id>/", PaymentAPI.as_view(), name="payment"),
    path('payment-success/<int:user_id>/<str:tran_id>/', PaymentSuccessAPI.as_view(), name='payment_success'),
    path("payment-fail/", PaymentFailedAPI.as_view(), name="payment-fail"),
]
