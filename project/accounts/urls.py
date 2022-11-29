from django.urls import path
from .views import SignUpView, LoginView
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"), #This will only give a result of tokens only
    path("login2/", views.TokenObtainPairView.as_view(), name="login2"), #This will only give a result of tokens and user's data ;-)
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("update/<int:pk>/", views.UserDetail.as_view(), name="update"),
]
