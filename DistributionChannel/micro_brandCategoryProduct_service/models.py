from django.db import models
from micro_auth_service.models import BusinessUsers
from django.utils import timezone

class Brand(models.Model):
    user=models.ForeignKey(BusinessUsers,on_delete=models.CASCADE)
    brand_id=models.CharField(max_length=50,default="",primary_key=True)
    brand_name=models.CharField(max_length=35,null=True,blank=True)
    brand_desc=models.CharField(max_length=155,null=True,blank=True)
    created_at=models.DateTimeField(timezone.now())

    def __str__(self):
        return str(f"Brand:{self.brand_name} under Author:{self.user}")
    

class ProductCategory(models.Model):
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    category_id=models.CharField(max_length=50,default="",primary_key=True)
    category_name=models.CharField(max_length=35,null=True,blank=True)
    desc=models.CharField(max_length=155,null=True,blank=True)
    created_at=models.DateTimeField(timezone.now())

    def __str__(self) -> str:
        return str(f"category:{self.category_name} under {self.brand}")


class Product(models.Model):
    category=models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    product_id=models.CharField(max_length=50,default="",primary_key=True)
    name=models.CharField(max_length=35,null=True,blank=True)
    price=models.CharField(max_length=8,null=True,blank=True)
    desc=models.CharField(max_length=155,null=True,blank=True)
    mfg_date=models.CharField(max_length=35,null=True,blank=True)
    expiry_date=models.CharField(max_length=35,null=True,blank=True)

    def __str__(self):
        return str(f"product:{self.name} under category:{self.category}")


