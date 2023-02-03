from django.contrib import admin
from .models import BusinessUsers,RefreshToken,OTP,Role

admin.site.register(BusinessUsers)
admin.site.register(Role)
admin.site.register(RefreshToken)
admin.site.register(OTP)