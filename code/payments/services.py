from typing import Protocol, OrderedDict
from django.db import transaction
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from . import models, choices, repository
from wallets import models as wallets_models
from wallets import services as wallet_services


class WalletTransactionServicesInterface(Protocol):

    @staticmethod
    def transfer(pk, data: OrderedDict) -> None:
        """
        Transfer an amount of money from one wallet to another.

        Args:
            pk (int): The primary key of the wallet sending the money.
            data (OrderedDict): A dictionary containing data about the transaction.
                The dictionary must contain the following keys:
                - wallet_number (str): The wallet number of the wallet receiving the money.
                - amount (Decimal): The amount of money to transfer.

        Raises:
            ValidationError: If the sender wallet does not have enough balance to make the transfer,
                or if the sender and receiver wallets are the same,or sender/receiver wallet is not active.

        Returns:
            None.

        Note:
            This method subtracts the transferred amount from the sender wallet's balance, and adds it
            to the receiver wallet's balance. If the currencies of the sender and receiver wallets are
            different, the amount is converted using the currency conversion service before the transfer.
            Finally, a transaction object is created to record the transaction details.
        """
        ...

    @staticmethod
    def deposit(data: OrderedDict) -> None:
        """
        Deposits the specified amount to the wallet with the given primary key.

        Args:
            pk (int): The primary key of the wallet to deposit to.
            data (OrderedDict): A dictionary containing transaction data.
                The dictionary must contain the following keys:
                - amount (Decimal): The amount to deposit.
                The dictionary may also contain the following key:
                - note (str): A note about the deposit transaction.

        Raises:
            Http404: If the wallet with the given primary key does not exist.
            ValidationError: If the amount to deposit is negative,or sender's/receiver's wallet is not active

        Note:
            This method uses a database transaction to ensure the atomicity of the deposit operation.
            The deposit transaction is recorded as a `WalletTransaction` instance in the database.
        """
        ...

    @staticmethod
    def withdraw(data: OrderedDict) -> None:
        """
        This method withdraws a certain amount of money from a wallet and creates a new transaction in the database
        to record the withdrawal.

        Args:

            pk (int): The primary key of the wallet from which to withdraw the money.
            data (OrderedDict): A dictionary containing the data for the transaction.
            The dictionary must contain the following key:
                - amount (Decimal): The amount of money to withdraw from the wallet.
        Returns:

            None
        Raises:

            ValidationError: If the wallet is blocked or the amount is less than zero,
            or if there is not enough balance in the wallet to withdraw the amount.
        Note:

            Method first checks whether the wallet is valid and has enough balance to withdraw the specified amount.
            If the wallet is active and has enough balance, the specified amount is deducted from the wallet's balance
            and a new transaction is created with the sender as the wallet
            from which the money was withdrawn, and no receiver.
        """
        ...

    @staticmethod
    def get_transactions(pk: int) -> QuerySet[models.WalletTransaction]:
        """
        Returns a queryset of all transactions related to a wallet with the given primary key.

        Args:
            pk (int): The primary key of the wallet to retrieve transactions for.

        Returns:
            QuerySet[models.WalletTransaction]: A queryset of all transactions related to the given wallet.

        Raises:
            Http404: If no wallet exists with the given primary key.
        """
        ...


class WalletTransactionServicesV1:
    transaction_repos: repository.WalletTransactionRepositoryInterface = repository.WalletTransactionRepositoryV1()

    def transfer(self, pk: int, data: OrderedDict) -> None:

        wallet_sender = get_object_or_404(wallets_models.Wallet, pk=pk)
        wallet_receiver = get_object_or_404(wallets_models.Wallet, wallet_number=data.pop('wallet_number'))
        amount = data['amount']

        self.is_wallet_valid(wallet_sender, data['amount'], choices.WalletTransactionChoices.transfer)

        if wallet_sender == wallet_receiver:
            raise ValidationError({'error': 'Sender and receiver wallets are the same'})

        with transaction.atomic():
            wallet_sender.amount -= amount

            if wallet_sender.amount_currency != wallet_receiver.amount_currency:
                amount = wallet_services.WalletServicesV1.currency_converter(
                    wallet_sender.amount_currency, wallet_receiver.amount_currency, amount)

            wallet_receiver.amount += amount
            wallet_sender.save()
            wallet_receiver.save()

            if not wallet_receiver.is_active:
                wallet_services.WalletServicesV1.charge_fee(wallet_receiver, wallet_receiver.fee)

            transaction_data = {
                'sender': wallet_sender,
                'receiver': wallet_receiver,
                'amount': data['amount'],
                'amount_currency': wallet_sender.amount_currency,
                'operation_type': choices.WalletTransactionChoices.transfer
            }

            self.transaction_repos.create_transaction(transaction_data)

    def deposit(self, pk: int, data: OrderedDict) -> None:
        wallet_receiver = get_object_or_404(wallets_models.Wallet, pk=pk)

        self.is_wallet_valid(wallet_receiver, data['amount'], choices.WalletTransactionChoices.deposit)

        with transaction.atomic():
            wallet_receiver.amount += data['amount']
            wallet_receiver.save()

            if not wallet_receiver.is_active:
                wallet_services.WalletServicesV1.charge_fee(wallet_receiver, wallet_receiver.fee)

            transaction_data = {
                'sender': None,
                'receiver': wallet_receiver,
                'amount': data['amount'],
                'amount_currency': wallet_receiver.amount_currency,
                'operation_type': choices.WalletTransactionChoices.deposit
            }

            self.transaction_repos.create_transaction(transaction_data)

    def withdraw(self, pk: int, data: OrderedDict) -> None:
        wallet_sender = get_object_or_404(wallets_models.Wallet, pk=pk)

        self.is_wallet_valid(wallet_sender, data['amount'], choices.WalletTransactionChoices.withdraw)

        with transaction.atomic():
            wallet_sender.amount -= data['amount']
            wallet_sender.save()

            transaction_data = {
                'sender': wallet_sender,
                'receiver': None,
                'amount': data['amount'],
                'amount_currency': wallet_sender.amount_currency,
                'operation_type': choices.WalletTransactionChoices.withdraw
            }

            self.transaction_repos.create_transaction(transaction_data)

    def get_transactions(self, pk: int) -> QuerySet[models.WalletTransaction]:
        return self.transaction_repos.get_transactions(pk)

    @staticmethod
    def is_wallet_valid(wallet: wallets_models.Wallet, amount, transaction_type):
        if amount < 0:
            raise ValidationError({'error': 'Operation with negative amount'})
        if not wallet.is_active and transaction_type is not choices.WalletTransactionChoices.deposit:
            raise ValidationError({'error': 'Your wallet is blocked'})
        if amount > wallet.amount and transaction_type is not choices.WalletTransactionChoices.deposit:
            raise ValidationError({'error': 'Not enough balance'})
        return True
