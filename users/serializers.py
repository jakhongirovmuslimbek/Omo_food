from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer

class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"}) 
    thumbnail_image = serializers.ImageField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "middle_name",
            "image",
            "thumbnail_image",
            "email",
            "user_permissions",

        ]
        extra_kwargs = {"password": {"write_only": True}}


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"