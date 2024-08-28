from django.urls import path, include
from .views import UserListAPI, UserUpdateAPI

urlpatterns = [
    path("users/", UserListAPI.as_view(), name="users"),
    path("user-update/<int:pk>/", UserUpdateAPI.as_view(), name="update-user")
]
