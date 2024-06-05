from django.db import models
from django.contrib.auth.models import AbstractUser,Permission,Group
# Create your models here.

class UserManage(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_lab = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        Group,
        related_name='user_manage_set',  # unique related_name to avoid conflict
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user_manage',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_manage_set',  # unique related_name to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user_manage',
    )


class Admin(models.Model):
    
    lab = models.CharField(max_length=30)