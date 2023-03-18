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
        fields = ['name', 'username', 'email', 'phoneno', 'password','is_admin','address']
        write_only_fields = ('password')

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.start_d = timezone.now()
        user.end_d = timezone.now()
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['name','username','email','phoneno','password','is_admin','profileimage','address']

        

class FeedBackSerializer(serializers.ModelSerializer):

    package = serializers.CharField(source='package.destination')

    class Meta:
        model = models.FeedBack
        fields = ['id', 'star', 'message','package']




class IncludePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IncludePlace
        fields = ['id', 'placename', 'hotels', 'lengthofstay', 'image']


class PackageSerializer(serializers.ModelSerializer):

    includeplace = IncludePlaceSerializer(many=True,read_only=True)

    class Meta:
        model = models.Package
        fields = ['id', 'destination', 'image',
                  'cost', 'duration', 'description','people_limit','travel_sdate','includeplace','discount']


class IncludePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IncludePlace
        fields = ['id', 'placename', 'hotels', 'lengthofstay', 'image']


class TravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Traveler
        fields = ['id','name','phoneno','email','idcardno','address']


class BookingSerializer(serializers.ModelSerializer):
    
    traveler = serializers.CharField(source='traveler.name')
    idcardno = serializers.CharField(source='traveler.idcardno')
    travelerid = serializers.CharField(source='traveler.id')
    package = serializers.CharField(source='package.destination')
    departuredt = serializers.CharField(source='package.travel_sdate')
   
    class Meta:
        model = models.Booking
        fields = ['id', 'travelcode','cost','departuredt',
                  'paid', 'is_halfpaid', 'is_fullpaid', 'is_finish', 'booking_date','traveler','package','travelerid','idcardno']


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model =  models.CompanyInformation 
        fields = ['id','companyname','phoneno','email','companyaddress','image']