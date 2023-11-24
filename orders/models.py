from django.db import models
from products.models import Category, SubCategory, Product

class Order(models.Model):
    product = models.ForeignKey(Product, related_name="products", on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=)10, decimal_places=2
