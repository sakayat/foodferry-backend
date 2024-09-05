from django.urls import path, include
from .views import UserListAPI, UserUpdateAPI

urlpatterns = [
    path("users/", UserListAPI.as_view({"get": "list"}), name="users"),
    path("update-user/<int:pk>/role/", UserUpdateAPI.as_view(), name="update-user")
]
