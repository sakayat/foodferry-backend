from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    RestaurantAPI,
    UpdateRestaurantAPI,
    FoodCategoryAPI,
    FoodCategoriesAPI,
    FoodsAPI,
    FoodItemAPI,
    UpdateFoodItemAPI,
)

router = DefaultRouter()

urlpatterns = [
    path("restaurant/", RestaurantAPI.as_view(), name="restaurant"),
    path("update-restaurant/", UpdateRestaurantAPI.as_view(), name="update"),
    path("restaurant-food-category/", FoodCategoryAPI.as_view(), name="food-category"),
    path("food-categories/", FoodCategoriesAPI.as_view(), name="food-categories"),
    path("foods/", FoodsAPI.as_view(), name="foods"),
    path("create-food/", FoodItemAPI.as_view(), name="create-food"),
    path("update-food/<int:pk>/", UpdateFoodItemAPI.as_view(), name="update-food"),
]
