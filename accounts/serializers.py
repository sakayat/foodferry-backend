from rest_framework import serializers
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "role",
            "password",
            "confirm_password",
        ]

    def save(self):
        username = self.validated_data["username"]
        email = self.validated_data["email"]
        password = self.validated_data["password"]
        password2 = self.validated_data["confirm_password"]

        if password != password2:
            raise serializers.ValidationError({"error": "password does'nt match"})

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "email already exists"})

        account = CustomUser(username=username, email=email)
        account.set_password(password)
        
        account.is_active = False
        account.save()
        return account
    

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
        ]
        read_only_fields = ["id", "username", "email", "role"]
