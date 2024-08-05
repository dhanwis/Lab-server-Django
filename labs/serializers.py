from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManage
        fields = ['id',"username",'labname', 'password', 'contact', 'email', 'latitude', 'longitude', 'address', 'city', 'state', 'profile_pic', 'pincode']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
            password = validated_data.pop('password')
            user = UserManage.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            return user
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        return representation
    
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
        
class TimeSlotSerilaizer(serializers.ModelSerializer) :
    class Meta:
        model = TimeSlot
        fields = '__all__'        

class TestResultSerializer(serializers.ModelSerializer) :
    class Meta :
        model = TestResult
        fields = '__all__'

class TestReviewReplySerializer(serializers.ModelSerializer) :
    class Meta :
        model = TestReviewReply
        fields = '__all__'


        
        
        
        