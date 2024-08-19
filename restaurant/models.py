from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"restaurant - {self.name}"