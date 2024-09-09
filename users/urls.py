from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reservations', ReservationViewset, basename='reservation')


urlpatterns = [
    path("register/",UserRegistration.as_view(),name="user-register"),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('users/update/', UpdateCurrentUserView.as_view(), name='update-current-user'),
    path('users/testresult/<int:pk>/', TestresultDownloadAPIView.as_view(), name='test-result'),
    path('test_review/', TestReviewAPIView.as_view(), name='test-review'),
    path('all-labs/',AllLabViewAPIView.as_view(), name='all-labs-view'),
    path('lab-detail/<int:usermanage_id>/', LabDetailAPIView.as_view(), name='lab-detail-view'),
    path('all-package/', AllPackageAPIView.as_view(), name='all-package-view'),
    path('all-doctor/', AllDoctorView.as_view(), name='all-doctor-view'),
    path('lab-doctor/<int:lab_id>/',LabDoctorAPIView.as_view(), name='lab-doctors'),
    path('lab-package/<int:lab_id>/',LabpackageAPIView.as_view(), name='lab-package'),
    path('lab-tests/<int:lab_id>/', LabTestsAPIView.as_view(), name='lab-tests'),
    path('lab-timeslot/<int:lab_id>/', LabTimeSlotAPIView.as_view(), name='lab-timeslot'),
    path('all-testreview/<int:test_id>/', AllTestReviewAPIView.as_view(), name='all-testreview'),
    path('userdata/<int:usermanage_id>/',UserDetailsAPIView.as_view(), name='userdata'),
    path('lab-review/', LabReviewAPIView.as_view(), name='lab-review'),
    path('lab-allreview/<int:lab_id>/', AllReviewAPIView.as_view(), name='lab-allreview'),
    path('testresult/<int:reservation_id>/', TestResultAPIView.as_view(), name='testresult'),
    path('test-detail/<int:id>/', TestDetailAPIView.as_view(), name='test-detail'),
    path('timeslot-details/<int:id>/', TimeSlotDetailAPIView.as_view(), name='timeslot-details'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]