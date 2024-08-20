from django.urls import path
from .views import AddToCartAPI

urlpatterns = [path("add-to-cart/<int:id>/", AddToCartAPI.as_view(), name="add-to-cart")]
