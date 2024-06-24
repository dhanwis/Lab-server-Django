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
    time_slot = serializers.PrimaryKeyRelatedField(queryset=TimeSlot.objects.all())
    test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all())
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    status=serializers.ChoiceField()
    
    class Meta:
        model = Reservation
        fields = [ 'lab', 'client', 'time_slot', 'test', 'reservation_date',"status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the default value for the client field to the current user
        if 'context' in kwargs and 'request' in kwargs['context']:
            user = kwargs['context']['request'].user
            self.fields['client'].default = user.id
            
            