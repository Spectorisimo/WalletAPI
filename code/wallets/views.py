from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import services, permissions, serializers
from utils import mixins


class WalletViewSet(mixins.ActionSerializerMixin, viewsets.ModelViewSet):
    ACTION_SERIALIZERS = {
        'partial_update': serializers.UpdateWalletSerializer,
        'create': serializers.CreateWalletSerializer,
    }

    wallet_services: services.WalletServicesInterface = services.WalletServicesV1()

    serializer_class = serializers.WalletSerializer
    permission_classes = permissions.IsWalletOwner,

    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        return self.wallet_services.get_wallets(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     try:
    #         super().create(request, *args, **kwargs)
    #     except ValidationError:
    #         return Response(data={"error": "User already have the wallet with this currency"},
    #                         status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = serializers.CreateWalletSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        self.wallet_services.create_wallet(serializer.validated_data)

        return Response({'message': 'Wallet has been successfully created'}, status=status.HTTP_201_CREATED)
