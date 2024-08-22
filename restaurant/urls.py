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
    FoodCategoryItemAPI,
    FoodDetailsAPI
)

router = DefaultRouter()

urlpatterns = [
    path("create/", RestaurantAPI.as_view(), name="restaurant"),
    path("update/", UpdateRestaurantAPI.as_view(), name="update"),
    path("add-category/", FoodCategoryAPI.as_view(), name="food-category"),
    path("food-categories/", FoodCategoriesAPI.as_view(), name="food-categories"),
    path("foods/", FoodsAPI.as_view(), name="foods"),
    path("add-food-item/", FoodItemAPI.as_view(), name="add-food-item"),
    path("update-food/<int:pk>/", UpdateFoodItemAPI.as_view(), name="update-food"),
    path("food-items/", FoodCategoryItemAPI.as_view(), name="food-items"),
    path("food-details/<slug:slug>/", FoodDetailsAPI.as_view(), name="food-details"),
]
