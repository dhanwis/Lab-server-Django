from django.urls import path
from .views import *

urlpatterns = [
    path('labadd/',LabAdd.as_view()),
    path('labedit/<int:admin_id>/',LabEdit.as_view()),
    path('login/',Login.as_view()),
    # path('userregister/',UserRegistration.as_view()),
    # path('loginn/', LoginView.as_view(),name='login'),
    # path('verifyotp/', VerifyOTPView.as_view(),name='verify-otp'),
]
