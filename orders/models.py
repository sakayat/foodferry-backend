from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=30, choices=[("Completed", "Completed"), ("Canceled", "Canceled"), ("Paid", "Paid")], default="Pending")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    payment_id = models.CharField(max_length=24, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order by {self.user.first_name} transaction_id {self.payment_id}"


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)
    item_image = models.CharField(max_length=255, blank=True, null=True)
    restaurant=models.CharField(max_length=100, blank=True, null=True)
    status=models.CharField(max_length=20, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.item_name
    


