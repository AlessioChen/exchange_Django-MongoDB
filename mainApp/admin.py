from django.contrib import admin
from mainApp.models import Transaction, Wallet, Order

# Register your models here.
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Order)