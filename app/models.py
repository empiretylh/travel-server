from email.policy import default
from socketserver import ThreadingUnixDatagramServer
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser, Group

from django.core.files.base import ContentFile
# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=255,null=False)
    phoneno = models.CharField(max_length=11, null=True, blank=False)
    
    profileimage = models.ImageField(
        upload_to="img/profile/%y/%mm/%dd", null=True)
    email = models.CharField(max_length=255,null=True)


class Package(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination= models.CharField(max_length=255,null=False,blank=False)
    image = models.ImageField(upload_to='img/place/%y/%mm/%dd',null=True)
    cost = models.CharField(max_length=10,null=False)
    duration = models.CharField(max_length=255,null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.destination


class Traveler(models.Model):
    name = models.CharField(max_length=255,null=False)
    phoneno = models.CharField(max_length=15,null=False)
    email = models.CharField(max_length=255,null=True)
    idcardno = models.CharField(max_length=22,null=True) #14/MaMaNa(N)/xxxxxx

    def __str__(self):
        return self.name

class Booking(models.Model):
    travelcode =  models.CharField(max_length=10)
    package = models.ForeignKey(Package, on_delete=models.CASCADE,related_name='mbooking')
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE,related_name='booking')
    travel_sdate = models.DateTimeField()
    travel_rdate = models.DateTimeField()
    cost = models.CharField(max_length=10,null=False)
    paid = models.CharField(max_length=10,null=False)
    is_halfpaid = models.BooleanField(default=False)
    is_fullpaid = models.BooleanField(default=False)
    is_finish = models.BooleanField(default=True)
    booking_date = models.DateTimeField()

    def __str__(self):
        return self.travelcode + ' ' + self.traveler.name



class IncludePlace(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    placename = models.CharField(max_length=255,null=False)
    package = models.ForeignKey(Package, on_delete=models.CASCADE,related_name='includeplace')
    hotels = models.CharField(max_length=255,null=True,default='No Hotel')
    lengthofstay = models.CharField(max_length=255,null=True)
    image =models.ImageField(upload_to='img/includeplace/%y%mm/%dd',null=True)

    
    def __str__(self):
        return self.placename