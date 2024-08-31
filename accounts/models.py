from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    ROLL_CHOICE = [
        ("customer", "Customer"),
        ("restaurant_owner", "Restaurant Owner"),
        ("admin", "Admin"),
    ]
    profile_image = models.ImageField(upload_to="profile/images/", default="")
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLL_CHOICE, default="customer")
    

    def __str__(self):
        return f"{self.username} - {self.role}"
