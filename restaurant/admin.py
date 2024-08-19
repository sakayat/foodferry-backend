from django.contrib import admin
from .models import Restaurant, FoodItem, FoodCategory

# Register your models here.

class FoodCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"restaurant_slug": ["name"]}

admin.site.register(Restaurant)
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)