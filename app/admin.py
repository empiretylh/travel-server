from django.contrib import admin
from . import models
# Register your models here.=
admin.site.register(models.User)
admin.site.register(models.Booking)
admin.site.register(models.Traveler)
admin.site.register(models.Package)
admin.site.register(models.IncludePlace)