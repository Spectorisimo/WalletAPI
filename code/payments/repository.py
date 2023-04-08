from typing import Protocol, OrderedDict
from . import models
from django.db.models import QuerySet, Q


class WalletTransactionRepositoryInterface(Protocol):

    @staticmethod
    def create_transaction(data: OrderedDict) -> None:
        """
        Creates a new wallet transaction in the database.

        Args:
            data (OrderedDict): A dictionary containing the details of the transaction.
                The dictionary must contain the following keys:
                - sender (Wallet): The sender wallet instance.
                - receiver (Wallet): The receiver wallet instance.
                - amount (Decimal): The amount of currency to be transferred in the transaction.
                - amount_currency (str): The currency code of the amount (e.g. 'USD', 'EUR', 'KZT').
                - operation_type (str): The type of the transaction (e.g. 'transfer', 'deposit', 'withdraw').
                - additional_info (str, optional): Additional information about the transaction.

        Returns:
            None.

        Note:
            This method creates a new wallet transaction instance in the database using the data provided in the
            `data` parameter. The new transaction is saved in the database and can be retrieved using the `get_transactions`
            method of the `WalletTransactionRepositoryInterface` repository.
        """
        ...

    @staticmethod
    def get_transactions() -> QuerySet[models.WalletTransaction]:
        """
        Retrieve all wallet transactions related to the wallet with the given primary key.

        Args:
            pk (int): The primary key of the wallet.

        Returns:
            QuerySet[models.WalletTransaction]: A QuerySet of all wallet transactions related to the wallet.

        Note:
            The method filters the transactions using the sender or receiver with the given primary key.
            It also uses `select_related` to optimize the database query by fetching the sender and receiver
            objects with a single JOIN query.
        """
        ...


class WalletTransactionRepositoryV1:

    def create_transaction(self, data: OrderedDict) -> None:
        models.WalletTransaction.objects.create(**data)

    def get_transactions(self, pk: int) -> QuerySet[models.WalletTransaction]:
        return models.WalletTransaction.objects.filter(
            Q(sender=pk) | Q(receiver=pk)
        ).select_related('sender', 'receiver')
