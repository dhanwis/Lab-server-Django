from rest_framework import serializers
from labs.models import *


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserManage
        fields = ['email', 'contact', 'profile_pic', 'address', 'city', 'state', 'pincode','name']
        
    def create(self, validated_data):
        user = UserManage.objects.create_user(username=validated_data['email'],**validated_data)
        user.is_customer = True
        user.save()
        return user




class ReservationSerializer(serializers.ModelSerializer):
    lab = serializers.PrimaryKeyRelatedField(queryset=UserManage.objects.all())
    # client=serializers.PrimaryKeyRelatedField(queryset=Reservation.objects.all())
    time_slot = serializers.PrimaryKeyRelatedField(queryset=TimeSlot.objects.all())
    test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all())
    
    
    
    class Meta:
        model = Reservation
        fields = [ 'lab','time_slot', 'test', 'reservation_date',"status"]
            
            