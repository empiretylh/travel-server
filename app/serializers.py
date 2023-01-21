from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

from django.utils import timezone

class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ['name', 'username', 'email', 'phoneno', 'password']
        write_only_fields = ('password')

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.start_d = timezone.now()
        user.end_d = timezone.now()
        user.save()

        return user



class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Package  
        fields = ['id','destination','image','cost','duration','description']



class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IncludePlace  
        fields = ['id','placename','hotels','lengthofstay','image']

        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking 
        fields = ['id','travelcode','package','traveler','travel_sdate','cost','paid','is_halfpaid','is_fullpaid','is_finish','is_call','booking_date']