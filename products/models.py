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
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
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


# class Discount(models.Model):
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#     percentage = models.IntegerField(default=0, blank=True, null=True)
#     product = models.ForeignKey(Product, blank=True)
#     products = models.ManyToManyField(Product, blank=True)
#     category = models.ManyToManyField(Category, blank=True)
#     subcategory = models.ManyToManyField(SubCategory, blank=True)




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


