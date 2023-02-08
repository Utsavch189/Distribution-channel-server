from django.urls import path
from micro_brandCategoryProduct_service.views.brand_views import *

urlpatterns=[
    path('create_brand/userid=<str:userid>',create_brand),
    path('update_brand/userid=<str:userid>&brand_id=<str:brand_id>',update_brand),
    path('delete_brand/userid=<str:userid>&brand_id=<str:brand_id>',delete_brand),
    path('get_brands/userid=<str:userid>',get_brands)
]