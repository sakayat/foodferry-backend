from django.shortcuts import render
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from rest_framework import status


# Create your views here.
class UserRegistration(APIView):

    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            return Response(
                {
                    "message": "",
                    "token": token,
                    "uid": uid,
                },
                status.HTTP_200_OK,
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
