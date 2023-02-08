from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import uuid
from django.utils import timezone
from micro_auth_service.models import BusinessUsers
from micro_auth_service.authorization import Verify
from micro_brandCategoryProduct_service.models import ProductCategory,Brand
import json
from VerifyAccess.access import verifyAccess
from decouple import config

ACCESSED_BY=config('Manufacturer')

def isCategoryExists(category_name):
    try:
        if(ProductCategory.objects.filter(category_name=category_name).exists()):
            return True
        else:
            return False
    except:
        pass


def get_categoriesOfaBrand(brand):
    try:
        category=[]
        if(ProductCategory.objects.filter(brand=brand).exists()):
            obj=ProductCategory.objects.filter(brand=brand)
            for cat in range(0,obj.count()):
                data={
                    "category_id":obj.values('category_id')[cat]['category_id'],
                    "category_name":obj.values('category_name')[cat]['category_name'],
                    "desc":obj.values('desc')[cat]['desc']
                }
                category.append(data)
            return category

        else:
            return category
    except:
        pass


@api_view(['GET'])
def get_categories(request,userid,brandid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            user=BusinessUsers.objects.get(uid=userid)
            brand=Brand.objects.get(brand_id=brandid)
            if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid and brand.user==user):
                data=get_categoriesOfaBrand(brand)              
                return Response({"data":data},status=status.HTTP_200_OK)
            else:
                return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            pass
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 



@api_view(['POST'])
def create_category(request,userid,brandid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid):
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                category_name=(body['category_name']).upper()
                category_desc=body['category_desc']
                if(not isCategoryExists(category_name=category_name)):
                    user=BusinessUsers.objects.get(uid=userid)
                    brand=Brand.objects.filter(user=user).get(brand_id=brandid)
                    print(brandid,brand)
                    ID=uuid.uuid4()
                    b=ProductCategory(brand=brand,category_id=ID,category_name=category_name,desc=category_desc,created_at=timezone.now())
                    b.save()
                    data={
                        "category_id":ID,
                        "category_name":category_name,
                        "desc":category_desc
                    }
                    return Response({"info":"created!!!","data":data},status=status.HTTP_201_CREATED)
                else:
                    return Response({"info":"category already exists!"},status=status.HTTP_409_CONFLICT)
            else:
                return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        except:             
            pass
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
def  update_category(request,userid,categoryid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            user=BusinessUsers.objects.get(uid=userid)
            category=ProductCategory.objects.get(category_id=categoryid)
            if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid and category.brand.user==user):
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)  
                if(body.__contains__('category_name')):
                    category.category_name=body['category_name'].upper()
                elif(body.__contains__('category_desc')):
                    category.desc=body['category_desc']
                elif(body.__contains__('category_name') and body.__contains__('category_desc')):
                    category.category_name=body['category_name'].upper()
                    category.desc=body['category_desc']
                category.save()     
                return Response({"info":"updated!!!"},status=status.HTTP_201_CREATED)
        except:
            pass
        else:
            return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
             
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_category(request,userid,categoryid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            user=BusinessUsers.objects.get(uid=userid)
            category=ProductCategory.objects.get(category_id=categoryid)
            if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid and category.brand.user==user):
                category.delete()    
                return Response({"info":"deleted!!!"},status=status.HTTP_201_CREATED)
        except:
            pass
        else:
            return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
             
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)