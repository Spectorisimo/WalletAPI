from rest_framework import permissions
from wallets import models


class IsWalletOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        wallet_pk = view.kwargs.get('pk')
        wallet = models.Wallet.objects.get(pk=wallet_pk)
        return wallet.user == request.user
