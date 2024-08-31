from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number", "profile_image")}),
        ("Role", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
