# rest_framework import
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
# django import
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# simple jwt
from rest_framework_simplejwt.tokens import RefreshToken
# local app import
from .serializers import CustomUserSerializer,BasketSerializer
from .models import Basket
from conf.views import AuthModelViewSet

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

class BasketViewSet(AuthModelViewSet):
    queryset=Basket.objects.all()
    serializer_class=BasketSerializer

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=self.data)
        serializer.is_valid(raise_exception=True)

        instance=Basket.objects.get_or_create(user=self.data["user"],product=self.data['product'])[0]
        instance.amount=self.data.get("amount",instance.amount)
        instance.save()

        serializer = self.get_serializer(instance,many=False)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
