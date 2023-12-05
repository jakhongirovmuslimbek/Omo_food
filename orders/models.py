from django.db import models
from users.models import Customer
from products.models import Product

class Card(models.Model):
    products = models.ManyToManyField(Product, related_name="products")
    created_date = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    PAYMENT_TYPE = (
        ('naqd', 'Naqd'),
        ('karta orqali', 'Karta orqali'),
    )
    card = models.ForeignKey(Card, related_name="orders", on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, related_name="user_orders", on_delete=models.PROTECT)
    payment = models.CharField(max_length=255, choices=PAYMENT_TYPE, default="naqd")
        