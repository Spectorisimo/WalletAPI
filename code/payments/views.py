from rest_framework import viewsets, status
from rest_framework.response import Response
from . import permissions
from . import serializers, services
from drf_yasg.utils import swagger_auto_schema


class WalletTransactionViewSet(viewsets.ViewSet):
    transaction_services: services.WalletTransactionServicesInterface = services.WalletTransactionServicesV1()
    permission_classes = permissions.IsWalletOwner,

    @swagger_auto_schema(request_body=serializers.WalletTransferSerializer)
    def transfer(self, request, pk=None):
        serializer = serializers.WalletTransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.transaction_services.transfer(pk, serializer.validated_data)

        return Response(status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.WalletDepositWithdrawSerializer)
    def deposit(self, request, pk=None):
        serializer = serializers.WalletDepositWithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.transaction_services.deposit(pk, serializer.validated_data)

        return Response(status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.WalletDepositWithdrawSerializer)
    def withdraw(self, request, pk=None):
        serializer = serializers.WalletDepositWithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.transaction_services.withdraw(pk, serializer.validated_data)

        return Response(status.HTTP_200_OK)

    def get_transactions(self, request, pk=None):
        transactions = self.transaction_services.get_transactions(pk)
        serializer = serializers.WalletTransactionSerializer(transactions, many=True)

        return Response(serializer.data)
