from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import uuid
from micro_auth_service.models import BusinessUsers
from Authorization.authorization import Verify
from micro_brandCategoryProduct_service.models import ProductCategory,Product
import json
from VerifyAccess.access import verifyAccess
from decouple import config

ACCESSED_BY=config('Manufacturer')

def isProductExists(product_name):
    try:
        if(Product.objects.filter(name=product_name).exists()):
            return True
        else:
            return False
    except:
        pass

def get_productsOfaCategory(category):
    try:
        products=[]
        if(Product.objects.filter(category=category).exists()):
            obj=Product.objects.filter(category=category)
            for pro in range(0,obj.count()):
                data={
                    "product_id":obj.values('product_id')[pro]['product_id'],
                    "product_name":obj.values('name')[pro]['name'],
                    "product_desc":obj.values('desc')[pro]['desc'],
                    "product_price":obj.values('price')[pro]['price'],
                    "product_mfg_date":obj.values("mfg_date")[pro]["mfg_date"],
                    "product_expiry_date":obj.values("expiry_date")[pro]["expiry_date"]
                }
                products.append(data)
            return products

        else:
            return products
    except:
        pass

@api_view(['GET'])
def get_products(request,userid,categoryid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            user=BusinessUsers.objects.get(uid=userid)
            category=ProductCategory.objects.get(category_id=categoryid)
            if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid and category.brand.user==user):
                data=get_productsOfaCategory(category)      
                return Response({"data":data},status=status.HTTP_200_OK)
            else:
                return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            pass
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['POST'])
def create_product(request,userid,categoryid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        user=BusinessUsers.objects.get(uid=userid)
        category=ProductCategory.objects.get(category_id=categoryid)
        try:
            if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid and category.brand.user==user):
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                product_name=(body['product_name']).upper()
                product_desc=body['product_desc']
                product_price=body['product_price']
                product_mfg_date=body['product_mfg_date']
                product_expiry_date=body['product_expiry_date']
                if(not isProductExists(product_name=product_name)):
                    ID=uuid.uuid4()
                    p=Product(category=category,product_id=ID,name=product_name,price=product_price,desc=product_desc,mfg_date=product_mfg_date,expiry_date=product_expiry_date)
                    p.save()
                    data={
                        "product_id":ID,
                        "product_name":product_name,
                        "product_desc":product_desc,
                        "product_price":product_price,
                        "product_mfg_date":product_mfg_date,
                        "product_expiry_date":product_expiry_date
                    }
                    return Response({"info":"created!!!","data":data},status=status.HTTP_201_CREATED)
                else:
                    return Response({"info":"product already exists!"},status=status.HTTP_409_CONFLICT)
            else:
                return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        except:             
            pass
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def update_product(request,userid,productid):
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
                if(body.__contains__('product_name')):
                    product.name=body['product_name'].upper()
                elif(body.__contains__('product_desc')):
                    product.desc=body['product_desc']
                elif(body.__contains__('product_price')):
                    product.price=body['product_price']
                elif(body.__contains__('product_mfg_date')):
                    product.mfg_date=body['product_mfg_date']
                elif(body.__contains__('product_expiry_date')):
                    product.expiry_date=body['product_expiry_date']
                product.save()     
                return Response({"info":"updated!!!"},status=status.HTTP_200_OK)
        except:
            pass
        else:
            return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
             
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_product(request,userid,productid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            user=BusinessUsers.objects.get(uid=userid)
            product=Product.objects.get(product_id=productid)
            if(verifyAccess(request,ACCESSED_BY) and Verify(request).is_Tokenvalid()['userid']==userid and product.category.brand.user==user):
                product.delete()    
                return Response({"info":"deleted!!!"},status=status.HTTP_201_CREATED)
        except:
            pass
        else:
            return Response({"info":"access denied!"},status=status.HTTP_406_NOT_ACCEPTABLE)
             
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)