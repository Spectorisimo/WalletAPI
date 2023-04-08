from django.db import models
from users import models as users_models
from . import choices
import random


class Wallet(models.Model):
    wallet_number = models.CharField(unique=True, editable=False, null=True, blank=True, max_length=10)

    user = models.ForeignKey(to=users_models.CustomUser, on_delete=models.PROTECT, related_name='wallets')

    name = models.CharField(max_length=30, default='Мой кошелёк')
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    amount_currency = models.CharField(max_length=3, choices=choices.WalletCurrencyChoices.choices,
                                       default=choices.WalletCurrencyChoices.KZT)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def generate_number() -> str:
        wallet_number = ''.join(random.choices('0123456789', k=10))

        if Wallet.objects.filter(wallet_number=wallet_number).exists():
            return Wallet.generate_number()

        return wallet_number

    def save(self, *args, **kwargs):
        if not self.pk:
            self.wallet_number = self.generate_number()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'amount_currency')


