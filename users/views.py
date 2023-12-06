# rest_framework import
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
# django import
from django.contrib.auth import get_user_model
# simple jwt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
# local app import
from .serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False,methods=['GET'])
    def get_token(self,request,*args,**kwargs):
        fake_user=get_user_model().objects.create_fake_user()
        refresh = RefreshToken.for_user(fake_user)
        access_token = str(refresh.access_token)
        response_data = {
            'access_token': access_token,
        }
        return Response(response_data,status=status.HTTP_200_OK)#TODO HttpOnly technology tutorial

    @action(detail=False, methods=['post'])
    def check_token(self, request):
        return Response({'detail': 'Access token is valid'}, status=status.HTTP_200_OK)
