import pytest
import helpers
from django.contrib.auth import get_user_model
from rest_framework import status


@pytest.mark.django_db
class WalletTransactionsViewSetTest:

    @pytest.fixture(autouse=True)
    def load_data(self, load_fixtures):
        load_fixtures('users.json', 'wallets.json')

    @pytest.mark.parametrize('case,user_id,wallet_id,status_code', (
            (1, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 15, status.HTTP_200_OK),  # Correct case
            (5, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 16, status.HTTP_403_FORBIDDEN),  # User hasn't access to wallet
            (1, None, 16, status.HTTP_401_UNAUTHORIZED),  # No auth
            (2, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 15, status.HTTP_400_BAD_REQUEST),  # Try to transfer to yourself
            (3, "bcd36cf4-d9df-4ee7-8a29-3dc5106f9752", 18, status.HTTP_400_BAD_REQUEST),  # Wallet isn't active
            (4, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 15, status.HTTP_400_BAD_REQUEST),  # Not enough money
            (6, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 15, status.HTTP_400_BAD_REQUEST),  # Negative amount
            (7, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 15, status.HTTP_200_OK),  # Different currencies

    ))
    def test_transfer(self, api_client, case, user_id, wallet_id, status_code):
        data = helpers.load_json_data(f'payments/transfer/{case}')

        if not user_id:
            authorization = None
        else:
            user = get_user_model().objects.get(pk=user_id)
            authorization = helpers.access_token(user)

        response = api_client.post(
            f'/api/v1/users/wallets/{wallet_id}/transfer/',
            data=data,
            format='json',
            HTTP_AUTHORIZATION=authorization,
        )

        assert response.status_code == status_code

    @pytest.mark.parametrize('case,user_id,wallet_id,status_code', (
            (1, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 15, status.HTTP_200_OK),  # Correct case
            (1, None, 15, status.HTTP_401_UNAUTHORIZED),  # No auth
            (1, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 16, status.HTTP_403_FORBIDDEN),  # No access to wallet
            (2, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 15, status.HTTP_400_BAD_REQUEST),  # Not enough money
            (3, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 15, status.HTTP_400_BAD_REQUEST),  # Negative amount
    ))
    def test_withdraw(self, api_client, case, user_id, wallet_id, status_code):
        data = helpers.load_json_data(f'payments/withdraw/{case}')

        if not user_id:
            authorization = None
        else:
            user = get_user_model().objects.get(pk=user_id)
            authorization = helpers.access_token(user)

        response = api_client.post(
            f'/api/v1/users/wallets/{wallet_id}/withdraw/',
            data=data,
            format='json',
            HTTP_AUTHORIZATION=authorization,
        )

        assert response.status_code == status_code

    @pytest.mark.parametrize('case,user_id,wallet_id,status_code', (
            (1, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 15, status.HTTP_200_OK),  # Correct case
            (1, None, 15, status.HTTP_401_UNAUTHORIZED),  # No auth
            (1, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 16, status.HTTP_403_FORBIDDEN),  # No access to wallet
            (2, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 15, status.HTTP_400_BAD_REQUEST),  # Negative amount
    ))
    def test_deposit(self, api_client, case, user_id, wallet_id, status_code):
        data = helpers.load_json_data(f'payments/deposit/{case}')

        if not user_id:
            authorization = None
        else:
            user = get_user_model().objects.get(pk=user_id)
            authorization = helpers.access_token(user)

        response = api_client.post(
            f'/api/v1/users/wallets/{wallet_id}/deposit/',
            data=data,
            format='json',
            HTTP_AUTHORIZATION=authorization,
        )

        assert response.status_code == status_code

    @pytest.mark.parametrize('user_id,wallet_id,status_code', (
            ("af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 15, status.HTTP_200_OK),  # Correct case
            (None, 15, status.HTTP_401_UNAUTHORIZED),  # No auth
            ("af58bf95-cbd8-49e3-afea-1c35cf83b3a4", 16, status.HTTP_403_FORBIDDEN),  # No access to wallet
    ))
    def test_get_transactions(self, api_client, user_id, wallet_id, status_code):

        if not user_id:
            authorization = None
        else:
            user = get_user_model().objects.get(pk=user_id)
            authorization = helpers.access_token(user)

        response = api_client.get(
            f'/api/v1/users/wallets/{wallet_id}/transactions/',
            format='json',
            HTTP_AUTHORIZATION=authorization,
        )

        assert response.status_code == status_code
