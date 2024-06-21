from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManage
        fields = '__all__' 
        extra_kwargs = {'password': {'write_only': True}}
        
        
    def create(self, validated_data):
        user = UserManage.objects.create_user(**validated_data)
        user.save()
        Token.objects.create(user=user)
        return user
    
class PackageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields ='__all__'


class testSerializers(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields ='__all__'
    

class DoctorsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields ='__all__'
        
        
        

        
        
        
        