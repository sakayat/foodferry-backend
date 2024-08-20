from django.db import models
from accounts.models import CustomUser
from restaurant.models import FoodItem

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.user.username
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self) -> str:
        return f"{self.food_item.name}-{self.quantity}"
    
    def total_price(self):
        return self.quantity * self.food_item.price