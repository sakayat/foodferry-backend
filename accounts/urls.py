from django.urls import path, include
from .views import UserRegistrationAPI, UserLoginAPI, UserLogoutAPI, UserProfileAPI, ResetPasswordAPI, activate

urlpatterns = [
    path("register/", UserRegistrationAPI.as_view(), name="registration"),
    path("login/", UserLoginAPI.as_view(), name="login"),
    path("logout/", UserLogoutAPI.as_view(), name="logout"),
    path("profile/", UserProfileAPI.as_view(), name="profile"),
    path("reset-password/", ResetPasswordAPI.as_view(), name="reset-password"),
    path("active/<uid64>/<token>/", activate, name="active"),
]

