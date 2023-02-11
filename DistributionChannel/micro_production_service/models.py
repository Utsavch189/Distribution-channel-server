from django.db import models
from micro_brandCategoryProduct_service.models import Product

class Production(models.Model):
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    production_id=models.CharField(max_length=50,default="",primary_key=True)
    production_rate=models.CharField(max_length=20,default="")
    production_date=models.CharField(max_length=20,default="")

    def __str__(self):
        return str(f"production number : {self.production_rate} of product : {self.product} at date : {self.production_date}")
