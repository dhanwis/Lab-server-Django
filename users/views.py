from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import random
import datetime
from .utils import send_otp
from labs.models import UserManage  
import requests
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializers



class UserRegistration(APIView):
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