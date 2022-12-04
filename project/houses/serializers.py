from rest_framework import serializers
from .models import Users, Houses, Images

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'

class HousesSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(read_only=True, many=True)
    class Meta:
        model = Houses
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    houses = HousesSerializer(read_only=True, many=True)
    class Meta:
        model=Users
        fields='__all__'