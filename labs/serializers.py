from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManage
        fields = '__all__'
        
        
    def create(self, validated_data):
        user = UserManage.objects.create_user(**validated_data)
        user.save()
        return user
    
   
        
        
        

        
        
        
        