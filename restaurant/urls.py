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
    RestaurantListAPI,
    DeleteRestaurantAPI,
    UpdateFoodCategoryAPI,
    DeleteFoodCategoryAPI,
    UpdateFoodTagAPI,
    DeleteFoodTagAPI,
    FoodTagListAPI,
    FoodFeedbackAPI,
    FeedbackListAPI,
    CategoryFoodListAPI,
    RestaurantInfoAPI,
    RestaurantFoodListView,
    TagFoodListView
)

router = DefaultRouter()


urlpatterns = [
    path("restaurant-info/", RestaurantOwnerInfoAPI.as_view(), name="restaurant-info"),
    path("create/", RestaurantAPI.as_view(), name="restaurant"),
    path("update/", UpdateRestaurantAPI.as_view(), name="update"),
    path("list/", RestaurantListAPI.as_view(), name="list"),
    path("delete/<int:id>/", DeleteRestaurantAPI.as_view(), name="delete"),
    path("food-category/", FoodCategoryAPI.as_view(), name="food-category"),
    path(
        "update-category/<int:id>/",
        UpdateFoodCategoryAPI.as_view(),
        name="update-category",
    ),
    path(
        "delete-category/<int:id>/",
        DeleteFoodCategoryAPI.as_view(),
        name="delete-category",
    ),
    path("food-categories/", FoodCategoriesAPI.as_view(), name="food-categories"),
    path("foods/", FoodsAPI.as_view(), name="foods"),
    path("add-food-item/", FoodItemAPI.as_view(), name="add-food-item"),
    path("update-food/<int:pk>/", UpdateFoodItemAPI.as_view(), name="update-food"),
    path("food-items/", FoodCategoryItemAPI.as_view(), name="food-items"),
    path("food-details/<slug:slug>/", FoodDetailsAPI.as_view(), name="food-details"),
    path("food-tags/", FoodTagsAPI.as_view(), name="food-tags"),
    path("update-tag/<int:id>/", UpdateFoodTagAPI.as_view(), name="update-tag"),
    path("delete-tag/<int:id>/", DeleteFoodTagAPI.as_view(), name="delete-tag"),
    path("tag-list/", FoodTagListAPI.as_view(), name="tag-list"),
    path("restaurant-foods/", RestaurantFoodsAPI.as_view({"get": "list"}), name="restaurant-foods"),
    path(
        "delete-food-item/<int:id>/", RemoveRestaurantFoodAPI.as_view(), name="delete"
    ),
    path('feedback/<slug:slug>/', FoodFeedbackAPI.as_view(), name='food-feedback'),
    path('feedback-list/<slug:slug>/', FeedbackListAPI.as_view(), name='feedback-list'),
    path('category-food-list/<slug:slug>/', CategoryFoodListAPI.as_view({'get': 'list'}), name='food-list'),
    path('info/<slug:slug>/', RestaurantInfoAPI.as_view(), name='info'),
    path("", include(router.urls)),
    path('restaurant-food-list/<slug:slug>/', RestaurantFoodListView.as_view({'get': 'list'}), name='food-list'),
    path('tag-food-list/<slug:slug>/', TagFoodListView.as_view({'get': 'list'}), name='food-list'),
]
