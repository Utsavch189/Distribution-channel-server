from django.core.mail import send_mail
from AuthProvider.models import OTP
from random import randint
from django.utils import timezone
from threading import Thread

def saveotp(otp,user):
    if(OTP.objects.filter(user=user).exists()):
        OTP.objects.filter(user=user).update(otp=otp)
        OTP.objects.filter(user=user).update(created_at=timezone.now())
    else:
        x=OTP(user=user,otp=otp,created_at=timezone.now())
        x.save()

def OtpDuringRegister(email,name,user):

        otp=randint(1111,9999)
        subject='Welcome To Our Service'
        body=f'{name}, Your Business account is almost ready. Please verify your account with OTP : {otp}'
        mail_sender = 'utsavpokemon9000chatterjee@gmail.com'
        try:
            t1=Thread(target=saveotp,args=[otp,user,])
            t2=Thread(target=send_mail,args=[subject,body,mail_sender,[email],False,])
            t1.start()
            t2.start()
            #send_mail(subject, body, mail_sender, [email], fail_silently=False)
        except:
            pass
        return
 