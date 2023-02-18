from django.urls import path
from .views import *

urlpatterns = [
    path('distribute/user_id=<str:userid>&product_id=<str:productid>',distribute),
    path('updatePrice/user_id=<str:userid>&product_id=<str:productid>',updatePrice),
    path('deleteStock/user_id=<str:userid>&stock_id=<str:stockid>',deleteStock),
    path('getStocks/user_id=<str:userid>',getStocks),
    path('distributionStatus/user_id=<str:userid>',distributionStatus)
]
