from django.urls import path
from houses import views

urlpatterns = [
    path('users/', views.UsersList.as_view(), name='users'),
    path('houses/', views.HousesList.as_view(), name='houses'),
    path('images/', views.ImagesList.as_view(), name='images'),
]