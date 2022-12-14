from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import serializers 
from .models import User

from .serializers import SignUpSerializer, UserDetailSerializer
from .tokens import create_jwt_pair_user

from rest_framework_simplejwt.serializers import(
    TokenObtainSerializer,
    RefreshToken,
    api_settings,
    update_last_login,
)

from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

from rest_framework_simplejwt.views import TokenViewBase

class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request:Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()
            response = {"message": "User Created Successfully", "user": serializer.data}
            # response = serializer.data
            return Response(data=response, status=status.HTTP_201_CREATED)
        #else
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes=[]

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_user(user)
            response = {"message": "Login Successful", "token": tokens}
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password, pr user does not exist"})

    def get(self, request: Request):
        content= {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=content, status = status.HTTP_200_OK)

#SECOND TOKEN OBTAINER.... USE THIS TO OBTAIN BOTH TOKENS AND USERS DATA
class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = serializers.TokenObtainPairSerializer

class UserDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes =[IsAuthenticated] # Before updating, user must provide jwt tokens which are obtained from login page...

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            #else
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format = None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)