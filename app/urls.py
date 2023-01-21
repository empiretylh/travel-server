from django.urls import path, include

# from app.models import SalesTwoDigits
from . import views
from . import apiview
from django.conf.urls.static import static
from django.conf import settings


from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
   


    path('auth/login/', obtain_auth_token, name='auth_user_login'),
    path('auth/register/', apiview.CreateUserApiView.as_view(),
         name='auth_user_create'), 

    path('api/packageadmin/',apiview.PackageAdmin,name='packageadmin'),
     path('api/packagedescription/',apiview.PackageDescriptionAdmin,name='description'),
      path('api/includeplaces/',apiview.IncludePlace,name='includeplace'),
       path('api/adminbooking/',apiview.AdminBookingView,name='adminbooking'),
        path('api/clientbooking/',apiview.ClientBooking,name='clientbooking')

  

    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
