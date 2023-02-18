from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import uuid
from micro_auth_service.models import BusinessUsers
from Authorization.authorization import Verify
from micro_brandCategoryProduct_service.models import Product,Brand,ProductCategory
from .models import Production
import json
from VerifyAccess.access import verifyAccess
from decouple import config
from datetime import datetime

ACCESSED_BY=config('Manufacturer')


@api_view(['PATCH'])
def update_production(request,userid,productid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            user=BusinessUsers.objects.get(uid=userid)
            product=Product.objects.get(product_id=productid)
            if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid and product.category.brand.user==user):
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)  
                production_rate=body['production_rate']
                currentDate=datetime.today().strftime('%Y-%m-%d')
                if(Production.objects.filter(production_date=currentDate,product=product).exists()):
                    obj=Production.objects.filter(production_date=currentDate,product=product)
                    pre_production_rate=obj.values('production_rate')[0]['production_rate']
                    obj.update(production_rate=int(pre_production_rate)+int(production_rate))
                    return Response({"info":"production updated!!!"},status=status.HTTP_200_OK)
                else:
                    p=Production(product=product,production_id=uuid.uuid4(),production_rate=production_rate,production_date=currentDate)
                    p.save()
                    return Response({"info":f"new production added for today {currentDate} !!!"},status=status.HTTP_201_CREATED)
        except:
            pass
        else:
            return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
             
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_a_single_production(product):
    try:
        production=[]
        if(Production.objects.filter(product=product).exists()):
            obj=Production.objects.filter(product=product)
            for p in range(0,obj.count()):
                data={
                    "product_name":(Product.objects.get(product_id=obj.values('product')[p]['product'])).name,
                    "production_id":obj.values('production_id')[p]['production_id'],
                    "production_rate":obj.values('production_rate')[p]['production_rate'],
                    "production_date":obj.values('production_date')[p]['production_date']
                }
                production.append(data)
            return production
        else:
            return production
    except:
        pass

@api_view(['GET'])
def get_total_production_of_a_product(request,userid,productid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            user=BusinessUsers.objects.get(uid=userid)
            product=Product.objects.get(product_id=productid)
            if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid and product.category.brand.user==user):
                data=get_a_single_production(product)
                return Response({"data":data},status=status.HTTP_200_OK)
        except:
            pass
        else:
            return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
             
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def get_a_users_production(user):
    try:
        production=[]    
        product_list=set()

        if(Production.objects.exists()):
            obj=Production.objects.all()
            for i in range(0,obj.count()):  
                if(Product.objects.get(product_id=obj.values('product')[i]['product']).category.brand.user==user):
                    product_list.add(Product.objects.get(product_id=obj.values('product')[i]['product']))
            
            for pro in list(product_list):
                obj_p=Production.objects.filter(product=pro)
                for p in range(0,obj_p.count()):    
                    data={
                        "product_name":(Product.objects.get(product_id=obj_p.values('product')[p]['product'])).name,
                        "production_id":obj_p.values('production_id')[p]['production_id'],
                        "production_rate":obj_p.values('production_rate')[p]['production_rate'],
                        "production_date":obj_p.values('production_date')[p]['production_date']
                    }
                    production.append(data)              

        return production
    except:
        pass

@api_view(['GET'])
def get_total_production_of_a_user(request,userid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            user=BusinessUsers.objects.get(uid=userid)
            if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid):
                data=get_a_users_production(user)
                return Response({"data":data},status=status.HTTP_200_OK)
        except:
            pass
        else:
            return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
             
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def deleteProduction(request,userid,productionid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            user=BusinessUsers.objects.get(uid=userid)
            if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid):
                p=Production.objects.get(production_id=productionid)
                if(p.product.category.brand.user==user):
                    p.delete()
                return Response({"info":"deleted!!!"},status=status.HTTP_200_OK)
        except:
            pass
        else:
            return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
             
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)