import users.models

from typing import Protocol
from django.db.models import QuerySet
from . import models


class WalletRepositoryInterface(Protocol):

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

    def get_wallets(self, user: users.models.CustomUser) -> QuerySet[models.Wallet]:
        return models.Wallet.objects.filter(user=user).select_related('user')
