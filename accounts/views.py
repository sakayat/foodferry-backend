from django.shortcuts import render
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from accounts.models import CustomUser
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import redirect

# Create your views here.
class UserRegistrationAPI(APIView):

    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"{settings.BASE_API_URL}/api/accounts/active/{uid}/{token}/"
            email_subject = "Confirm Your Email"
            email_body = render_to_string(
                "confirm_mail.html", {"confirm_link": confirm_link}
            )
            email = EmailMultiAlternatives(email_subject, "", to={user.email})
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({"message": "check your mail for active account"}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except CustomUser.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(f"{settings.VITE_BASE_URL}/sign-in/")


class UserLoginAPI(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response(
                    {"token": token.key, "user_id": user.id}, status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid credentials"}, status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserLogoutAPI(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"message": "Successfully logged out."}, status=status.HTTP_200_OK
        )


class UserProfileAPI(APIView):

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPI(APIView):

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "No user with this email"}, status=status.HTTP_404_NOT_FOUND
            )

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"{settings.VITE_BASE_URL}/reset-password/{uid}/{token}/"

        subject = "Reset Your Password"
        
        email_body = render_to_string(
            "reset_email.html", {"reset_link": reset_link, "user": user.username}
        )
        email = EmailMultiAlternatives(subject, "", to={user.email})
        email.attach_alternative(email_body, "text/html")
        email.send()
        
        return Response({"message": "Password reset link sent successfully"}, status=status.HTTP_200_OK)

