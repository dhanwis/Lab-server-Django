from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import * 
from users.serializers import ReservationSerializer
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated , AllowAny,IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .permissions import IsLab
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.


# {
#     "labname": "Central Lab",
#     'password':"pass@123"
#     "contact": "123-456-7890",
#     "email": "central.lab@example.com",
#     "latitude": 37.7749,
#     "longitude": -122.4194,
#     "address": "123 Main Street",
#     "city": "San Francisco",
#     "state": "California",
#     "profile_pic": "path/to/profile_pic.jpg",
#     "pincode": "94103"
# }


class ObtainSuperuserToken(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        
        try:
            user = get_user_model().objects.get(username=username)
        except user.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password) or not user.is_superuser:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class LabAdd(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        lab = UserManage.objects.filter(is_lab=True)
        serializer = UserSerializer(lab, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_lab=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LabEdit(APIView):
    permission_classes=[IsAdminUser,IsLab]
    authentication_classes=[TokenAuthentication]
    def get(self, request, admin_id, format=None):
        lab = get_object_or_404(UserManage, id=admin_id)
        serializer = UserSerializer(lab)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, admin_id, format=None):
        lab = get_object_or_404(UserManage, id=admin_id)
        serializer = UserSerializer(lab, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class Login(APIView):
    def post(self, request, format=None):
        data = request.data
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            serializer = UserSerializer(user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"user": serializer.data, "token": token.key}, status=status.HTTP_200_OK)
        return Response({"details": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    


# GET lab/package/: List all tests.
# POST lab/package/: Create a new test.
# GET lab/package/{id}/: Retrieve a specific test by ID.
# PUT lab/package/{id}/: Update a specific test by ID.
# PATCH lab/package/{id}/: Partially update a specific test by ID.
# DELETE lab/package/{id}/: Delete a specific test by ID.

class PackageViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated,IsLab]
    authentication_classes=[TokenAuthentication]
    queryset=Package.objects.all()
    serializer_class=PackageSerializers

# GET lab/tests/: List all tests.
# POST lab/tests/: Create a new test.
# GET lab/tests/{id}/: Retrieve a specific test by ID.
# PUT lab/tests/{id}/: Update a specific test by ID.
# PATCH lab/tests/{id}/: Partially update a specific test by ID.
# DELETE lab/tests/{id}/: Delete a specific test by ID.
   
class TestViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated,IsLab]
    authentication_classes=[TokenAuthentication]
    queryset = Test.objects.all()
    serializer_class = TestSerializers


# GET lab/docter/: List all tests.
# POST lab/docter/: Create a new test.
# GET lab/docter/{id}/: Retrieve a specific test by ID.
# PUT lab/docter/{id}/: Update a specific test by ID.
# PATCH lab/docter/{id}/: Partially update a specific test by ID.
# DELETE lab/docter/{id}/: Delete a specific test by ID.

class DocterViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated,IsLab]
    authentication_classes=[TokenAuthentication]
    queryset=Doctor.objects.all()
    serializer_class=DoctorsSerializers



class TimeSlotViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated,IsLab]
    authentication_classes=[JWTAuthentication]
    queryset=TimeSlot.objects.all()
    serializer_class=TimeslotSerializers
    
    
    
    
class ReservationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
