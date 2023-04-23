from django.db.models import TextChoices


class WalletTransactionChoices(TextChoices):
    deposit = 'DEPOSIT'
    transfer = 'TRANSFER'
    withdraw = 'WITHDRAW'
    fee = 'FEE'
