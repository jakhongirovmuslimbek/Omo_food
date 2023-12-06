# django import
from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.utils.crypto import get_random_string

class CustomUserManager(UserManager):
    def create_fake_user(self):
        # Generate a unique username
        username = get_random_string(length=10)
        # Generate a strong password (you can customize the logic for a strong password)
        password = get_random_string(length=12)
        # Create a new user with the generated username and password
        user = self.create_user(username=username, password=password)
        return user

class CustomUser(AbstractUser):
    objects = CustomUserManager()
