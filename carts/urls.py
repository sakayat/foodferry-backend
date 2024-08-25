from django.urls import path
from .views import AddToCartAPI, CartItemsAPI, UpdateCartItem, ClearCartItemsAPI

urlpatterns = [
    path("add-to-cart/<slug:slug>/", AddToCartAPI.as_view(), name="add-to-cart"),
    path("update/<int:id>/", UpdateCartItem.as_view(), name="update-cart"),
    path("list/", CartItemsAPI.as_view(), name="cart-items"),
    path("clear/", ClearCartItemsAPI.as_view(), name="clear-cart"),
]
