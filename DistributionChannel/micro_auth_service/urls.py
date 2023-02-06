from django.urls import path
from .views import *

urlpatterns = [
    path('login',Login),
    path(r'refresh_token/userid=<str:userid>',refresh_token),
    path('register',register),
    path('otpverify/email=<str:email>',OtpVerify)
]
