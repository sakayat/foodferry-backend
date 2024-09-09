from django.urls import path, include
from .views import UserListAPI, UserUpdateAPI, UserListForRestaurantCreationAPI

urlpatterns = [
    path("users/", UserListAPI.as_view({"get": "list"}), name="users"),
    path("update-user/<int:pk>/role/", UserUpdateAPI.as_view(), name="update-user"),
    path("user-list/", UserListForRestaurantCreationAPI.as_view(), name="user-list"),
]
