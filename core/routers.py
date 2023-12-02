from rest_framework.routers import DefaultRouter
from products.views import CategoryViewSet, SubCategoryViewSet, ProductViewSet, ProductImageViewSet, DiscountViewSet
from users.views import AdminViewSet, CustomerViewSet

router = DefaultRouter()
# Products 
router.register("categories", CategoryViewSet, basename="categories")
router.register("sub-categories", SubCategoryViewSet, basename="sub-categories")
router.register("products", ProductViewSet, basename="products")
router.register("product-images", ProductImageViewSet, basename="product-images")
router.register("discounts", DiscountViewSet, basename="discount")
# Users
router.register("admin", AdminViewSet, basename="admins")
router.register("customers", CustomerViewSet, basename="customers")
