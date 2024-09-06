from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
import random
import datetime
from .utils import send_otp
from labs.models import UserManage, TestResult, TestReview
from labs.permissions import IsUser
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from labs.models import Reservation
from .serializers import ReservationSerializer, TestReviewSerializer, LabReviewSerializer
from labs.permissions import IsLab
from django.http import FileResponse
from labs.models import *
from labs.serializers import *

class UserRegistration(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        contact = request.data.get('contact')
        if not contact:
            return Response("Phone number is required", status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserManage.objects.get(contact=contact)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
        
        # Generate OTP and update user record
        otp = random.randint(1000, 9999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)

        user.otp = otp
        user.otp_expiry = otp_expiry
        user.save()

        # Function to send OTP, adjust this according to your sending method
        send_otp(user.contact, otp, user)

        return Response("Successfully generated OTP", status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        otp = request.data['otp']
        print(otp)
        user = UserManage.objects.get(otp=otp)
        if user:
            login(request, user)
            user.otp = None
            user.otp_expiry = None
            user.max_otp_try = 3
            user.otp_max_out = None
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({'access': str(refresh.access_token),
                            'user_id': user.id}, status=status.HTTP_200_OK)
        else:
            return Response("Please enter the correct OTP", status=status.HTTP_400_BAD_REQUEST)





# {
#   "email": "example@example.com",
#   "contact": "1234567890",
#   "profile_pic": "path/to/profile_pic.jpg",
#   "address": "123 Street Name",
#   "city": "City",
#   "state": "State",
#   "pincode": "123456",
#   "name": "John Doe"
# }




class UpdateCurrentUserView(APIView):
    permission_classes = [IsAuthenticated,IsUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserSerializers(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializers(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(is_customer=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        user = request.user
        serializer = UserSerializers(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(is_customer=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    

class ReservationViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated,IsUser]
    authentication_classes=[JWTAuthentication]
    serializer_class=ReservationSerializer
    
    def get_queryset(self):
        user=self.request.user
        qs=Reservation.objects.filter(client=user)  
        return qs

class TestresultDownloadAPIView(APIView) :
    permission_classes=[IsAuthenticated,IsUser]
    authentication_classes=[JWTAuthentication]

    def get(self, request, pk, format=None):
        try:
            test_result = TestResult.objects.get(pk=pk, user=request.user)
        except TestResult.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        response = FileResponse(test_result.result_file, as_attachment=True)
        return response

class TestReviewAPIView(APIView) :
    permission_classes = [IsAuthenticated, IsUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request, format=None) :
        serializer = TestReviewSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AllLabViewAPIView(APIView) :
    permission_classes = [AllowAny]
    def get(self, request, format=None) :
        labs = UserManage.objects.filter(is_lab=True)
        serializer = UserSerializer(labs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LabDetailAPIView(APIView) :
    permission_classes = [AllowAny]
    def get(self, request, usermanage_id) :
        try :
            lab=UserManage.objects.get(id=usermanage_id, is_lab=True)
            serializer = UserSerializer(lab)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except :
            return Response({'details' : 'No labs found'}, status=status.HTTP_404_NOT_FOUND)
    
class AllPackageAPIView(APIView) :
    permission_classes=[AllowAny]
    def get(self, request, format=None) :
        packages = Package.objects.all()
        serializer = PackageSerializers(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllDoctorView(APIView) :
    permission_classes=[AllowAny]
    def get(self, request, format=None) :
        doctors = Doctor.objects.all()
        serializer = DoctorsSerializers(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LabDoctorAPIView(APIView) :
    permission_classes=[AllowAny]

    def get(self, request, lab_id):
        try:
            lab = UserManage.objects.get(id=lab_id, is_lab=True)
        except UserManage.DoesNotExist:
            return Response({'detail': 'Lab not found'}, status=status.HTTP_404_NOT_FOUND)

        doctors = Doctor.objects.filter(lab=lab)
        serializer = DoctorsSerializers(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LabpackageAPIView(APIView) :
    permission_classes = [AllowAny]

    def get(self, request, lab_id) :
        try :
            lab = UserManage.objects.get(id=lab_id, is_lab=True)
        except UserManage.DoesNotExist :
            return Response ({'detail' : 'Lab not found'}, status=status.HTTP_404_NOT_FOUND)

        packages = Package.objects.filter(lab_name=lab)
        serializer = PackageSerializers(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LabTestsAPIView(APIView) :
    permission_classes=[AllowAny]

    def get(self, request, lab_id) :
        try :
            lab = UserManage.objects.get(id=lab_id, is_lab=True)
        except UserManage.DoesNotExist :
            return Response({'details' : 'Lab not found'}, status=status.HTTP_404_NOT_FOUND)
        
        tests = Test.objects.filter(lab=lab)
        serializer = TestSerializers(tests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LabTimeSlotAPIView(APIView) :
    permission_classes = [AllowAny]

    def get(self, request, lab_id) :
        try :
            lab = UserManage.objects.get(id=lab_id, is_lab=True)
        except UserManage.DoesNotExist :
            return Response({'details' : 'Lab not found'}, status=status.HTTP_404_NOT_FOUND)

        timeslot = TimeSlot.objects.filter(lab=lab)
        serializer = TimeSlotSerilaizer(timeslot, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AllTestReviewAPIView(APIView) :
    permission_classes = [AllowAny]

    def get(self, request, test_id) :
        try :
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist :
            return Response({'details' : 'Test not found'}, status=status.HTTP_404_NOT_FOUND)
        
        testreview = TestReview.objects.filter(test=test)
        serializer = TestReviewSerializer(testreview, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserDetailsAPIView(APIView) :
    permission_classes = [AllowAny]

    def get(self, request, usermanage_id) :
        try :
            user = UserManage.objects.get(id=usermanage_id, is_customer=True)
            serializer = UserSerializers(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except UserManage.DoesNotExist :
            return Response({'details' : 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class LabReviewAPIView(APIView) :
    permission_classes = [IsAuthenticated, IsUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request, format=None) :
        serializer = LabReviewSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllReviewAPIView(APIView) :
    permission_classes = [AllowAny]

    def get(self, request, lab_id) :
        try :
            lab = UserManage.objects.get(id=lab_id, is_lab=True)
        except UserManage.DoesNotExist :
            return Response({'details' : 'Lab not found'}, status=status.HTTP_404_NOT_FOUND)
        
        labreview = LabReview.objects.filter(lab=lab)
        serializer = LabReviewSerializer(labreview, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TestResultAPIView(APIView) :
    permission_classes = [IsAuthenticated, IsUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request, reservation_id, format=None) :
        try :
            reservation = Reservation.objects.get(id=reservation_id) 
        except Reservation.DoesNotExist :
            return Response({'details' : 'Reservation not found'}, status=status.HTTP_404_NOT_FOUND)
        
        result = TestResult.objects.filter(reservation=reservation)
        serializer = TestResultSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TestDetailAPIView(APIView) :
    permission_classes = [AllowAny]

    def get(self, request, id, format=None) :
        try :
            test = Test.objects.get(id=id)
            serializer = TestSerializers(test)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Test.DoesNotExist :
            return Response({'details' : 'Test not found'}, status=status.HTTP_404_NOT_FOUND)
        
class TimeSlotDetailAPIView(APIView) :
    permission_classes = [AllowAny]

    def get(self, request, id, format=None) :
        try :
            timeslot = TimeSlot.objects.get(id=id)
            serializer = TimeSlotSerilaizer(timeslot)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TimeSlot.DoesNotExist :
            return Response({'details' : 'Time slot not found'}, status=status.HTTP_404_NOT_FOUND)
        
