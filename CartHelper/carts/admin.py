from django.contrib import admin
from .models import Cart, DataSet, CartGroup, CartFleet, DataCollection, Fault

admin.site.register(Cart)
admin.site.register(DataSet)
admin.site.register(CartGroup)
admin.site.register(CartFleet)
admin.site.register(DataCollection)
admin.site.register(Fault)
# Register your models here.
