from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import CustomUserSerializer
from accounts.models import CustomUser


# Create your views here.


class UserListForRestaurantCreationAPI(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListAPI(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class UserUpdateAPI(APIView):

    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):

        user = CustomUser.objects.get(pk=pk)

        if request.user == user and user.role == "admin":
            return Response(
                {"error": "Admin cannot change their own permissions."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if "role" in request.data and request.data["role"] == "admin":
            user.is_staff = True
        elif "role" in request.data and request.data["role"] != "admin":
            user.is_staff = False
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
