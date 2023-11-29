from django.db import models
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import Transpose

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(editable=False)
    image = models.FileField(upload_to="images/categories/%y%m%d", blank=True, null=True)
    thumbnail_image = ImageSpecField(
        source = 'image',
        processors = [Transpose(),],
        format = 'JPEG',
        options = {'quality':30}
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(editable=False)
    image = models.FileField(upload_to="images/subcategories/%y%m%d", blank=True, null=True)
    thumbnail_image = ImageSpecField(
        source = 'image',
        processors = [Transpose(),],
        format = 'JPEG',
        options = {'quality':30}
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Product(models.Model):
    MEASURE_TYPE = (
        ("kg", "kg"),
        ("litr", "litr"),
        ("dona", "dona"),
        ("metr", "metr")
    )
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name="products", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount = models.FloatField(default=0)
    amount_measure = models.CharField(max_length=25, choices=MEASURE_TYPE, default="kg")
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to="images/products/%y%m%d")
    thumbnail_image = ImageSpecField(
        source = 'image',
        processors = [Transpose(),],
        format = 'JPEG',
        options = {'quality':30}
    )

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.FileField(upload_to="images/products/%y%m%d")
    thumbnail_image = ImageSpecField(
        source = 'image',
        processors = [Transpose(),],
        format = 'JPEG',
        options = {'quality':30}
    )

    def __str__(self):
        return self.product.title


class Discount(models.Model):
    DISCOUNT_TYPE = (
        ("percentage", "Percentage"),   # dinamik chegirma
        ("fixed", "Fixed Amount"),      # fixed chegirma
    )
    title = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE, default="percentage")
    value = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    product = models.ForeignKey(Product, related_name="discounts", on_delete=models.CASCADE, blank=True)
    products = models.ManyToManyField(Product, related_name="discount_many", blank=True)
    category = models.ManyToManyField(Category, related_name="discounts", blank=True)
    subcategory = models.ManyToManyField(SubCategory, related_name="discounts", blank=True)
    
    def apply_discount(self, original_price):
        if self.discount_type == "percentage":
            discount_amount = (self.value / 100) * original_price
            discounted_price = original_price - discount_amount
        elif self.discount_type == "fixed":
            discounted_price = max(original_price - self.value, 0)
        else:
            discounted_price = original_price
        return round(discounted_price, 2)        
    
    def __str__(self):
        return self.title
    




"""
discount
    start date 
    end date
    foiz
    products(manytomany) blank true
    category(manytomany) blank true
    subcategory(manytomany) blank true
    products_status (tanlanganlarga, barcha maxsulotlarga)
    discount_status (fixed chegirma, dinamik chegirma % )
    
"""


