import uuid

from django.db import models
import wallets.models
from wallets import choices as wallet_choices
from . import choices


class WalletTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    amount = models.DecimalField(decimal_places=2, max_digits=14)
    amount_currency = models.CharField(choices=wallet_choices.WalletCurrencyChoices.choices, max_length=3)

    sender = models.ForeignKey(to=wallets.models.Wallet, on_delete=models.PROTECT, related_name='sent_operations',
                               null=True)
    receiver = models.ForeignKey(to=wallets.models.Wallet, on_delete=models.PROTECT, related_name='received_operations',
                                 null=True)

    operation_type = models.CharField(choices=choices.WalletTransactionChoices.choices, max_length=8)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction {self.id}'
