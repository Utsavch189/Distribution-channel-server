from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import uuid
from micro_auth_service.models import BusinessUsers,Role
from Authorization.authorization import Verify
from micro_brandCategoryProduct_service.models import Product
from .models import SetProductPriceForWholesalerAndRetailer,Stock
from micro_production_service.models import Production
import json
from VerifyAccess.access import verifyAccess
from decouple import config
from datetime import datetime

Manufacturer=config('Manufacturer')
WholeSaler=config('WholeSaler')
Retailer=config('Retailer')

def manageDistributionFromManufacturer(product,product_quant):
    try:
        if(Production.objects.filter(product=product).exists()):
            lists=[]
            obj=Production.objects.filter(product=product)
            if obj.filter(production_rate=product_quant).exists():
                obj_id=obj.values('production_id')[0]['production_id']
                production=Production.objects.get(production_id=obj_id)
                lists.append({
                        "production_obj":production,
                        "remain_production":0
                        })
                return lists
            else:
                quant=0
                for p in range(0,obj.count()):
                    product_quants=obj.values('production_rate')[p]['production_rate']
                    obj_id=obj.values('production_id')[p]['production_id']
                    production=Production.objects.get(production_id=obj_id)
                    if int(product_quants)>(int(product_quant)-quant):
                        lists.append({
                            "production_obj":production,
                            "remain_production":int(product_quants)-(int(product_quant)-quant)
                        })
                        quant=0
                        break
                    elif int(product_quants)<=(int(product_quant)-quant):
                        if(quant==int(product_quant)):
                            quant=0
                            break
                        quant=quant+int(product_quants)
                        lists.append({
                            "production_obj":production,
                            "remain_production":0
                        })
                    if(p==obj.count()-1):
                        if not (quant==product_quant):
                            lists=[]
            return lists

    except:
        pass

def manageProductionStockForManufacturer(m):
    try:
        for i in m:
            i['production_obj'].production_rate=i['remain_production']
            i['production_obj'].save()
    except:
        pass

def manageDistributionFromOtherUsers(product,product_quant,imported_from_user):
    try:
        if(Stock.objects.filter(stock_admin=imported_from_user,product=product).exists()):
            lists=[]
            obj=Stock.objects.filter(stock_admin=imported_from_user,product=product)
            if obj.filter(stock_quantity=product_quant).exists():
                obj_id=obj.filter(stock_quantity=product_quant).values('stock_id')[0]['stock_id']
                stock=Stock.objects.get(stock_id=obj_id)
                lists.append({
                        "stock_obj":stock,
                        "remain_stock":0
                        })
                return lists
            else:
                quant=0
                for p in range(0,obj.count()):
                    product_quants=obj.values('stock_quantity')[p]['stock_quantity']
                    obj_id=obj.values('stock_id')[p]['stock_id']
                    stock=Stock.objects.get(stock_id=obj_id)
                    if int(product_quants)>(int(product_quant)-quant):
                        lists.append({
                            "stock_obj":stock,
                            "remain_stock":int(product_quants)-(int(product_quant)-quant)
                        })
                        break
                    elif int(product_quants)<=(int(product_quant)-quant):
                        if(quant==int(product_quant)):
                            break
                        quant=quant+int(product_quants)
                        lists.append({
                            "stock_obj":stock,
                            "remain_stock":0
                        })
                    if(p==obj.count()-1):
                        if not (quant==product_quant):
                            lists=[]
            return lists
    except:
        pass

def manageStockForOthers(m):
    try:
        for i in m:
            i['stock_obj'].stock_quantity=i['remain_stock']
            i['stock_obj'].save()
    except:
        pass

@api_view(['POST'])
def distribute(request,productid,userid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            product_quant=body['product_quant']
            supply_to_id=body['supply_to_id']
            currentDate=datetime.today().strftime('%Y-%m-%d')

            supply_to_user=BusinessUsers.objects.get(uid=supply_to_id)
            product=Product.objects.get(product_id=productid)
            imported_from_user=BusinessUsers.objects.get(uid=userid)

            if(Role.objects.get(user=supply_to_user).role==Manufacturer or supply_to_user==imported_from_user):
                return Response({"info":"not accepted!"},status=status.HTTP_406_NOT_ACCEPTABLE)

            if(Role.objects.get(user=imported_from_user).role==Manufacturer):
                #import from manufacturer's production
                m=manageDistributionFromManufacturer(product,product_quant)
                if(m):
                    if not (SetProductPriceForWholesalerAndRetailer.objects.filter(user=supply_to_user,product=product).exists()):
                        y=SetProductPriceForWholesalerAndRetailer(user=supply_to_user,product=product,price_id=uuid.uuid4(),price=0)
                        y.save()
                    if(Stock.objects.filter(stock_admin=supply_to_user,imported_from=imported_from_user,product=product,date=currentDate).exists()):
                        s_obj=Stock.objects.filter(stock_admin=supply_to_user,imported_from=imported_from_user,product=product,date=currentDate)
                        pre_stock=s_obj.values('stock_quantity')[0]['stock_quantity']
                        pre_price=s_obj.values('total_price')[0]['total_price']
                        s_obj.update(stock_quantity=int(pre_stock)+int(product_quant))
                        s_obj.update(total_price=int(pre_price)+(int(product.price)*int(product_quant)))
                        manageProductionStockForManufacturer(m)
                        return Response({"info":"stock updated!!!"},status=status.HTTP_200_OK)
                    else:
                        s=Stock(stock_admin=supply_to_user,imported_from=imported_from_user,product=product,stock_id=uuid.uuid4(),stock_quantity=product_quant,total_price=int(product.price)*int(product_quant),date=currentDate)
                        s.save()
                        manageProductionStockForManufacturer(m)
                        return Response({"info":"stock added!!!"},status=status.HTTP_200_OK)
                else:
                    return Response({"info":"not enough stock!"},status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                #import from others stock
                m=manageDistributionFromOtherUsers(product,product_quant,imported_from_user)
                if(m):
                    obj=SetProductPriceForWholesalerAndRetailer.objects.filter(user=imported_from_user,product=product)
                    price=obj.values('price')[0]['price']

                    if(int(price)==0):
                        return Response({"update your selling price first!"},status=status.HTTP_400_BAD_REQUEST)

                    if not (SetProductPriceForWholesalerAndRetailer.objects.filter(user=supply_to_user,product=product).exists()):
                        y=SetProductPriceForWholesalerAndRetailer(user=supply_to_user,product=product,price_id=uuid.uuid4(),price=0)
                        y.save()
                    if(Stock.objects.filter(stock_admin=supply_to_user,imported_from=imported_from_user,product=product,date=currentDate).exists()):
                        s_obj=Stock.objects.filter(stock_admin=supply_to_user,imported_from=imported_from_user,product=product,date=currentDate)
                        pre_stock=s_obj.values('stock_quantity')[0]['stock_quantity']
                        pre_price=s_obj.values('total_price')[0]['total_price']
                        s_obj.update(stock_quantity=int(pre_stock)+int(product_quant))
                        s_obj.update(total_price=int(pre_price)+(int(price)*int(product_quant)))
                        manageStockForOthers(m)
                        return Response({"info":"stock updated!!!"},status=status.HTTP_200_OK)
                    else:
                        s=Stock(stock_admin=supply_to_user,imported_from=imported_from_user,product=product,stock_id=uuid.uuid4(),stock_quantity=product_quant,total_price=int(price)*int(product_quant),date=currentDate)
                        s.save()
                        manageStockForOthers(m)
                        return Response({"info":"stock added!!!"},status=status.HTTP_200_OK)
                else:
                    return Response({"info":"not enough stock!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            pass
             
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def updatePrice(request,productid,userid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            product_price=body['product_price']

            user=BusinessUsers.objects.get(uid=userid)
            product=Product.objects.get(product_id=productid)

            if(Role.objects.get(user=user).role==Manufacturer):
                return Response({"info":"not accepted!"},status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if(SetProductPriceForWholesalerAndRetailer.objects.filter(user=user,product=product).exists()):
                obj=SetProductPriceForWholesalerAndRetailer.objects.filter(user=user,product=product)
                obj.update(price=product_price)
                return Response({"info":"price updated!!!"},status=status.HTTP_200_OK)
        except:
            pass
             
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def deleteStock(request,stockid,userid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            user=BusinessUsers.objects.get(uid=userid)
            s=Stock.objects.get(stock_id=stockid)
            if(Role.objects.get(user=user).role==Manufacturer or s.stock_admin!=user):
                return Response({"info":"not accepted!"},status=status.HTTP_406_NOT_ACCEPTABLE)
            
            s1=SetProductPriceForWholesalerAndRetailer.objects.filter(user=user,product=s.product)
            s.delete()
            if not (Stock.objects.filter(stock_admin=user).exists()):
                s1.delete()
            return Response({"info":"stock deleted!!!"},status=status.HTTP_200_OK)
        except:
            pass
             
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def getAllStock(user):
    try:
        if(Stock.objects.filter(stock_admin=user).exists()):
            obj=Stock.objects.filter(stock_admin=user)
            sub_obj=SetProductPriceForWholesalerAndRetailer.objects.filter(user=user)
            lists=[]
            for i in range(0,obj.count()):
                product_id=(obj.values('product')[i]['product'])
                product=Product.objects.get(product_id=product_id)
                imported_from=(obj.values('imported_from')[i]['imported_from'])
                imported_from_user=BusinessUsers.objects.get(uid=imported_from).name
                data={
                    "product_id":product_id,
                    "product_name":product.name,
                    "product_quantity":(obj.values('stock_quantity')[i]['stock_quantity']),
                    "stock_id":(obj.values('stock_id')[i]['stock_id']),
                    "buying_cost_total":(obj.values('total_price')[i]['total_price']),
                    "selling_price":sub_obj.filter(product=product).values('price')[0]['price'],
                    "buying_from":imported_from_user,
                    "date":(obj.values('date')[i]['date'])
                }
                
                lists.append(data)
            return lists
    except:
        pass

@api_view(['GET'])
def getStocks(request,userid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            user=BusinessUsers.objects.get(uid=userid)

            if(Role.objects.get(user=user).role==Manufacturer):
                return Response({"info":"not accepted!"},status=status.HTTP_406_NOT_ACCEPTABLE)
            
            data=getAllStock(user)
            return Response({"data":data},status=status.HTTP_200_OK)
        except:
            pass
             
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def getDistributionStatus(user):
    try:
        if(Stock.objects.filter(imported_from=user).exists()):
            obj=Stock.objects.filter(imported_from=user)
            
            lists=[]
            for i in range(0,obj.count()):
                product_id=(obj.values('product')[i]['product'])
                product=Product.objects.get(product_id=product_id)
                selled_to=(obj.values('stock_admin')[i]['stock_admin'])
                selled_to_user=BusinessUsers.objects.get(uid=selled_to).name
                data={
                    "product_id":product_id,
                    "product_name":product.name,
                    "product_quantity":(obj.values('stock_quantity')[i]['stock_quantity']),
                    "selling_cost_total":(obj.values('total_price')[i]['total_price']),
                    "selled_to":selled_to_user,
                    "date":(obj.values('date')[i]['date'])
                }
                
                lists.append(data)
            return lists
    except:
        pass

@api_view(['GET'])
def distributionStatus(request,userid):
    if(Verify(request).is_Tokenvalid()['status']==401):
        return Response({"info":"UnAuthorized"},status=status.HTTP_401_UNAUTHORIZED)
    
    elif (Verify(request).is_Tokenvalid()['status']==403):
        return Response({"info":"invalid token"},status=status.HTTP_403_FORBIDDEN)
    
    elif(Verify(request).is_Tokenvalid()['status']==200):
        try:
            user=BusinessUsers.objects.get(uid=userid)
            data=getDistributionStatus(user)
            return Response({"data":data},status=status.HTTP_200_OK)
        except:
            pass
             
    return Response({"info":"Something wrong!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)