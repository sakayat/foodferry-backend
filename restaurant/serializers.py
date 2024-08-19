from rest_framework import serializers
from .models import Restaurant, FoodCategory, FoodItem


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = "__all__"
        read_only_fields = ["id", "owner", "is_approved"]


class RestaurantFoodCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodCategory
        fields = "__all__"
        read_only_fields = ["restaurant"]


class FoodCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodCategory
        fields = ["name"]


class FoodItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    restaurant_name = serializers.CharField(
        source="restaurant.name", read_only=True
    )

    class Meta:
        model = FoodItem
        fields = [
            "id",
            "name",
            "description",
            "price",
            "is_available",
            "image",
            "category",
            "category_name",
            "restaurant_name",
        ]
