from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission
from control_account.manager import CustomUserManager

class User(AbstractUser):
    # General Information about the user
    profile = models.ImageField(upload_to="profile/images", blank=True, null=True)
    username = models.CharField(max_length=100, unique=True, db_index=True, null=True, blank=True)    
    email = models.EmailField(unique=True)  
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

class PersonalDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    full_name = models.CharField(max_length=100,db_index=True, default="")
    nationality = models.CharField(max_length=100, db_index=True, default="")
    date_ordered = models.DateField(db_index=True,auto_now_add=True)
    phone_no = models.CharField(max_length=100,db_index=True, default="")
    email = models.EmailField(db_index=True)  



