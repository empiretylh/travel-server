from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

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


User = get_user_model()


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise ValidationError('Invalid email address')
        return user.email
    
    class Meta:
        model = User
        fields = ['email']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id','name','username','email','phoneno','password','is_admin','profileimage','address']

        

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

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentInfo
        fields = ['ReceiverName','ReceiverPhoneno','SenderName','SenderPhoneno','Operator','Amount']


class BookingSerializer(serializers.ModelSerializer):
    
    traveler = serializers.CharField(source='traveler.name')
    idcardno = serializers.CharField(source='traveler.idcardno')
    travelerid = serializers.CharField(source='traveler.id')
    package = serializers.CharField(source='package.destination')
    departuredt = serializers.CharField(source='package.travel_sdate')
    paymentinfo = PaymentSerializer(read_only=True)

    class Meta:
        model = models.Booking
        fields = ['id', 'travelcode','cost','departuredt',
                  'paid', 'is_halfpaid', 'is_fullpaid', 'is_finish','is_cancel',
                  'paymentinfo','booking_date','traveler','package',
                  'travelerid','idcardno']


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model =  models.CompanyInformation 
        fields = ['id','companyname','phoneno','email','companyaddress','image']