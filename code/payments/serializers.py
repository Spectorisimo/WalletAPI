from rest_framework import serializers
from . import models
from wallets import models as wallets_models


class WalletDepositWithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WalletTransaction
        fields = ('amount',)


class WalletTransferSerializer(serializers.ModelSerializer):
    wallet_number = serializers.CharField(required=True)

    class Meta:
        model = models.WalletTransaction
        fields = ('wallet_number', 'amount')


class WalletPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = wallets_models.Wallet
        fields = ('wallet_number',)


class WalletTransactionSerializer(serializers.ModelSerializer):
    sender = WalletPhoneNumberSerializer()
    receiver = WalletPhoneNumberSerializer()

    class Meta:
        model = models.WalletTransaction
        fields = '__all__'
