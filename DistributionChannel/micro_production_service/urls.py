from django.urls import path
from .views import *

urlpatterns = [
    path('update_production/user_id=<str:userid>&product_id=<str:productid>',update_production),
    path('get_total_production_of_a_product/user_id=<str:userid>&product_id=<str:productid>',get_total_production_of_a_product),
    path('get_total_production_of_a_user/user_id=<str:userid>',get_total_production_of_a_user)
]
