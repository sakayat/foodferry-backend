from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RestaurantAPI, UpdateRestaurantAPI

router = DefaultRouter()

urlpatterns = [
    path("restaurant/", RestaurantAPI.as_view(), name="restaurant"),
    path("update-restaurant/", UpdateRestaurantAPI.as_view(), name="update")
    
]
