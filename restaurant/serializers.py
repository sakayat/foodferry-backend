from rest_framework import serializers
from .models import Restaurant, FoodCategory, FoodItem, FoodTag, FoodFeedback


class FoodItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name", read_only=True)
    restaurant_name = serializers.ReadOnlyField(
        source="restaurant.name", read_only=True
    )
    food_tag = serializers.ReadOnlyField(source="tags.slug", read_only=True)
    category_slug = serializers.ReadOnlyField(source="category.slug", read_only=True)

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
            "category_slug",
            "restaurant_name",
            "tags",
            "food_tag",
            "created_at"
        ]


class RestaurantSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="owner.email")
    total_foods = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "address",
            "cover_image",
            "total_foods",
            "slug"
        ]

    def get_total_foods(self, obj):
        return obj.foods.count()


class RestaurantInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ["id", "name", "address"]


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


class FoodFeedbackSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    firstname = serializers.ReadOnlyField(source="user.first_name")
    lastname = serializers.ReadOnlyField(source="user.last_name")

    class Meta:
        model = FoodFeedback
        fields = [
            "id",
            "username",
            "firstname",
            "lastname",
            "food_item",
            "comment",
            "rating",
        ]
        read_only_fields = ["user", "food_item"]
