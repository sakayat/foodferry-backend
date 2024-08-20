from django.urls import path
from .views import AddToCartAPI, CartItemsAPI, UpdateCartItem

urlpatterns = [
    path("add-to-cart/<int:id>/", AddToCartAPI.as_view(), name="add-to-cart"),
    path("update-cart/<int:id>/", UpdateCartItem.as_view(), name="update-cart"),
    path("cart-items/", CartItemsAPI.as_view(), name="cart-items"),
]
