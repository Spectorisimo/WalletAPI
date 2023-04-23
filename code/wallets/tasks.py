from celery import shared_task
from . import services
from . import models
from django.utils import timezone


@shared_task
def charge_monthly_fees():
    wallet_services: services.WalletServicesInterface = services.WalletServicesV1()
    for fee in models.WalletMonthlyFee.objects.filter(next_charge_date__lte=timezone.now()):
        wallet_services.charge_fee(fee.wallet, fee)
