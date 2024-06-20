from rest_framework import serializers
from labs.models import UserManage

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserManage
        fields = ['email', 'contact', 'profile_pic', 'address', 'city', 'state', 'pincode','name']
        
    def create(self, validated_data):
        user = UserManage.objects.create_user(username=validated_data['email'],**validated_data)
        user.is_customer = True
        user.save()
        return user
