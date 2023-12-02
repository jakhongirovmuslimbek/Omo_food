from django.db import models
from users.models import Customer
from products.models import Product

class Card(models.Model):
    products = models.ManyToManyField(Product, related_name="products")
    created_date = models.DateTimeField(auto_now_add=True)


