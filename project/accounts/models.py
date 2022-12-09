from django.db import models

# Create your models here.

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

GENDER_CHOICES = (('M','Male'),('F','Female'),)
USER_TYPE = (('A','Admin'),('C','Client'),('S','Seller'),)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(email, **extra_fields)
        user.is_active = True
        user.last_login = timezone.now()
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("last_login", timezone.now())
        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Super User has to have is_staff being True")
        
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Super User has to have is_superuser being True")

        return self.create_user(email = email, password=password)

class User(AbstractUser):

    email = models.CharField(max_length=80, unique = True)
    username = models.CharField(max_length=45)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default='M', null=True,  blank=True) #Gender can be empty
    user_type = models.CharField(max_length=1,choices=USER_TYPE,default= 'C')
    profile_image = models.TextField(null=True,  blank=True) #TextField has inifinite max length
    has_houses = models.BooleanField(default=False) #Check if user has houses.
    
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def _str_(self):
        return self.username+ ' '+self.email

#For updating user profle ;-)
#Can't update user through above User(AbstractUser) because email,username,password fields cant be empty... of which we dont want the user to update email and password fields.
class UserDetail(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=20)
    profile_image = models.TextField(null=True,  blank=True) #TextField has inifinite max length
    has_houses = models.BooleanField(default=False) #Check if user has houses.

