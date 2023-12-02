from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField
from imagekit.processors import Transpose

# admin
class AdminProfile(AbstractUser):
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.FileField(upload_to="images/admin/%y%m%d", blank=True, null=True)
    thumbnail_image = ImageSpecField(
        source = 'image',
        processors = [Transpose(),],
        format = 'JPEG',
        options = {'quality':60}
    )

# users
class Customer(models.Model):
    username = models.CharField(max_length=255)
    main_phone_number = models.DecimalField(max_digits=12, decimal_places=0)
    additional_phone_number = models.DecimalField(max_digits=12, decimal_places=0)
    location = models.CharField(max_length=300)
    date_joined = models.DateTimeField(auto_now_add=True)
    
