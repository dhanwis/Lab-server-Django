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
    
# class UserSerializer(serializers.ModelSerializer):
#     class Meta: 
#         model = User
#         fields = ['id', 'username', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         # validated_data['is_user'] = True 
#         user = User.objects.create_user(**validated_data)
#         user.save()
        
#         return user
        
        
        

        
        
        
        