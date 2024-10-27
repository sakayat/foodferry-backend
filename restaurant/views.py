from django.shortcuts import render
from rest_framework.views import APIView
from .models import Restaurant, FoodCategory, FoodItem, FoodTag, FoodFeedback
from .serializers import (
    RestaurantSerializer,
    RestaurantFoodCategorySerializer,
    FoodCategorySerializer,
    FoodItemSerializer,
    FoodTagSerializer,
    FoodFeedbackSerializer,
    RestaurantInfoSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsRestaurantOwner
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework import filters
from django.core.cache import cache
from orders.models import OrderDetails
from datetime import datetime
from collections import defaultdict

# Create your views here.


class RestaurantOwnerInfoAPI(APIView):

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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class DeleteRestaurantAPI(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, id):
        try:
            restaurant = Restaurant.objects.get(id=id)
        except Restaurant.DoesNotExist:
            return Response(
                {"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user.role == "admin":
            restaurant.delete()
            return Response({"message": "restaurant delete successfully"})


class RestaurantListAPI(APIView):

    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RestaurantFoodListView(viewsets.ModelViewSet):

    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return FoodItem.objects.filter(restaurant__slug=slug)


class RestaurantInfoAPI(APIView):

    def get(self, request, slug):
        info = Restaurant.objects.get(slug=slug)
        serializer = RestaurantInfoSerializer(info)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FoodCategoryAPI(APIView):

    serializer_class = RestaurantFoodCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        categories = FoodCategory.objects.all()
        serializer = FoodCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RestaurantFoodCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateFoodCategoryAPI(APIView):

    serializer_class = RestaurantFoodCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, id):
        try:
            category = FoodCategory.objects.get(id=id)
        except FoodCategory.DoesNotExist:
            return Response(
                {"error": "food category not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = FoodCategorySerializer(category)
        return Response(serializer.data)

    def put(sef, request, id):

        try:
            category = FoodCategory.objects.get(id=id)
        except FoodCategory.DoesNotExist:
            return Response(
                {"error": "FoodCategory not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = RestaurantFoodCategorySerializer(
            category, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteFoodCategoryAPI(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, id):
        try:
            category = FoodCategory.objects.get(id=id)
            category.delete()
            return Response({"item deleted successfully"}, status=status.HTTP_200_OK)
        except FoodItem.DoesNotExist:
            return Response(
                {"error": "item not found"}, status=status.HTTP_400_BAD_REQUEST
            )


class FoodCategoriesAPI(APIView):
    def get(self, request):
        cache_key = "food_categories"
        cache_data = cache.get(cache_key)
        if cache_data is not None:
            return Response(cache_data)
        categories = FoodCategory.objects.all()
        serializer = FoodCategorySerializer(categories, many=True)
        cache.set(cache_key, serializer.data, 60 * 60)
        return Response(serializer.data)


class FoodsAPI(APIView):
    def get(self, request):
        restaurant_query = request.query_params.get("restaurant")
        cache_key = f"foods_{restaurant_query}" if restaurant_query else "foods_all"
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
        if restaurant_query:
            foods = (
                FoodItem.objects.filter(restaurant_slug=restaurant_query)
                .select_related("category", "restaurant")
                .prefetch_related("tags")
            )
        else:
            foods = (
                FoodItem.objects.all()
                .select_related("category", "restaurant")
                .prefetch_related("tags")
            )
        serializer = FoodItemSerializer(foods, many=True)
        cache.set(cache_key, serializer.data, timeout=3600)
        return Response(serializer.data)


class TagFoodListView(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return FoodItem.objects.filter(tags__slug=slug)


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


class RestaurantFoodsAPI(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FoodItem.objects.filter(restaurant=self.request.user.restaurant)


class RemoveRestaurantFoodAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            item = FoodItem.objects.get(restaurant=request.user.restaurant, id=id)
            item.delete()
            return Response({"item deleted successfully"}, status=status.HTTP_200_OK)
        except FoodItem.DoesNotExist:
            return Response({"error": "item not found"})


class FoodDetailsAPI(APIView):
    def get(self, request, slug):
        food = FoodItem.objects.get(slug=slug)
        serializer = FoodItemSerializer(food, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateFoodItemAPI(APIView):
    serializer_class = FoodItemSerializer

    def get(self, request, pk):
        try:
            food = FoodItem.objects.get(restaurant=request.user.restaurant, pk=pk)
            serializer = FoodItemSerializer(food, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FoodItem.DoesNotExist:
            return Response(
                {"error": "item not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            food = FoodItem.objects.get(restaurant=request.user.restaurant, pk=pk)
            serializer = FoodItemSerializer(food, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(restaurant=request.user.restaurant)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except FoodItem.DoesNotExist:
            return Response(
                {"error": "item not found"}, status=status.HTTP_404_NOT_FOUND
            )


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


class FoodTagsAPI(APIView):
    serializer_class = FoodTagSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tags = FoodTag.objects.all()
        serializer = FoodTagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FoodTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryFoodListAPI(viewsets.ModelViewSet):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodItemSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return FoodItem.objects.filter(category__slug=slug)


class UpdateFoodTagAPI(APIView):
    serializer_class = FoodTagSerializer
    permission_classes = [IsAuthenticated]

    def get(self, id):
        try:
            tag = FoodTag.objects.get(id=id)
            serializer = FoodTagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FoodTag.DoesNotExist:
            return Response({"error": "tag not found"})

    def put(self, request, id):
        try:
            tag = FoodTag.objects.get(id=id)
        except FoodTag.DoesNotExist:
            return Response(
                {"error": "tag not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = FoodTagSerializer(tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteFoodTagAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, id):
        try:
            tag = FoodTag.objects.get(id=id)
            tag.delete()
            return Response({"tag deleted successfully"}, status=status.HTTP_200_OK)
        except FoodItem.DoesNotExist:
            return Response(
                {"error": "tag not found"}, status=status.HTTP_400_BAD_REQUEST
            )


class FoodTagListAPI(APIView):
    def get(self, request):
        tags = FoodTag.objects.all()
        serializer = FoodTagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FoodFeedbackAPI(APIView):
    serializer_class = FoodFeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        food_item = FoodItem.objects.get(slug=slug)
        feedbacks = FoodFeedback.objects.filter(food_item=food_item)
        serializer = FoodFeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, slug):
        try:
            food_item = FoodItem.objects.get(slug=slug)
        except FoodItem.DoesNotExist:
            return Response({"error": "item not found"})
        serializer = FoodFeedbackSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save(user=request.user, food_item=food_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackListAPI(APIView):
    def get(self, request, slug):
        food_item = FoodItem.objects.get(slug=slug)
        feedbacks = FoodFeedback.objects.filter(food_item=food_item)
        serializer = FoodFeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FoodSearchAPI(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "category__name"]


class RestaurantDataAPI(APIView):

    def get(self, request):

        restaurant = Restaurant.objects.get(owner=request.user)
        foods = FoodItem.objects.filter(restaurant=restaurant)
        total_products = foods.count()

        orders = OrderDetails.objects.filter(restaurant=restaurant.slug)
        total_orders = orders.count()
        pending_orders = orders.filter(status="pending").count()
        completed_orders = orders.filter(status="Completed").count()
        cancel_orders = orders.filter(status="Canceled").count()

        total_sales = 0
        month_names = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        monthly_sales = {month: 0 for month in month_names}

        for order in orders:
            if order.subtotal and order.status == "Completed":
                total_sales += order.item_price
                month_index = order.created_at.month - 1
                month_name = month_names[month_index]
                monthly_sales[month_name] += order.item_price

        response_data = {
            "total_products": total_products,
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "completed_orders": completed_orders,
            "total_sales": total_sales,
            "cancel_orders": cancel_orders,
            "monthly_sales": monthly_sales,
        }

        return Response(response_data, status=status.HTTP_200_OK)
