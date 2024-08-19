from django.contrib import admin
from .models import Restaurant, FoodItem

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(FoodItem)