from django.urls import path
from micro_brandCategoryProduct_service.views.product_views import *

urlpatterns = [
    path('get_products/userid=<str:userid>&category_id=<str:categoryid>',get_products),
    path('create_product/userid=<str:userid>&category_id=<str:categoryid>',create_product),
    path('update_product/userid=<str:userid>&product_id=<str:productid>',update_product),
    path('delete_product/userid=<str:userid>&product_id=<str:productid>',delete_product)
]
