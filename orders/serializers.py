from rest_framework import serializers
from .models import Order, OrderDetails


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["id", "user", "subtotal", "shipping_cost", "total", "status"]


class OrderDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderDetails
        fields = "__all__"


class UserOrderSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="order.user.username", read_only=True)
    address = serializers.ReadOnlyField(source="order.address", read_only=True)
    email = serializers.ReadOnlyField(source="order.user.email", read_only=True)
    phone_number = serializers.ReadOnlyField(source="order.user.phone_number", read_only=True)
    class Meta:
        model = OrderDetails
        fields = ["id", "item_name", "item_price", "quantity", "status", "subtotal", "username", "address", "email", "phone_number"]
        
    
class UserOrderStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderDetails
        fields = ["status"]
        
        