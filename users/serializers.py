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
    # status=serializers.ChoiceField()
    
    class Meta:
        model = Reservation
        fields = [ 'lab', 'client', 'time_slot', 'test', 'reservation_date', 'status']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['client'] = user  # Set the client field to the current user
        return super().create(validated_data)

class TestReviewSerializer(serializers.ModelSerializer) :
    class Meta :
        model = TestReview
        fields = '__all__'
            
            