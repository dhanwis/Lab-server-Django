from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token

#LAB
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
    
#USER
# class UserSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = UserManage
#         fields = ['email','contact','profile_pic','address','city','state','pincode','name']
        
#     def create(self,validated_data):
#         user = UserManage.objects.create_user(username=validated_data['email'],**validated_data)
#         user.is_customer = True
#         user.save()
#         return user        
        
        

        
        
        
        