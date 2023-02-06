from django.db import models
from micro_brands_service.models import Brand
from django.utils import timezone

class ProductCategory(models.Model):
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    category_id=models.CharField(max_length=50,default="",primary_key=True)
    category_name=models.CharField(max_length=35,null=True,blank=True)
    desc=models.CharField(max_length=155,null=True,blank=True)
    created_at=models.DateTimeField(timezone.now())

    def __str__(self) -> str:
        return str(self.brand +" "+self.category_name)
