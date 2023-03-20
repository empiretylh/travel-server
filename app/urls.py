from django.urls import path, include

# from app.models import SalesTwoDigits
from . import views
from . import apiview
from django.conf.urls.static import static
from django.conf import settings


from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [



    path('auth/login/', apiview.LoginView.as_view(), name='auth_user_login'),
    path('auth/register/', apiview.CreateUserApiView.as_view(),
         name='auth_user_create'),
    path('auth/changepassword/',apiview.UserChangePasswordView.as_view(),name='changepassword'),
    path('auth/forgotpassword/',apiview.ForgotPasswordView.as_view(),name='forgotpassword'),

    path('api/packageadmin/', apiview.PackageAdmin.as_view(), name='packageadmin'),
    path('api/packagedescription/',
         apiview.PackageDescriptionAdmin.as_view(), name='description'),
    path('api/includeplaces/', apiview.IncludePlace.as_view(), name='includeplace'),
    path('api/adminbooking/', apiview.AdminBookingView.as_view(), name='adminbooking'),
    path('api/traveler/', apiview.TravelerView.as_view(), name='traveler'),
    path('api/clientbooking/', apiview.ClientBooking.as_view(), name='clientbooking'),
    path('api/feedbacks/', apiview.FeedBackView.as_view(), name='feedback'),
    path('api/companyinfo/', apiview.CompanyInfoView.as_view(), name='companyinfo'),
    path('api/checkcode/', apiview.CheckCode.as_view(), name='checkcode'),
    path('api/package/', apiview.PackageView.as_view(), name='package'),
    path('api/user/',apiview.UserApiView.as_view(),name='user'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
