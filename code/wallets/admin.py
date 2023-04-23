from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['wallet_number','user','amount','amount_currency','is_active','updated_at','created_at']


admin.site.register(models.WalletMonthlyFee)