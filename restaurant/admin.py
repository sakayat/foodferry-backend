from django.contrib import admin
from .models import Restaurant, FoodItem, FoodCategory

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(FoodItem)
admin.site.register(FoodCategory)