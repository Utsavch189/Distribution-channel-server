from django.db import models
import uuid
from django.utils import timezone

class BusinessUsers(models.Model):
    uid=models.CharField(max_length=50,primary_key=True,default="")
    name=models.CharField(max_length=50,null=True,blank=True)
    email=models.CharField(max_length=50,null=True,blank=True)
    phone=models.CharField(max_length=15,null=True,blank=True)
    password=models.CharField(max_length=555
                              ,null=True,blank=True)
    otp_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(timezone.now())

    def __str__(self):
        return self.name
    
class Role(models.Model):
    user=models.ForeignKey(BusinessUsers,on_delete=models.CASCADE)
    role=models.CharField(max_length=15,null=True,blank=True)

    def __str__(self) -> str:
        return self.role

class OTP(models.Model):
    user=models.OneToOneField(BusinessUsers,on_delete=models.CASCADE,primary_key=True,default="")
    otp=models.CharField(max_length=4,null=True,blank=True)
    expiry=models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.otp

class RefreshToken(models.Model):
    user=models.OneToOneField(BusinessUsers,on_delete=models.CASCADE,primary_key=True,default="")
    refresh_token=models.CharField(max_length=555,null=True,blank=True)

    def __str__(self):
        return str(self.user)

