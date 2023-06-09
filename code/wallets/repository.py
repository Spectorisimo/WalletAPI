from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

import users.models

from typing import Protocol, OrderedDict
from django.db.models import QuerySet
from . import models


class WalletRepositoryInterface(Protocol):

    @staticmethod
    def create_wallet(data: OrderedDict) -> None:
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
    def get_wallets() -> QuerySet[models.Wallet]:
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


class WalletRepositoryV1:

    def create_wallet(self, data: OrderedDict) -> None:
        wallet = models.Wallet.objects.create(**data)
        wallet_fee = models.WalletMonthlyFee.objects.create(wallet=wallet,
                                                            next_charge_date=timezone.now() + timedelta(days=30),
                                                            )

    def get_wallets(self, user: users.models.CustomUser) -> QuerySet[models.Wallet]:
        return models.Wallet.objects.filter(user=user).select_related('user')
