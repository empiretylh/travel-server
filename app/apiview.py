import operator
import functools
import collections
from collections import OrderedDict
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from django.utils import timezone


from . import models, serializers

import json


def CHECK_IN_PLAN_AND_RESPONSE(user, data, **args):
    if user.is_plan:
        return Response('End Plan or No Purchase Plan')
    else:
        return Response(data=data, **args)

    print('User is in Plan')


class CreateUserApiView(CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = serializers.CreateUserSerializer

    def post(self, request):

        print(request.data)
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        self.perform_create(serializers)
        headers = self.get_success_headers(serializers.data)

        # Create a token than will be used for future auth
        token = Token.objects.create(user=serializers.instance)
        token_data = {'token': token.key}

        return Response(
            {**serializers.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers)


class PackageAdmin(APIView):

    # destination(str),image(file),cost(str),duration(str)

    permission_classes=[AllowAny]

    def post(self, request):
        user = models.User.objects.get(username=request.user)
        destination = request.data['destination']
        image = request.data['image']
        cost = request.data['cost']
        duration = request.data['duration']

        package = models.Package.objects.create(
            user=user, destination=destination, image=image, cost=cost, duration=duration)

        includePlace = models.IncludePlace.objects.create(
            user=user, placename=destination, package=package)

        return Response(status=status.HTTP_201_CREATED)

    # return all data
    def get(self, request,format=None):
        user = models.User.objects.get(username=request.user)
        package = models.Package.objects.all()
        ser = serializers.PackageSerializer(package, many=True)

        return Response(ser.data)

    def put(self, request):
        # print(request.data)
        user = models.User.objects.get(username=request.user)
        packageid = request.data['packageid']
        destination = request.data['destination']
        image = request.data['image']
        cost = request.data['cost']
        duration = request.data['duration']

        package = models.Package.objects.get(id=packageid, user=user)
        package.destination = destination

        print(image)
        if image:
            package.image = image
        package.cost = cost
        package.duration = duration
        package.save()

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = models.User.objects.get(username=request.user)
        packageid = request.GET.get('packageid')

        package = models.Package.objects.get(id=packageid, user=user)
        package.delete()

        return Response(status=status.HTTP_201_CREATED)


class PackageDescriptionAdmin(APIView):
    def put(self, request):
        user = models.User.objects.get(username=request.user)
        packageid = request.data['packageid']
        description = request.data['description']
        package = models.Package.objects.get(user=user, id=packageid)
        package.description = description

        package.save()
        return Response(status=status.HTTP_201_CREATED)


class IncludePlace(APIView):

    def get(self, request):
        user = models.User.objects.get(username=request.user)
        packageid = request.data['packageid']

        ip = models.IncludePlace.objects.filter(package_id=packageid)

        sr = serializers.IncludePlace(ip, many=True)

        return Response(sr.data)

    def post(self, request):
        print(request.data)
        user = models.User.objects.get(username=request.user)
        packageid = request.data['packageid']
        placename = request.data['placename']
        hotels = request.data['hotel']
        lengthofstay = request.data['lengthofstay']
        image = request.data['image']

        ip = models.IncludePlace.objects.create(
            user=user, package_id=packageid, placename=placename, hotels=hotels, lengthofstay=lengthofstay)

        if image:
            ip.image = image

        ip.save()

        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, format=None):
        user = models.User.objects.get(username=request.user)
        ipid = request.data['includeplaceid']
        packageid = request.data['packageid']
        placename = request.data['placename']
        hotels = request.data['hotels']
        lengthofstay = request.data['lengthofstay']
        image = request.data['image']

        ip = models.IncludePlace.objects.get(
            id=ipid, user=user, package__id=packageid)
        ip.placename = placename
        ip.hotels = hotels
        ip.lengthofstay = lengthofstay
        ip.image = image

        ip.save()

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        user = models.User.objects.get(username=request.user)
        ipid = request.GET.get('includeplaceid')

        ip = models.IncludePlace.objects.get(id=ipid, user=user)

        ip.delete()

        return Response(status=status.HTTP_201_CREATED)


class AdminBookingView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        type = request.GET.get('type')
        if type == 'finish':
            booking = models.Booking.objects.filter(is_finish=True)
        elif type == 'unfinish':
            booking = models.Booking.objects.filter(is_finish=False)
        else:
            booking = models.Booking.objects.all()
        ser = serializers.BookingSerializer(booking, many=True)

        return Response(ser.data)

    def put(self, request):
        travelcode = request.data['travelcode']
        paid = request.data['paid']

        booking = models.Booking.objects.get(travelcode=travelcode)
        is_halfpaid = booking.cost / 2 <= paid
        is_fullpaid = booking.cost <= paid
        booking.is_halfpaid = is_halfpaid
        booking.is_fullpaid = is_fullpaid
        booking.save()

        return Response(status=status.HTTP_201_CREATED)


class ClientBooking(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data['name']
        phoneno = request.data['phoneno']
        email = request.data['email']
        idcardno = request.data['idcardno']

        packageid = request.data['package_id']
        package = models.Package.objects.get(id=packageid)
        is_call = request.data['is_call']

        if 'paid' in request.data:
            paid = request.data['paid']

        is_halfpaid = package.cost / 2 <= paid
        is_fullpaid = package.cost <= paid

        traveler = models.Traveler.objects.create(
            name=name,
            phoneno=phoneno,
            email=email,
            idcardno=idcardno)

        booking = models.Booking.objects.create(
            package=package,
            traveler=traveler,
            cost=package.cost,
            paid=paid,
            is_fullpaid=is_fullpaid,
            is_halfpaid=is_halfpaid,
            is_call=is_call)

        booking.travelcode = booking.id + 1000

        booking.save()

        return Response(booking.travelcode, status=status.HTTP_201_CREATED)

    def delete(self, request):
        bookingid = request.data['bookingid']

        booking = models.Booking.objects.get(id=bookingid)
        booking.delete()

        return Response(status=status.HTTP_201_CREATED)

    # check Booking from here
    def get(self, request):

        travelcode = request.GET.get('travelcode')
        booking = models.Booking.objects.get(travelcode=travelcode)

        ser = serializers.BookingSerializer(booking, many=True)

        return Response(ser.data)
