from rest_framework.decorators import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import * 
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets 
from rest_framework.permissions import IsAuthenticated , AllowAny,IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .permissions import IsLab
from django.shortcuts import get_object_or_404
from users.serializers import TestReviewSerializer, ReservationSerializer, LabReviewSerializer
# Create your views here.


# {
#     "labname": "Central Lab",
#     "username" : "centrallab",
#     "password":"pass@123",
#     "contact": "123-456-7890",
#     "email": "central.lab@example.com",
#     "profile_pic": "path/to/profile_pic.jpg",
#     "latitude": 37.7749,
#     "longitude": -122.4194,
#     "address": "123 Main Street",
#     "city": "San Francisco",
#     "state": "California",
#     "pincode": "94103"
# }


class ObtainSuperuserToken(APIView):
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
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
    permission_classes=[IsAuthenticated, IsLab]
    authentication_classes=[TokenAuthentication]
    queryset=Package.objects.all()
    serializer_class=PackageSerializers

    def get_queryset(self):
        # Filter packages based on the logged-in user's lab
        user = self.request.user
        if user.is_lab:
            return Package.objects.filter(lab_name=user)
        return Package.objects.none()

# GET lab/tests/: List all tests.
# POST lab/tests/: Create a new test.
# GET lab/tests/{id}/: Retrieve a specific test by ID.
# PUT lab/tests/{id}/: Update a specific test by ID.
# PATCH lab/tests/{id}/: Partially update a specific test by ID.
# DELETE lab/tests/{id}/: Delete a specific test by ID.
   
class TestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TestSerializers

    def get_queryset(self):
        # Filter tests based on the logged-in user's lab
        user = self.request.user
        if user.is_lab:
            return Test.objects.filter(lab=user)
        return Test.objects.none()


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

    def get_queryset(self):
        # Filter docotors based on the logged-in user's lab
        user = self.request.user
        if user.is_lab:
            return Doctor.objects.filter(lab=user)
        return Doctor.objects.none()


# GET lab/timeslot/: List all timeslots.
# POST lab/timeslot/: Create a new timeslot.
# GET lab/timeslot/{id}/: Retrieve a specific timeslot by ID.
# PUT lab/timeslot/{id}/: Update a specific timeslot by ID.
# PATCH lab/timeslot/{id}/: Partially update a specific timeslot by ID.
# DELETE lab/timelsot/{id}/: Delete a specific timeslot by ID

class TimeSlotViewSet(viewsets.ModelViewSet) :
    permission_classes = [IsAuthenticated, IsLab]
    authentication_classes = [TokenAuthentication]
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerilaizer
    
    def get_queryset(self):
        # Filter timeslots based on the logged-in user's lab
        user = self.request.user
        if user.is_lab:
            return TimeSlot.objects.filter(lab=user)
        return TimeSlot.objects.none()

class TestResultAPIView(APIView) :
    permission_classes = [IsAuthenticated, IsLab]
    authentication_classes = [TokenAuthentication]

    def post(self, request, format = None) :
        serializer = TestResultSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestReviewReplyAPIView(APIView) :
    permission_classes = [IsAuthenticated, IsLab]
    authentication_classes = [TokenAuthentication]

    def get(self, request, test_id, format=None) :
        reviews = TestReview.objects.filter(test_id=test_id)
        serializer = TestReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, testreview_id, format=None):
        try:
            review = TestReview.objects.get(pk=testreview_id)
        except TestReview.DoesNotExist:
            return Response({'detail': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        data['review'] = testreview_id
        serializer = TestReviewReplySerializer(data=data)

        if serializer.is_valid():
            serializer.save(lab_admin=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AllReservationAPIView(APIView) :
    permission_classes = [AllowAny]

    def get(self, request, lab_id) :
        try :
            lab = UserManage.objects.get(id=lab_id, is_lab=True)
        except UserManage.DoesNotExist :
            return Response({'details' : 'No lab Found'}, status= status.HTTP_404_NOT_FOUND)
        
        reservation = Reservation.objects.filter(lab=lab)
        serializer = ReservationSerializer(reservation, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReservationStatusAPIView(APIView) :
    permission_classes = [IsAuthenticated, IsLab]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, pk, format=None) :
        try :
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist :
            return Response({'details' : 'No reservation found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReservationStatusSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FeedbackAPIView(APIView) :
    permission_classes = [IsAuthenticated, IsLab]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None) :
        user = request.user
        feedback = LabReview.objects.filter(lab=user).order_by('-created_at')
        serializer = LabReviewSerializer(feedback, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


