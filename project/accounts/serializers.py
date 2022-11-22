from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError

from .models import User
from django.utils import timezone

from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    RefreshToken,
    api_settings,
    update_last_login,
)

from rest_framework.response import Response
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        # fields = ["email", "username", "password"]
        fields = '__all__'

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used. Please use another email")

        #else
        return super().validate(attrs)

    def create(self, validate_data):
        password = validate_data.pop("password")

        user = super().create(validate_data)

        user.set_password(password)
        user.is_active = True
        user.last_login = timezone.now()
        user.save()

        Token.objects.create(user=user)
        return user

class CurrentUserPostsSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many = True, view_name="post_detail", queryset=User.objects.all()
    )


'''
2nd TokenObtainer
for obtaining users details during login
'''
class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['message'] = 'Login Successful'
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        my_user = User.objects.filter(pk=self.user.id).first()
        if my_user:
             # use user serelizer or parse required fields
            #data['user'] = my_user
            data['user'] = {
                'id': self.user.id,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
                "phone": self.user.phone,
                "password": self.user.password,
                "gender": self.user.gender,

                "last_login": timezone.now(),
                "is_superuser": self.user.is_superuser,
                "is_active": self.user.is_active,
                "date_joined": self.user.date_joined,
                "groups": [],
                "user_permissions": [],
            }
            serelizer = UserSerializer(my_user)

            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, self.user)

            return data
            #return serializer.data