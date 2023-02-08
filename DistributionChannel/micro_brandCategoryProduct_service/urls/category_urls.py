from django.urls import path
from micro_brandCategoryProduct_service.views.category_views import *

urlpatterns = [
    path('get_categories/userid=<str:userid>&brand_id=<str:brandid>',get_categories),
    path('create_category/userid=<str:userid>&brand_id=<str:brandid>',create_category),
    path('update_category/userid=<str:userid>&category_id=<str:categoryid>',update_category),
    path('delete_category/userid=<str:userid>&category_id=<str:categoryid>',delete_category)
]
