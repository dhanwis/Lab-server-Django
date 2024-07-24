from django.shortcuts import render
from rest_framework.decorators import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import * 
# import datetime
# from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
# import random
# from .utils import send_otp
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.permissions import AllowAny 
# Create your views here.

#LAB
class LabAdd(APIView):
    def get(self,request,format=None):
        lab = UserManage.objects.filter(is_lab=True)
        serializer = UserSerializer(lab,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        serializer = UserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(is_lab=True)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)  
    
class LabEdit(APIView):
    def get(self,request,format=None,admin_id=None):
        lab=UserManage.objects.get(id=admin_id)
        serializer =UserSerializer(lab)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def patch(self,request,admin_id,format=None):
        lab=UserManage.objects.get(id=admin_id)
        serializer =UserSerializer(lab,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
    
class Login(APIView):
    def post(self, request, format=None):
        data = request.data
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            serializer = UserSerializer(user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"user": serializer.data, "token": token.key}, status=status.HTTP_200_OK)
        return Response({"details": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    

        
