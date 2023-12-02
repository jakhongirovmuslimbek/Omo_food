from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .routers import router
from .swagger import schema_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import Dict,Any,api_settings,update_last_login,TokenObtainSerializer
from users.serializers import AdminSerializer

class CustomTokenObtainPairSerializer(TokenObtainSerializer):
   token_class = RefreshToken

   def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
      data = super().validate(attrs)

      refresh = self.get_token(self.user)

      data['user'] = AdminSerializer(self.user,many=False,context=self.context).data
      data["access"] = str(refresh.access_token)
      data["refresh"] = str(refresh)
      
      if api_settings.UPDATE_LAST_LOGIN:
         update_last_login(None, self.user)
      return data

class CustomTokenObtainPairView(TokenObtainPairView):
   serializer_class = CustomTokenObtainPairSerializer

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/v1/', include(router.urls)),

   path('admins/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('admins/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
