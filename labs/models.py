from django.db import models
from django.contrib.auth.models import AbstractUser,Permission,Group
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class UserManage(AbstractUser):
    is_customer = models.BooleanField(default=False)
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
    profile_pic = models.ImageField(upload_to="media/", blank=True, null=True)
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
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self._create_user(username, email, password, **extra_fields)



class Test(models.Model):
    lab = models.ForeignKey(UserManage, on_delete=models.CASCADE, limit_choices_to={'is_lab': True}, related_name="tests")
    testname = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    testprice = models.IntegerField()

    def __str__(self):
        return self.testname
    

class Package(models.Model):
    lab_name=models.ForeignKey(UserManage,on_delete=models.CASCADE, limit_choices_to={'is_lab': True}, related_name="labs")
    packagename=models.CharField(max_length=20,null=True,blank=True)
    tests=models.ManyToManyField(Test, related_name="packages") 
    price=models.IntegerField()
    packageimage=models.FileField(upload_to='media/',null=True,blank=True)

    def __str__(self):
        return self.packagename


class Doctor(models.Model):
    lab=models.ForeignKey(UserManage,on_delete=models.CASCADE,limit_choices_to={'is_lab': True}, related_name="lab_docter")
    doctorname=models.CharField(max_length=20)
    qualification=models.CharField(max_length=20)
    specialiazation=models.CharField(max_length=20)
    doctorimage=models.FileField(upload_to='media/',null=True,blank=True)

    def __str__(self) :
        return self.doctorname
    
    
class TimeSlot(models.Model):
    lab = models.ForeignKey(UserManage, on_delete=models.CASCADE, limit_choices_to={'is_lab': True}, related_name='time_slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_clients = models.PositiveIntegerField() 

    def __str__(self):
        return f"{self.lab.labname}: {self.start_time} - {self.end_time}"
    
 
class Reservation(models.Model):
    status_choice=[
        ("pending","Pending"),
        ("approved","Approved"),  
        ("rejected","Rejected")
    ]
    lab=models.ForeignKey(UserManage,on_delete=models.CASCADE, limit_choices_to={'is_lab': True}, related_name="res_lab")
    client = models.ForeignKey(UserManage, on_delete=models.CASCADE, related_name='reservations')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='reservations')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='reservations')
    status=models.CharField(max_length=10,choices=status_choice,default="pending")    

    def save(self, *args, **kwargs):
        if self.time_slot.reservations.count() >= self.time_slot.max_clients:
            raise ValueError('This time slot is full.')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.name} - {self.test.testname} on {self.time_slot.start_time}"
    
class TestResult(models.Model) :
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='test_result')
    result_file = models.FileField(upload_to='test-result/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f"{self.reservation.client.email} - {self.reservation.test.testname}"
    
class TestReview(models.Model) :
    user = models.ForeignKey(UserManage, on_delete=models.CASCADE, limit_choices_to={'is_customer' : True}, related_name='test_review')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_reviews')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class TestReviewReply(models.Model) :
    lab_admin = models.ForeignKey(UserManage, on_delete=models.CASCADE, limit_choices_to={'is_lab' : True}, related_name='review_reply')
    review = models.ForeignKey(TestReview, on_delete=models.CASCADE, related_name='test_review_reply')
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class LabReview(models.Model) :
    user = models.ForeignKey(UserManage, on_delete=models.CASCADE, limit_choices_to={'is_customer' : True}, related_name='lab_review')
    lab = models.ForeignKey(UserManage, on_delete=models.CASCADE, limit_choices_to={'is_lab' : True})
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    

