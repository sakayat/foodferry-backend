from django.urls import path, include
from .views import UserRegistration, UserProfileAPI

urlpatterns = [
    path("register/", UserRegistration.as_view(), name="registration"),
    path("profile/", UserProfileAPI.as_view(), name="profile"),
]
