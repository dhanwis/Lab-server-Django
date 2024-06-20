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
    name = models.CharField(max_length=30,null=True,blank=True)
    profile_pic = models.ImageField(upload_to="static/images/profile", blank=True, null=True)
    pincode = models.CharField(max_length=20,null=True,blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=3)
    otp_max_out = models.DateTimeField(blank=True, null=True)
    

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

class Package(models.Model):
    
    packagename=models.CharField(max_length=20,null=True,blank=True)
    tests=models.CharField(max_length=20)
    price=models.IntegerField()
    packageimage=models.FileField(upload_to='media/',null=True,blank=True)

    def __str__(self):
        return self.packagename

class Test(models.Model):
    testname=models.CharField(max_length=20)
    package=models.ForeignKey(Package,on_delete=models.CASCADE,related_name='package')
    description=models.CharField(max_length=20)
    testprice=models.IntegerField()
    
    def __str__(self):
        return self.testname
    

class Doctor(models.Model):
    doctorname=models.CharField(max_length=20)
    qualification=models.CharField(max_length=20)
    specialiazation=models.CharField(max_length=20)
    doctorimage=models.FileField(upload_to='media/',null=True,blank=True)

    def __str__(self) :
        return self.doctorname
    

# class TestReport(models.Model):
#     customername =models

