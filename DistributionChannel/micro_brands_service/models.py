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
        return str(f"Author:{self.user} and Brand:{self.brand_name}")




