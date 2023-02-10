from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import uuid
from django.utils import timezone
from micro_auth_service.models import BusinessUsers
from Authorization.authorization import Verify
from micro_brandCategoryProduct_service.models import Brand
import json
from VerifyAccess.access import verifyAccess
from decouple import config

ACCESSED_BY=config('Manufacturer')

def isBrandExists(brand_name):
    try:
        if(Brand.objects.filter(brand_name=brand_name).exists()):
            return True
        else:
            return False
    except:
        pass

def getAllBrands(user):
    try:
        brands=[]
        if(Brand.objects.filter(user=user).exists()):           
            obj=Brand.objects.filter(user=user)
            for brand in range (0,obj.count()):
                data={
                    "brand_id":obj.values('brand_id')[brand]['brand_id'],
                    "brand_name":obj.values('brand_name')[brand]['brand_name'],
                    "brand_desc":obj.values('brand_desc')[brand]['brand_desc']
                }
                brands.append(data)
            return brands
        else:
            return brands
    except:
        pass


@api_view(['POST'])
def create_brand(request,userid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        user=BusinessUsers.objects.get(uid=userid)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        brand_name=(body['brand_name']).upper()
        brand_desc=body['brand_desc']
        if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid):
           if(not isBrandExists(brand_name=brand_name)):
                try:
                    ID=uuid.uuid4()
                    brand=Brand(user=user,brand_id=ID,brand_name=brand_name,brand_desc=brand_desc,created_at=timezone.now())
                    brand.save()
                    data={
                        "brand_id":ID,
                        "brand_name":brand_name,
                        "brand_desc":brand_desc
                    }
                    return Response({"info":"created!!!","data":data},status=status.HTTP_201_CREATED)
                except Exception as e:
                    print(e)
           else:
               return Response({"info":"brand already exists!"},status=status.HTTP_409_CONFLICT)
        else:
            return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def update_brand(request,brand_id,userid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        user=BusinessUsers.objects.get(uid=userid)
        brand=Brand.objects.get(brand_id=brand_id)
        if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid and brand.user==user):
            if(Brand.objects.filter(brand_id=brand_id).exists()):
                try:
                    body_unicode = request.body.decode('utf-8')
                    body = json.loads(body_unicode)
                    if(body.__contains__('brand_name')):                  
                        brand.brand_name=(body['brand_name']).upper()
                    elif(body.__contains__('brand_desc')):
                        brand.brand_desc=body['brand_desc']
                    brand.save()
                    return Response({"info":"updated!"},status=status.HTTP_200_OK)
                except:
                    pass
            else:
                return Response({"info":"bad request!"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_brand(request,brand_id,userid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            brand=Brand.objects.get(brand_id=brand_id)
            user=BusinessUsers.objects.get(uid=userid)
            if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid and brand.user==user):
                if(Brand.objects.filter(brand_id=brand_id).exists()):       
                    brand.delete()
                    return Response({"info":"deleted!"},status=status.HTTP_200_OK)
                else:
                    return Response({"info":"bad request!"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            pass
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['GET'])
def get_brands(request,userid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid):
            try:
                user=BusinessUsers.objects.get(uid=userid)
                data=(getAllBrands(user))
                return Response({"data":data},status=status.HTTP_200_OK)
            except:
                pass
        else:
            return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 