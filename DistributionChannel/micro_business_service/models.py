from django.db import models
from micro_auth_service.models import BusinessUsers
from micro_brandCategoryProduct_service.models import Product

class Stock(models.Model):
    stock_admin=models.ForeignKey(BusinessUsers,on_delete=models.CASCADE,related_name='stock_admin',default="")
    imported_from=models.ForeignKey(BusinessUsers,on_delete=models.DO_NOTHING,related_name='imported_from',default="")
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING,default="")
    stock_id=models.CharField(max_length=50,default="",primary_key=True)
    stock_quantity=models.CharField(max_length=20,default="")
    total_price=models.CharField(max_length=20,default="")
    date=models.CharField(max_length=20,default="")

    def __str__(self):
        return str(f"{self.product} under {self.stock_admin} imported-from {self.imported_from} at {self.stock_quantity} quantity")

class SetProductPriceForWholesalerAndRetailer(models.Model):
    user=models.ForeignKey(BusinessUsers,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    price_id=models.CharField(max_length=50,default="",primary_key=True)
    price=models.CharField(max_length=20,default="")

    def __str__(self):
        return str(f"{self.product} under {self.user} in price of {self.price}")