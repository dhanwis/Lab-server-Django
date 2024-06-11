from django.shortcuts import render
from rest_framework.decorators import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import * 
# Create your views here.


class LabAdd(APIView):
    def get(self,request,format=None):
        lab = UserManage.objects.all()
        serializer = UserSerializer(lab,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_admin=True)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  
    
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