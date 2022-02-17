from django.contrib import admin
from mainApp.models import Wallet, Trade, Order

# Register your models here.
admin.site.register(Wallet)
admin.site.register(Trade)
admin.site.register(Order)