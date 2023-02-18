from django.core.mail import send_mail
from micro_auth_service.models import OTP
from random import randint
from threading import Thread
from datetime import datetime,timedelta

def saveotp(otp,user):
    try:
        x=OTP(user=user,otp=otp,expiry=datetime.timestamp(datetime.now()+timedelta(minutes=3)))
        x.save()
    except:
         pass


def OtpDuringRegister(email,name,user):
        otp=randint(1111,9999)
        subject='Welcome To Our Service'
        body=f'{name}, Your Business account is almost ready. Please verify your account with OTP : {otp} within 3 minutes!'
        mail_sender = 'utsav.cha@bedigit.in'
        try:
            t1=Thread(target=saveotp,args=[otp,user,])
            t2=Thread(target=send_mail,args=[subject,body,mail_sender,[email],False,])
            t1.start()
            t2.start()
        except:
            pass
        return
 