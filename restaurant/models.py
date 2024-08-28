from django.db import models
from accounts.models import CustomUser
from django.utils.text import slugify

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    cover_image=models.ImageField(upload_to="restaurant/cover/images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"restaurant - {self.name}"
    
    
class FoodCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to="categories/images", blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"
    
class FoodTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name
    
    
class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="food/images/", null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="foods", blank=True, null=True)
    tags = models.ForeignKey(FoodTag, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name}"
    