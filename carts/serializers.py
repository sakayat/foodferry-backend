from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    food_item_name = serializers.CharField(source="food_item.name", read_only=True)
    food_item_price = serializers.CharField(source="food_item.price", read_only=True)
    total_price = serializers.ReadOnlyField()
    food_image = serializers.CharField(source="food_item.image", read_only=True)
    class Meta:
        model = CartItem
        fields = [
            "id",
            "food_item",
            "food_item_name",
            "food_item_price",
            "quantity",
            "total_price",
            "food_image",
        ]
        read_only_fields = ["food_item"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ["id", "user", "items", "created_at"]
