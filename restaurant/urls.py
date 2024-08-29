from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    RestaurantOwnerInfoAPI,
    RestaurantAPI,
    UpdateRestaurantAPI,
    FoodCategoryAPI,
    FoodCategoriesAPI,
    FoodsAPI,
    FoodItemAPI,
    UpdateFoodItemAPI,
    FoodCategoryItemAPI,
    FoodDetailsAPI,
    FoodTagsAPI,
    RestaurantFoodsAPI,
    RemoveRestaurantFoodAPI,
    RestaurantListAPI
)

router = DefaultRouter()

urlpatterns = [
    path("restaurant-info/", RestaurantOwnerInfoAPI.as_view(), name="restaurant-info"),
    path("create/", RestaurantAPI.as_view(), name="restaurant"),
    path("update/", UpdateRestaurantAPI.as_view(), name="update"),
    path("list/", RestaurantListAPI.as_view(), name="list"),
    path("add-category/", FoodCategoryAPI.as_view(), name="food-category"),
    path("food-categories/", FoodCategoriesAPI.as_view(), name="food-categories"),
    path("foods/", FoodsAPI.as_view(), name="foods"),
    path("add-food-item/", FoodItemAPI.as_view(), name="add-food-item"),
    path("update-food/<int:pk>/", UpdateFoodItemAPI.as_view(), name="update-food"),
    path("food-items/", FoodCategoryItemAPI.as_view(), name="food-items"),
    path("food-details/<slug:slug>/", FoodDetailsAPI.as_view(), name="food-details"),
    path("food-tags/", FoodTagsAPI.as_view(), name="food-tags"),
    path("restaurant-foods/", RestaurantFoodsAPI.as_view(), name="restaurant-foods"),
    path("delete-food-item/<int:id>/", RemoveRestaurantFoodAPI.as_view(), name="delete"),
]
