from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r"reservartion",ReservationViewset, basename='reservation')


urlpatterns = [
    path("register/",UserRegistration.as_view(),name="user-register"),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('users/update/', UpdateCurrentUserView.as_view(), name='update-current-user'),
]


