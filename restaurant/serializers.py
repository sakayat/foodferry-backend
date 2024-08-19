from rest_framework import serializers
from .models import Restaurant, FoodCategory, FoodItem


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = "__all__"
        read_only_fields = ['id', 'owner', 'is_approved']
        
        
class FoodCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FoodCategory
        fields = "__all__"
        read_only_fields = ['restaurant']



