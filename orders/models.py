from django.db import models
from accounts.models import CustomUser
from restaurant.models import FoodItem


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone = models.PositiveIntegerField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=20, default="Dhaka")
    postal_code = models.PositiveIntegerField(max_length=10, blank=True, null=True)
    payment_method = models.CharField(max_length=30, default="Cash on delivery")
    status = models.CharField(max_length=30, default="pending")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.user.id} by {self.user.username}"


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.PositiveIntegerField(default=1)
    
    def __str__(self) -> str:
        return self.item_name