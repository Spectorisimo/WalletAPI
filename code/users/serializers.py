from rest_framework import serializers
from . import models
from wallets import serializers as wallets_serializers


class UserSerializer(serializers.ModelSerializer):
    wallets = wallets_serializers.WalletSerializer(many=True)

    class Meta:
        model = models.CustomUser
        fields = ('email', 'phone_number', 'wallets', 'profile_image', 'first_name', 'last_name')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('email', 'phone_number', 'password')


class VerifyUserSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    code = serializers.CharField(max_length=4)


class CreateTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()


class UpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()


class UpdatePersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('profile_image', 'first_name', 'last_name')
