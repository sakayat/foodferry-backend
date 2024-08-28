from rest_framework import serializers
from .models import Restaurant, FoodCategory, FoodItem, FoodTag


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = "__all__"
        read_only_fields = ["id", "owner", "is_approved"]


class RestaurantFoodCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodCategory
        fields = "__all__"


class FoodCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodCategory
        fields = "__all__"


class FoodTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodTag
        fields = ["id", "name", "slug"]


class FoodItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name", read_only=True)
    restaurant_name = serializers.ReadOnlyField(
        source="restaurant.name", read_only=True
    )
    food_tag = serializers.ReadOnlyField(source="tags.name", read_only=True)

    class Meta:
        model = FoodItem
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "is_available",
            "image",
            "category",
            "category_name",
            "restaurant_name",
            "tags",
            "food_tag",
        ]
