from rest_framework import serializers
from . import models

class CategorySerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.ImageField(read_only=True)

    class Meta:
        model = models.Category
        fields = "__all__"

class SubCategorySerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.ImageField(read_only=True)
    class Meta:
        model = models.SubCategory
        fields = "__all__"

    def get_category(self, obj):
        category = obj.category
        data = {
            "id": category.id,
            "title": category.title,
        }
        return data

    def __init__(self, *args, **kwargs):
        super(SubCategorySerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method == "GET":
            self.fields["category"] = serializers.SerializerMethodField("get_category")

class ProductSerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.ImageField(read_only=True)

    class Meta:
        model = models.Product
        fields = "__all__"

    def get_category(self, obj):
        category = obj.category
        data = {
            "id": category.id,
            "title": category.title,
        }
        return data

    def get_subcategory(self, obj):
        subcategory = obj.subcategory
        if subcategory:
            data = {
                "id": subcategory.id,
                "title": subcategory.title,
            }
            return data
        else:
            return None

    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method == "GET":
            self.fields["category"] = serializers.SerializerMethodField("get_category")
            self.fields["subcategory"] = serializers.SerializerMethodField("get_subcategory")

class ProductImageSerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.ImageField(read_only=True)

    class Meta:
        model = models.ProductImage
        fields = "__all__"

    def get_product(self, obj):
        product = obj.product
        data = {
            "id": product.id,
            "product": product.title
        }
        return data

    def __init__(self, *args, **kwargs):
        super(ProductImageSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method == "GET":
            self.fields["product"] = serializers.SerializerMethodField("get_product")