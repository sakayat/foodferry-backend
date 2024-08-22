from django.shortcuts import render
from rest_framework.views import APIView
from .models import Restaurant, FoodCategory, FoodItem
from .serializers import (
    RestaurantSerializer,
    RestaurantFoodCategorySerializer,
    FoodCategorySerializer,
    FoodItemSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsRestaurantOwner
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class RestaurantAPI(APIView):

    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

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

        restaurant = Restaurant.objects.filter(owner=request.user)
        if restaurant:
            return Response("already exits", status=status.HTTP_302_FOUND)
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)


class UpdateRestaurantAPI(APIView):

    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

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


class FoodCategoryAPI(APIView):

    serializer_class = RestaurantFoodCategorySerializer
    permission_classes = [IsRestaurantOwner]

    def get(self, request):
        categories = FoodCategory.objects.all()
        serializer = FoodCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestaurantFoodCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodCategoriesAPI(APIView):
    def get(self, request):
        categories = FoodCategory.objects.all()
        serializer = FoodCategorySerializer(categories, many=True)
        return Response(serializer.data)


class FoodsAPI(APIView):
    
    def get(self, request):
        restaurant_query = request.query_params.get("restaurant")
        if restaurant_query:
            foods = FoodItem.objects.filter(restaurant_slug=restaurant_query)
        else:
            foods = FoodItem.objects.all()
        serializer = FoodItemSerializer(foods, many=True)
        return Response(serializer.data)


class FoodItemAPI(APIView):

    serializer_class = FoodItemSerializer
    permission_classes = [IsRestaurantOwner]

    def get(self, request):
        try:
            restaurant = FoodItem.objects.filter(restaurant=request.user.restaurant)
            serializer = FoodItemSerializer(restaurant, many=True)
            return Response(serializer.data)
        except AttributeError:
            return Response({"error": "User does not have a restaurant"})

    def post(self, request):
        serializer = FoodItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(restaurant=request.user.restaurant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodDetailsAPI(APIView):
    
    def get(self, request, slug):
        food = FoodItem.objects.get(name_slug=slug)
        serializer= FoodItemSerializer(food, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateFoodItemAPI(APIView):

    serializer_class = FoodItemSerializer

    def get(self, request, pk):
        try:
            food = FoodItem.objects.get(pk=pk)
            serializer = FoodItemSerializer(food, many=False)
            return Response(serializer.data)
        except FoodItem.DoesNotExist:
            return Response({"error": "item not found"})

    def put(self, request, pk):
        try:
            food = FoodItem.objects.get(pk=pk)
            serializer = FoodItemSerializer(food, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except FoodItem.DoesNotExist:
            return Response({"error": "item not found"})
        

class FoodCategoryItemAPI(APIView):
    
    def get(self, request):
        category_query = request.query_params.get("category")
        if category_query:
            category = FoodCategory.objects.get(slug=category_query)
            food_items = FoodItem.objects.filter(category=category)
        else:
            food_items = FoodItem.objects.all()
        serializer = FoodItemSerializer(food_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)