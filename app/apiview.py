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
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.authtoken.views import ObtainAuthToken


# A Python program to demonstrate working of OrderedDict
from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone






from . import models, serializers

import json
    



def CHECK_IN_PLAN_AND_RESPONSE(user, data, **args):
    if user.is_plan:
        return Response('End Plan or No Purchase Plan')
    else:
        return Response(data=data, **args)

    print('User is in Plan')


class UserChangePasswordView(APIView):

    def put(self, request):
        newpassword = request.data['new_password']
        print(request.data)
        if 'old_password' in request.data:
            user = authenticate(request, username=request.user.username, password=request.data['old_password'])
        else:
            user = models.User.objects.get(username=request.user)
        if user is not None:
            user.set_password(newpassword)
            user.save()
            return Response({'message':'Password Change Success'},status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Invalid old password'}, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordView(APIView):
    serializer_class = serializers.ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = models.User.objects.get(email=serializer.validated_data['email'])
        token, created = Token.objects.get_or_create(user=user)
        
        email = request.data['email']

        subject = 'TMT Agency Account Reset Password'


        CI = models.CompanyInformation.objects.last()

        html_content = '''<html>
<head>
   
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">


<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

<script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
<style>
 .reset-password-btn {
 text-decoration:none;
  background-color: blue;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

.reset-password-btn:hover {
  background-color: darkblue;
}
In this code, the background-color property sets the background color of the button to blue, while the color property sets the text color to white. The border, border-radius, and padding properties are used to style the button, while the `font-size




</style>
</head>
<body>
  <div>
      <p> <strong>Dear '''+user.name+'''</strong>, <br/><br/>
        We have received a request to rest the password associated with your account. To proceed with resetting your password, please click on the "Rest Password" button bellow. This will take you to a secure page where you can enter a new password for your account.
         <br/>
           <br/>
        Company : '''+CI.companyname+'''<br/>
        Call Center : <a href="tel:'''+CI.phoneno+'''">'''+CI.phoneno+'''</a><br/>
        Email : '''+CI.email+'''<br/>
        Company Address : '''+CI.companyaddress+'''<br/>
    </p>  
    </div>
<div class='container'>
<a class='reset-password-btn' href="https://tmtagency.github.io/travel/#/restpassword/'''+str(token)+'''">
Reset Password
</a>
<p>
If you are unable to clck on the button below, please copy and paste the following URL into your web browser:<br/>
 https://tmtagency.github.io/travel/#/restpassword/'''+str(token)+'''<br/>
</p>
</div>
</body>
</html>
        '''        


        SENDEMAIL = EmailMessage(subject, html_content, 'traveleragencymm@gmail.com', [
                                 email], headers={'Message-ID': user.id})
        SENDEMAIL.content_subtype = "html"
        SENDEMAIL.send()
        # TODO: Send the password reset link to the user's email address
        # email = ...
        # send_email(email, uid, token)

        return Response({'detail': 'Password reset link has been sent to your email address.'}, status=status.HTTP_200_OK)


class LoginView(APIView):

    permission_classes = [AllowAny]


    def post(self, request, *args, **kwargs):
      
        print(request.data)

        username_or_email = request.data['username']
        password = request.data['password']

        user = None
        if '@' in username_or_email:
            b = models.User.objects.get(email=username_or_email)
            user = authenticate(username=b.username, password=password)
        else:
            user = authenticate(username=username_or_email, password=password)


        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)



        # add custom data to response
        response_data = {
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            # add additional data fields here as needed
        }
        return Response(response_data)

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


class UserApiView(APIView):

    permission_classes = [AllowAny]

    def get(self,request):
        types = request.GET.get('type')
        user = models.User.objects.get(username=request.user)
        if types == 'all':
            users = models.User.objects.all()
            ser = serializers.UserSerializer(users,many=True)
        else:
            users = user
            ser = serializers.UserSerializer(users)
        

        return Response(ser.data)

    def put(self,request):
      name = request.data['name']
      email = request.data['email']
      phoneno = request.data['phoneno']
      address = request.data['address']
      user = models.User.objects.get(username=request.user)
      user.name = name 
      user.email = email 
      user.phoneno = phoneno 
      user.address = address 
      user.save()

      return Response(1)

    def delete(self,request):
        models.User.objects.get(username=request.user)
        userid = request.GET.get('id')
        user = models.User.objects.get(id=userid)
        user.delete()
        return Response(1)


class PackageAdmin(APIView):

    # destination(str),image(file),cost(str),duration(str)

    permission_classes = [AllowAny]

    def post(self, request):
        user = models.User.objects.get(username=request.user)
        destination = request.data['destination']
        image = request.data['image']
        cost = request.data['cost']
        duration = request.data['duration']
        people_limit = request.data['people_limit']
        travel_sdate = request.data['travel_sdate']
        discount = request.data['discount']

        package = models.Package.objects.create(
            user=user, destination=destination, image=image, cost=cost, duration=duration, people_limit=people_limit, travel_sdate=travel_sdate)
    
        if discount:
          package.discount = discount

        package.save()
        return Response(status=status.HTTP_201_CREATED)

    # return all data
    def get(self, request, format=None):

        package = models.Package.objects.all()
        ser = serializers.PackageSerializer(package, many=True)

        return Response(ser.data)

    def put(self, request):
        print(request.data)
        user = models.User.objects.get(username=request.user)
        packageid = request.data['packageid']
        destination = request.data['destination']
        image = request.data['image']
        cost = request.data['cost']
        duration = request.data['duration']
        people_limit = request.data['people_limit']
        travel_sdate = request.data['travel_sdate']
        discount = request.data['discount']

        package = models.Package.objects.get(id=packageid)
        package.destination = destination
        if discount:
          package.discount = discount
      
        if image:
            package.image = image

        package.cost = cost
        package.duration = duration
        package.people_limit = people_limit
        package.travel_sdate = travel_sdate
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
        package = models.Package.objects.get(id=packageid)
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

    def get(self, request):

        type = request.GET.get('type')
        if type == 'finish':
            booking = models.Booking.objects.filter(is_finish=True)
        elif type == 'unfinish':
            booking = models.Booking.objects.filter(is_finish=False)
        else:
            print('all data')
            booking = models.Booking.objects.all()
        ser = serializers.BookingSerializer(booking, many=True)

        return Response(ser.data)

    def put(self, request):
        bookingid = request.data['bookingid']

        booking = models.Booking.objects.get(id=bookingid)
        print(request.data)
        if "prepaid" in request.data:
            prepaid = request.data['prepaid']
            booking.is_halfpaid = prepaid
            if prepaid:
                booking.paid = int(float(booking.cost) / 2)
            else:
                booking.paid = int(float(booking.paid) -
                                   (float(booking.cost) / 2))

        if "fullpaid" in request.data:
            fullpaid = request.data['fullpaid']
            booking.is_fullpaid = fullpaid
            if fullpaid:
                booking.paid = booking.cost
            else:
                booking.paid = int(float(booking.paid) -
                                   (float(booking.cost) / 2))

        if "is_finish" in request.data:
            is_finish = request.data['is_finish']
            booking.is_finish = is_finish

        if "cancel" in request.data:
            cancel = request.data['cancel']
            booking.is_cancel = cancel

        booking.save()

        return Response(status=status.HTTP_201_CREATED)


    def delete(self, request):
        bookingid = request.GET.get('bookingid')

        booking = models.Booking.objects.get(id=bookingid)
        booking.delete()

        return Response(status=status.HTTP_201_CREATED)


class TravelerView(APIView):

    def get(self, request):
        travelerid = request.GET.get('travelerid')
        if int(travelerid) > 0:
            Traveler = models.Traveler.objects.get(id=travelerid)
            ser = serializers.TravelerSerializer(Traveler)

            return Response(ser.data)
        return Response(0)


class ClientBooking(APIView):

    

    def post(self, request):
        print(request.data)
        user = models.User.objects.get(username=request.user)

        rname = request.data['receivername']
        rphone = request.data['receiverphoneno']
        sname = request.data['sendername']
        sphone = request.data['senderphoneno']
        amount = request.data['amount']
        operator = request.data['operator']


        pi =  models.PaymentInfo.objects.create(ReceiverName=rname,ReceiverPhoneno=rphone,

            SenderName=sname,SenderPhoneno=sphone,Amount=amount,Operator=operator)

        name = request.data['name']
        phoneno = request.data['phoneno']
        email = request.data['email']
        idcardno = request.data['idcardno']
        address = request.data['address']

        packageid = request.data['package_id']
        package = models.Package.objects.get(id=packageid)

        pserializer = serializers.PackageSerializer(package)

        paidtype = request.data['paidtype']


        traveler = models.Traveler.objects.create(
            name=name,
            phoneno=phoneno,
            email=email,
            idcardno=idcardno,address=address)

        booking = models.Booking.objects.create(
            paymentinfo=pi,
            package=package,
            traveler=traveler,
            cost=package.cost, is_finish=False,
          user=user
            )

        
        if paidtype == 'prepaid':
          booking.paid = int(package.cost) /2
          booking.is_halfpaid = True
        else:
          booking.paid = package.cost
          booking.is_halfpaid = True 
          booking.is_fullpaid = True


        booking.travelcode = booking.id + 1000

        booking.save()

        package.people_limit = package.people_limit - 1
        package.save()

        ser = serializers.BookingSerializer(booking)

        startdate = package.travel_sdate.strftime('%Y-%m-%d')
        starttime = package.travel_sdate.strftime('%I:%M %p')

        placename = ''
        # print(pserializer.data['includeplace'][])
        for value in pserializer.data['includeplace']:
            placename += value['placename']+','

        print(placename)
    
        placename += package.destination

        CI = models.CompanyInformation.objects.last()

        # Sending Email ..............
        subject = 'Travel Reservation'
        html_content = '''<html>
<head>
   
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">


<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

<script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
<style>
    
body{
  font-family:"Arial, Helvetica, sans-serif"
}
table tbody tr th{
  text-align: "center";
  height: 50px;
}

table, td, th {
border: 1px solid black;
padding: 8px;
font-size: large;
font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif
}

th {
background-color:  rgb(26, 44, 68);
color: white;
}
table {
border-collapse: collapse;
width: 100%;
height:100px;
}

td {
text-align: center;
}

p{
font-size: larger;
}
</style>
</head>
<body>
<div>
    <div>
      <p> <strong>Dear '''+name+'''</strong>, <br/><br/>
        At the request of the ticket holder, the booking below has been sent to you.<br/>
        The following message is included at the sender's request <br/>
        We hope you have a pleasant journey.
         <br/>
           <br/>
        Company : '''+CI.companyname+'''<br/>
        Call Center : <a href="tel:'''+CI.phoneno+'''">'''+CI.phoneno+'''</a><br/>
        Email : '''+CI.email+'''<br/>
        Company Address : '''+CI.companyaddress+'''<br/>
    </p>  
    </div>
   
<table class="table table-striped table-hover">
        <tbody>
          <tr>
            <th>Travel Code - '''+str(booking.travelcode)+'''</th>
          </tr>
        </tbody>
      </table>
  <div>
    <h3 style="margin-top: 5px">Person Details</h3>
    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <tbody>
          <tr>
            <th>Name</th>
            <td style="text-align: left">'''+traveler.name+'''</td>
          </tr>
            <tr>
            <th>NRC No</th>
             <td style="text-align: left">'''+traveler.idcardno+'''</td>
            </tr>
            <tr>
            <th>Phone No</th>
              <td style="text-align: left">'''+traveler.phoneno+'''</td>
            </tr>
            <tr>
            <th>Email</th>
              <td style="text-align: left">'''+traveler.email+'''</td>
            </tr>
            <tr>
            <th>Address</th>
              <td style="text-align: left">'''+traveler.address+'''</td>
            </tr>
          </tr>
        </tbody>
      </table>
    </div>
    <h3 style="display: flex;margin-top: 10px">
      Package Details
    </h3>
    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <tbody>
          <tr>
            <th>Destination</th>
            <th>Departure Date</th>
            <th>Departure Time</th>
            <th>Include Places</th>
          </tr>
          <tr>
            <td style="text-align: center">'''+package.destination+'''</td>
            <td style="text-align: center">'''+startdate+'''</td>
            <td style="text-align: center">'''+starttime+'''</td>
            <td style="text-align: center">'''+placename+'''</td>
          </tr>
        </tbody>
      </table>
    </div>
    <h3 style="margin-top: 10px">Pricing Details</h3>
    <div class="table-responsive">
      <table class="table table-striped table-hover" style="position: relative">
        <tbody>
          <tr>
            <th>Package Costs</th>
            <th>Paid</th>
            <th>Balance</th>
          </tr>
          <tr>
            <td style="text-align: center">'''+str(booking.cost)+''' Ks</td>
            <td style="text-align: center">'''+str(booking.paid)+''' Ks</td>
            <td style="text-align: center">'''+str(int(float(booking.cost) - float(booking.paid)))+''' Ks</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
</body>
</html>
        '''
        SENDEMAIL = EmailMessage(subject, html_content, 'traveleragencymm@gmail.com', [
                                 email], headers={'Message-ID': booking.id})
        SENDEMAIL.content_subtype = "html"
        SENDEMAIL.send()
        # send_mail(package.destination,
        # 'Your Booked This Package',
        # 'traveleragencymm@gmail.com'
        # ,[email],fail_silently=False)

        return Response(ser.data, status=status.HTTP_201_CREATED)

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


class FeedBackView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        star = request.data['star']
        packageid = request.data['packageid']

        feedback = models.FeedBack.objects.create(
            star=star, package_id=packageid)

        if 'message' in request.data:
            message = request.data['message']
            feedback.message = message
            feedback.save()

        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):

        type = request.GET.get('type')

        if type == 'one':
            packageid = request.data['packageid']
            feedback = models.FeedBack.objects.filter(package_id=packageid)
        else:
            feedback = models.FeedBack.objects.all()

        ser = serializers.FeedBackSerializer(feedback, many=True)

        return Response(ser.data)

    def delete(self, request):
        user = models.User.objects.get(username=request.user)
        feedbackid = request.GET.get('feedbackid')

        feedback = models.FeedBack.objects.get(id=feedbackid)

        feedback.delete()

        return Response(status=status.HTTP_201_CREATED)


class CompanyInfoView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        CI = models.CompanyInformation.objects.last()
        SCI = serializers.CompanyInfoSerializer(CI)

        return Response(SCI.data)

    def post(self, request):
        user = models.User.objects.get(username=request.user)
        companyname = request.data['companyname']
        phoneno = request.data['phoneno']
        email = request.data['email']
        address = request.data['address']

        try:
            CI = models.CompanyInformation.objects.last()
            CI.companyname = companyname
            CI.phoneno = phoneno
            CI.email = email
            CI.companyaddress = address

        except ObjectDoesNotExist:
            CI = models.CompanyInformation.objects.create(
                companyname=companyname,
                phoneno=phoneno,
                email=email,
                companyaddress=address)

        image = request.data['image']

        if image:
            CI.image = image

        CI.save()

        return Response(status=status.HTTP_201_CREATED)


class PackageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):

        pkid = request.GET.get('pkid')

        package = models.Package.objects.get(id=pkid)
        ser = serializers.PackageSerializer(package)

        return Response(ser.data)

import json

class CheckCode(APIView):
  permission_classes = [AllowAny]

  def get(self,request,format=None):
    
    travelcode = request.GET.get('travelcode')
    print(travelcode,'LRERTERRR')
    c = json.loads(travelcode)

    booking = models.Booking.objects.filter(travelcode__in=c)
    ser = serializers.BookingSerializer(booking,many=True)
    
    return Response(ser.data)  