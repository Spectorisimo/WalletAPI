from rest_framework import serializers
from . import models


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wallet
        fields = '__all__'


class CreateWalletSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Wallet
        fields = ('user', 'name', 'amount_currency')


class UpdateWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wallet
        fields = ('name',)
