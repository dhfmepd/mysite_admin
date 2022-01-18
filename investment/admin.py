from django.contrib import admin
from .models import Market, Account, Stock

admin.site.register(Market)
admin.site.register(Account)
admin.site.register(Stock)