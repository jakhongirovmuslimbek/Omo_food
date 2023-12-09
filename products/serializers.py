from rest_framework import serializers
from . import models
from django.urls import reverse

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

class CategorySerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.ImageField(read_only=True)

    class Meta:
        model = models.Category
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and request.method == "GET":
            subcategory=request.GET.get("subcategory",False)=="true"
            if subcategory:
                self.fields["subcategories"] = SubCategorySerializer(many=True, read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.ImageField(read_only=True)

    class Meta:
        model = models.Product
        fields = "__all__"

    def get_images(self, obj):
        images = obj.images.all()
        return images

    def get_category(self, obj):
        # category = obj.category
        # request = self.context.get('request')

        # if category.image:
        #     image_url = request.build_absolute_uri(category.image.url)
        # else:
        #     None    

        # data = {
        #     "id": category.id,
        #     "title": category.title,
        #     "image": image_url
        # }
        serializer=CategorySerializer(obj.category,many=False,context=self.context)
        return serializer.data

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
            # self.fields["price"]=serializers.IntegerField(source="price")
            self.fields["discount"] = serializers.DictField(source="check_discount")
            category=request.GET.get("category",None)=='true'
            if category:
                self.fields["category"] = serializers.SerializerMethodField("get_category")
            subcategory=request.GET.get("subcategory",None)=='true'
            if subcategory:
                self.fields["subcategory"] = serializers.SerializerMethodField("get_subcategory")
            images=request.GET.get("images",None)=='true'
            if images:
                self.fields["images"] = ProductImageSerializer(serializers.SerializerMethodField("get_images"),many=True,context=self.context)

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
            product=request.GET.get("product",None)=='true'
            if product:
                self.fields["product"] = serializers.SerializerMethodField("get_product")

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discount
        fields = "__all__"

class BannerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BannerImage
        fields = "__all__"
        