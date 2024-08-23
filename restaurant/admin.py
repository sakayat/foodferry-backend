from django.contrib import admin
from .models import Restaurant, FoodItem, FoodCategory, FoodTag

# Register your models here.


class RestaurantAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class FoodCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class FoodTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(FoodTag, FoodTagAdmin)
