from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password,check_password
from Authorization.authorization import Verify
from Jwt.jwtToken import JWT_Builder
import json
from django.contrib.auth.hashers import check_password,make_password
from .models import BusinessUsers,RefreshToken,Role,OTP
from rest_framework import status
import uuid
from EmailServer.emails import OtpDuringRegister
from django.utils import timezone
from datetime import datetime


def saveRefreshToken(token,user):
    try:
        x=RefreshToken(user=user,refresh_token=token)
        x.save()
    except:
        pass

def validate_Email_and_Phone(email,phone):
    try:
        if BusinessUsers.objects.filter(email=email).exists() or BusinessUsers.objects.filter(phone=phone).exists():
            return False
        else:
            return True
    except:
        pass


@api_view(['POST'])
def Login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email=body['email']
    password=body['password']
    if email and password and len(body)==2:
        if BusinessUsers.objects.filter(email=email,otp_verified=True).exists() and check_password(password,BusinessUsers.objects.filter(email=email).values('password')[0]['password']):
            ID=BusinessUsers.objects.filter(email=email).values('uid')[0]['uid']
            user=BusinessUsers.objects.get(uid=ID)
            tokens=JWT_Builder({"userid":ID,"role":Role.objects.get(user=user).role}).get_token()
            token_pair={"access_token":tokens['access_token'],"refresh_token":tokens['refresh_token']}            
            saveRefreshToken(tokens['refresh_token'],user)
            return Response(token_pair,status=status.HTTP_200_OK)
    
    info={"info":"invalid credentials!"}
    return Response(info,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def refresh_token(request,userid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        if(RefreshToken.objects.filter(refresh_token=Verify(request).is_Tokenvalid()['token']).exists()):
            try:              
                if BusinessUsers.objects.filter(uid=userid).exists():
                    user=BusinessUsers.objects.get(uid=userid)
                    access_token=JWT_Builder({"userid":userid,"role":Role.objects.get(user=user).role}).get_token()['access_token']
                    refresh_token=JWT_Builder({"userid":userid,"role":Role.objects.get(user=user).role}).get_token()['refresh_token']
                    token={"access_token":access_token,"refresh_token":refresh_token}
                    saveRefreshToken(refresh_token,user)
                    return Response(token,status=status.HTTP_200_OK)
                else:
                    info={"info":"invalid userid"}
                    return Response(info,status=status.HTTP_400_BAD_REQUEST)
            except:
                pass
        else:
            return Response({"info":"Something wrong!"},status=status.HTTP_400_BAD_REQUEST)
        
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def saveUsers(user,role):   
    user.save()
    Role.objects.create(user=user,role=role)

@api_view(['POST'])
def register(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email=body['email']
    password=body['password']
    phone=body['phone']
    role=body['role']
    name=body['name']
    if len(body)==5 and (role in ['Manufacturer','WholeSaler','Retailer']):     
        if not validate_Email_and_Phone(email,phone):
            return Response({"info":"Already exists"},status=status.HTTP_409_CONFLICT)
        else:
            try:
                ID=uuid.uuid4()
                user=BusinessUsers(uid=ID,name=name,email=email,phone=phone,password=make_password(password),otp_verified=False,created_at=timezone.now())
                saveUsers(user,role)
                OtpDuringRegister(email,name,user)
                return Response({"info":"otp sent!"},status=status.HTTP_200_OK)
            except:
                return Response({"info":"Something went wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"info":"Bad request!"},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def OtpVerify(request,email):
    if not email:
        return Response({"missing credentials!"},status=status.HTTP_406_NOT_ACCEPTABLE)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    otp=body['otp']
    if(BusinessUsers.objects.filter(email=email,otp_verified=False)).exists():
        ID=BusinessUsers.objects.filter(email=email).values('uid')[0]['uid']
        user=BusinessUsers.objects.get(uid=ID)
        if(OTP.objects.filter(user=user).exists() and int(OTP.objects.filter(user=user).values('otp')[0]['otp'])==int(otp)):
            try:
                currentTimestamp=datetime.timestamp(datetime.now())
                if(float(OTP.objects.filter(user=user).values('expiry')[0]['expiry'])>=currentTimestamp):
                    OTP.objects.filter(user=user).delete()
                    user.otp_verified=True
                    user.save()
                    return Response({"info":"created!!!"},status=status.HTTP_201_CREATED)
                else:
                    OTP.objects.filter(user=user).delete()
                    user.delete()
                    return Response({"info":"expired otp, register again!!!"},status=status.HTTP_403_FORBIDDEN)
            except:
                return Response({"info":"Something went wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"wrong credentials!"},status=status.HTTP_404_NOT_FOUND)
