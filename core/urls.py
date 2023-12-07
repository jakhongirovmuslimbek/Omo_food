from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .swagger import schema_view
from .routers import products_router,users_router

urlpatterns = [
   path('admin/', admin.site.urls),
   path("api/v1/",include("core.routers")),
   # path('api/v1/', include(products_router.urls)),
   # path('api/v1/', include(users_router.urls)),

   # path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   # path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
