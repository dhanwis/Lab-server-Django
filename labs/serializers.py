from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManage
        fields = ['labname', 'password', 'contact', 'email', 'latitude', 'longitude', 'address', 'city', 'state', 'profile_pic', 'pincode']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
            password = validated_data.pop('password')
            user = UserManage.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            return user
    
class PackageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields ='__all__'


class TestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields ='__all__'
    

class DoctorsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields ='__all__'
        
        
        

        
        
        
        