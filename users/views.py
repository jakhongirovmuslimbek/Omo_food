from rest_framework import viewsets
from .serializers import AdminSerializer, CustomerSerializer
from django.contrib.auth import get_user_model
from .models import Customer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = AdminSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer