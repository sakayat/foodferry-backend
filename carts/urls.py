from django.urls import path
from .views import AddToCartAPI, CartItemsAPI

urlpatterns = [
    path("add-to-cart/<int:id>/", AddToCartAPI.as_view(), name="add-to-cart"),
    path("cart-items/", CartItemsAPI.as_view(), name="cart-items"),
]
