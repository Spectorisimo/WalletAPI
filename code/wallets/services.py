import users.models
from typing import Protocol
from django.db.models import QuerySet
from . import models
from . import repository
from py_currency_converter import convert
from decimal import Decimal


class WalletServicesInterface(Protocol):

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


class WalletServicesV1:
    wallet_repo: repository.WalletRepositoryInterface = repository.WalletRepositoryV1()

    def get_wallets(self, user: users.models.CustomUser) -> QuerySet[models.Wallet]:
        return self.wallet_repo.get_wallets(user)

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
