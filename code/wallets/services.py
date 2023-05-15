from django.db import transaction

import users.models
from typing import Protocol, OrderedDict
from django.db.models import QuerySet
from . import models
from . import repository
from py_currency_converter import convert
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from . import choices
from payments import repository as payments_repository
from payments import choices as payments_choices


class WalletServicesInterface(Protocol):

    @staticmethod
    def create_wallet(self, data: OrderedDict) -> None:
        """
        Creates a new wallet for the user with the given data, and also creates a monthly fee for the wallet.

        Args:
        - data (OrderedDict): An OrderedDict containing the data for the new wallet. It must include the following keys:
            - user (User): The User instance associated with the new wallet.
            - currency (str): The currency code for the new wallet, e.g. "USD", "EUR", "KZT", etc.
            - name (Decimal): The wallet name.

        Returns:
        None
        """
        ...

    @staticmethod
    def get_wallets(user: models.Wallet) -> QuerySet[models.Wallet]:
        """
        Retrieves all wallets belonging to the specified user.

        Args:
            user: A CustomUser object representing the user whose wallets to retrieve.

        Returns:
            A QuerySet of Wallet objects related to the specified user, with the 'user' attribute preloaded.

        Raises:
            None.
        """
        ...

    @staticmethod
    def charge_fee(wallet: models.Wallet, fee: models.WalletMonthlyFee) -> None:
        """
        Deducts the monthly fee for using the wallet from the wallet balance and records transaction information.

        Args:
        - wallet (models.Wallet): An instance of the Wallet model representing the user's wallet.
        - fee (models.WalletMonthlyFee): An instance of the WalletMonthlyFee model representing the monthly fee to be charged.

        Returns:
        None.
        """
        ...


class WalletServicesV1:
    wallet_repo: repository.WalletRepositoryInterface = repository.WalletRepositoryV1()
    payments_repo: payments_repository.WalletTransactionRepositoryInterface = payments_repository.WalletTransactionRepositoryV1()

    def get_wallets(self, user: users.models.CustomUser) -> QuerySet[models.Wallet]:
        return self.wallet_repo.get_wallets(user)

    def create_wallet(self, data: OrderedDict) -> None:
        self.wallet_repo.create_wallet(data)

    @staticmethod
    def currency_converter(first_currency: str, second_currency: str, amount: Decimal) -> Decimal:
        match first_currency, second_currency:
            case 'KZT', 'USD':
                return round(Decimal((convert('KZT', amount=float(amount), to=['USD', ])['USD'])), 2)
            case 'KZT', 'EUR':
                return round(Decimal((convert('KZT', amount=float(amount), to=['EUR', ])['EUR'])), 2)
            case 'USD', 'KZT':
                return round(Decimal((convert('USD', amount=float(amount), to=['KZT', ])['KZT'])), 2)
            case 'USD', 'EUR':
                return round(Decimal((convert('USD', amount=float(amount), to=['EUR', ])['EUR'])), 2)
            case 'EUR', 'USD':
                return round(Decimal((convert('EUR', amount=float(amount), to=['USD', ])['USD'])), 2)
            case 'EUR', 'KZT':
                return round(Decimal((convert('EUR', amount=float(amount), to=['KZT', ])['KZT'])), 2)

    @staticmethod
    def charge_fee(wallet: models.Wallet, fee: models.WalletMonthlyFee) -> None:
        amount = fee.amount
        if wallet.amount_currency != 'KZT':
            amount = WalletServicesV1.currency_converter('KZT', wallet.amount_currency, fee.amount)
        with transaction.atomic():

            if wallet.amount >= amount:

                wallet.amount -= amount
                wallet.is_active = True
                wallet.save()

                wallet.fee.next_charge_date = timezone.now() + timedelta(days=30)
                wallet.fee.save()

                transaction_data = {
                    'sender': wallet,
                    'receiver': None,
                    'amount': amount,
                    'amount_currency': wallet.amount_currency,
                    'operation_type': payments_choices.WalletTransactionChoices.fee
                }
                WalletServicesV1.payments_repo.create_transaction(transaction_data)

            else:
                wallet.is_active = False
                wallet.save()
