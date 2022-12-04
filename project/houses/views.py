from django.shortcuts import render
from rest_framework import generics
from .models import Users, Houses, Images
from .serializers import UsersSerializer, HousesSerializer, ImagesSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UsersList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [SearchFilter]
    searh_fields = ['agent_name']

class HousesList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Houses.objects.all()
    serializer_class = HousesSerializer
    filter_backends = [SearchFilter]
    searh_fields = ['category', 'description', 'loaction', 'monthly_price']

class ImagesList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    filter_backends = [SearchFilter]
    searh_fields = ['title', 'description',]
    