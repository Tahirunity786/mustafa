from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission
from control_account.manager import CustomUserManager

class User(AbstractUser):
    # General Information about the user
    profile = models.ImageField(upload_to="profile/images", blank=True, null=True)
    username = models.CharField(max_length=100, unique=True, db_index=True, null=True, blank=True)
    first_name = models.CharField(max_length=100,db_index=True, default="")
    last_name = models.CharField(max_length=100,db_index=True, default="")
    nationality = models.CharField(max_length=100, db_index=True, default="")
    payment_method = models.CharField(max_length=100, db_index=True, default="")
    email = models.EmailField(null=False, unique=True)  
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=None, null=True)
    is_blocked = models.BooleanField(default=False, null=True)
    is_verified = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    password = models.CharField(max_length=200,db_index=True, default=None )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    # Unique related_name for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', blank=True)
  

    