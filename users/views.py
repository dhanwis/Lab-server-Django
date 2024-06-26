from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
import random
import datetime
from .utils import send_otp
from labs.models import UserManage  
from labs.permissions import IsUser
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from labs.models import Reservation
from .serializers import ReservationSerializer



class UserRegistration(APIView):
    permission_classes=[AllowAny]
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
            return Response({'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
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
    permission_classes = [IsAuthenticated, IsUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = ReservationSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.filter(client=user)


