from django.contrib import admin
from .models import Stock,SetProductPriceForWholesalerAndRetailer

admin.site.register(Stock)
admin.site.register(SetProductPriceForWholesalerAndRetailer)