from django.shortcuts import render
from rest_framework.views import APIView
from .models import Restaurant
from .serializers import RestaurantSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class RestaurantAPI(APIView):

    serializer_class = RestaurantSerializer

    def get(self, request):
        try:
            restaurant = Restaurant.objects.get(owner=request.user)
            serializer = RestaurantSerializer(restaurant)
            return Response(serializer.data)
        except Restaurant.DoesNotExist:
            return Response(
                {"error": "Restaurant not found"}, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        restaurant = Restaurant.objects.get(owner=request.user)
        if restaurant:
            return Response("already register")
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class UpdateRestaurantAPI(APIView):

    serializer_class = RestaurantSerializer

    def get(self, request):
        restaurant = Restaurant.objects.get(owner=request.user)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)

    def put(self, request):
        try:
            restaurant = Restaurant.objects.get(owner=request.user)
            serializer = RestaurantSerializer(
                restaurant, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Restaurant.DoesNotExist:
            return Response(
                {"error": "restaurant not found"}, status=status.HTTP_404_NOT_FOUND
            )
