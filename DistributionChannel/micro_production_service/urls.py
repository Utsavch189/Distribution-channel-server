from django.urls import path
from .views import *

urlpatterns = [
    path('update_production/user_id=<str:userid>&product_id=<str:productid>',update_production),
    path('get_production_of_a_product/user_id=<str:userid>&product_id=<str:productid>',get_production_of_a_product)
]
