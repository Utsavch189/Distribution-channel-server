from django.db import models
from micro_category_service.models import ProductCategory
from django.utils import timezone


class Product(models.Model):
    category=models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    product_id=models.CharField(max_length=50,default="",primary_key=True)
    name=models.CharField(max_length=35,null=True,blank=True)
    price=models.CharField(max_length=8,null=True,blank=True)
    desc=models.CharField(max_length=155,null=True,blank=True)
    mfg_date=models.CharField(max_length=35,null=True,blank=True)
    expiry_date=models.CharField(max_length=35,null=True,blank=True)

    def __str__(self):
        return str(self.category+" "+self.name)