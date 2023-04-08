from django.db.models import TextChoices


class WalletCurrencyChoices(TextChoices):
    KZT = 'KZT'
    EUR = 'EUR'
    USD = 'USD'
