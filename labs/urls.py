from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'tests', TestViewSet, basename='test')
router.register(r'docter',DocterViewSet)
router.register(r'package',PackageViewSet)  
router.register(r'timeslot',TimeSlotViewSet)

urlpatterns = [
    path('labadd/',LabAdd.as_view()),
    path('labedit/<int:admin_id>/',LabEdit.as_view()),
    path('login/',Login.as_view()),
    path('token/superuser/', ObtainSuperuserToken.as_view(), name='token_superuser_obtain'),
    path('test-result/', TestResultAPIView.as_view(), name='test-result'),
    path('lab/test_review_reply/<int:testreview_id>/', TestReviewReplyAPIView.as_view(), name='review_reply'),
    path('all-reservations/<int:lab_id>/', AllReservationAPIView.as_view(), name='all-reservations'),
    path('reservation/status/<int:pk>/', ReservationStatusAPIView.as_view(), name='reservation-status'),
    path('', include(router.urls)),     
]
