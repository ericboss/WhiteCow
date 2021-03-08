from django.contrib import admin
from .models import Deals, Adress,AssetTypes,ComputeDeals

# Register your models here.
admin.site.register(Adress)
admin.site.register(Deals)
admin.site.register(AssetTypes)
admin.site.register(ComputeDeals)

