from rest_framework import serializers
from .models import Order, OrderDetails


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["user", "subtotal", "shipping_cost", "total", "status"]


class OrderDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderDetails
        fields = "__all__"
