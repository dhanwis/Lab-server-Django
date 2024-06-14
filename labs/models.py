from django.db import models
from django.contrib.auth.models import AbstractUser,Permission,Group
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class UserManage(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_lab = models.BooleanField(default=False)
    labname = models.CharField(max_length=30)
    contact = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=150,null=True,blank=True)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)],default=0.0)
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)],default=0.0)   
    address = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=20,null=True,blank=True)
    state = models.CharField(max_length=20,null=True,blank=True)
    status = models.CharField(max_length=20,default='enable')
    
    

    groups = models.ManyToManyField(
        Group,
        related_name='user_manage_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user_manage',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_manage_set', 
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user_manage',
    )
    
# class lab(models.Model):
    
#     packages=models.CharField(max_length=20,null=True,blank=True)
#     test=models.CharField(max_length=20,null=True,blank=True)
#     doctors=models.CharField(max_length=20,null=True,blank=True)
