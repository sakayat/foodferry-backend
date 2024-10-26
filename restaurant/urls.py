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
    TagFoodListView,
    FoodSearchAPI,
    RestaurantDataAPI
)

router = DefaultRouter()


urlpatterns = [
    # restaurant urls
    path("info/", RestaurantOwnerInfoAPI.as_view(), name="restaurant-info"),
    path("create/", RestaurantAPI.as_view(), name="restaurant-create"),
    path("update/", UpdateRestaurantAPI.as_view(), name="restaurant-update"),
    path("delete/<int:id>/", DeleteRestaurantAPI.as_view(), name="restaurant-delete"),
    path("list/", RestaurantListAPI.as_view(), name="restaurant-list"),
    # food category urls
    path("categories/", FoodCategoriesAPI.as_view(), name="food-categories"),
    path("category/", FoodCategoryAPI.as_view(), name="food-category"),
    path(
        "category/update/<int:id>/",
        UpdateFoodCategoryAPI.as_view(),
        name="food-category-update",
    ),
    path(
        "category/delete/<int:id>/",
        DeleteFoodCategoryAPI.as_view(),
        name="food-category-delete",
    ),
    
    # food item urls
    path("category/items/", FoodCategoryItemAPI.as_view(), name="food-category-items"),
    path("details/<slug:slug>/", FoodDetailsAPI.as_view(), name="food-details"),
    
    # food tags urls
    path("tags/", FoodTagsAPI.as_view(), name="food-tags"),
    path("tag/update/<int:id>/", UpdateFoodTagAPI.as_view(), name="food-tag-update"),
    path("tag/delete/<int:id>/", DeleteFoodTagAPI.as_view(), name="food-tag-delete"),
    path("tag-list/", FoodTagListAPI.as_view(), name="tag-list"),
    
    # restaurant foods urls
    path("items/", FoodsAPI.as_view(), name="food-items"),
    path("item/add", FoodItemAPI.as_view(), name="food-item-add"),
    path("item/update/<int:pk>/", UpdateFoodItemAPI.as_view(), name="food-item-update"),
    path(
        "foods/",
        RestaurantFoodsAPI.as_view({"get": "list"}),
        name="restaurant-foods",
    ),
    path("food/delete/<int:id>/", RemoveRestaurantFoodAPI.as_view(), name="delete"),
    
    # feedback urls
    path("feedback/<slug:slug>/", FoodFeedbackAPI.as_view(), name="food-feedback"),
    path("feedback-list/<slug:slug>/", FeedbackListAPI.as_view(), name="feedback-list"),
    
    # category food list urls
    path(
        "category-foods/<slug:slug>/",
        CategoryFoodListAPI.as_view({"get": "list"}),
        name="food-list",
    ),
    
    # restaurant urls
    path("info/<slug:slug>/", RestaurantInfoAPI.as_view(), name="restaurant-info"),
    path(
        "restaurant-food-list/<slug:slug>/",
        RestaurantFoodListView.as_view({"get": "list"}),
        name="food-list",
    ),
    path(
        "tag-food-list/<slug:slug>/",
        TagFoodListView.as_view({"get": "list"}),
        name="food-list",
    ),
    
    # search url
    path("search-food/", FoodSearchAPI.as_view({"get": "list"}), name="search-foods"),
    path('data/', RestaurantDataAPI.as_view(), name='restaurant-data'),
    path("", include(router.urls)),
]
