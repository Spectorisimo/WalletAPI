import helpers
import pytest

from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework import status
from wallets import repository, services
from py_currency_converter import convert


@pytest.mark.django_db
class WalletViewSetTest:

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'wallets.json', 'fees.json')

    @pytest.mark.parametrize('case,user_id,status_code', (
            ('1', 'af58bf95-cbd8-49e3-afea-1c35cf83b3a4', status.HTTP_201_CREATED),  # Correct case
            ('1', None, status.HTTP_401_UNAUTHORIZED),  # No auth
            ('2', 'af58bf95-cbd8-49e3-afea-1c35cf83b3a4', status.HTTP_400_BAD_REQUEST),  # Wallet with currency exists

    ))
    def test_create_wallet(self, api_client, case, user_id, status_code):
        data = helpers.load_json_data(f'wallets/create_wallet/{case}')

        if not user_id:
            authorization = None
        else:
            user = get_user_model().objects.get(pk=user_id)
            authorization = helpers.access_token(user)

        response = api_client.post(
            '/api/v1/users/wallets/create/',
            data=data,
            format='json',
            HTTP_AUTHORIZATION=authorization,

        )

        assert response.status_code == status_code

    @pytest.mark.parametrize('wallet_id,user_id,status_code', (
            (15, 'af58bf95-cbd8-49e3-afea-1c35cf83b3a4', status.HTTP_200_OK),  # Correct case
            (15, None, status.HTTP_401_UNAUTHORIZED),  # No auth
            (15, 'bcd36cf4-d9df-4ee7-8a29-3dc5106f9752', status.HTTP_404_NOT_FOUND),  # User hasn't accessed to wallet

    ))
    def test_get_wallet(self, api_client, wallet_id, user_id, status_code):
        if not user_id:
            authorization = None
        else:
            user = get_user_model().objects.get(pk=user_id)
            authorization = helpers.access_token(user)

        response = api_client.get(
            f'/api/v1/users/wallets/{wallet_id}/',
            format='json',
            HTTP_AUTHORIZATION=authorization,
        )

        assert response.status_code == status_code

    @pytest.mark.parametrize('case,wallet_id,user_id,status_code', (
            ('1', 15, 'af58bf95-cbd8-49e3-afea-1c35cf83b3a4', status.HTTP_200_OK),  # Correct case
            ('1', 15, None, status.HTTP_401_UNAUTHORIZED),  # No auth
            ('1', 15, 'bcd36cf4-d9df-4ee7-8a29-3dc5106f9752', status.HTTP_404_NOT_FOUND),
            # User hasn't accessed to wallet

    ))
    def test_update_wallet(self, api_client, case, wallet_id, user_id, status_code):
        data = helpers.load_json_data(f'wallets/update_wallet/{case}')

        if not user_id:
            authorization = None
        else:
            user = get_user_model().objects.get(pk=user_id)
            authorization = helpers.access_token(user)

        response = api_client.patch(
            f'/api/v1/users/wallets/{wallet_id}/update/',
            data=data,
            format='json',
            HTTP_AUTHORIZATION=authorization,
        )

        assert response.status_code == status_code


@pytest.mark.django_db
class WalletRepositoryTest:

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'wallets.json')

    def test_get_wallets(self):
        user = get_user_model().objects.get(pk="af58bf95-cbd8-49e3-afea-1c35cf83b3a4")

        assert user.wallets.count() == len(repository.WalletRepositoryV1.get_wallets(self, user=user))


@pytest.mark.django_db
class WalletServicesTest:

    @pytest.mark.parametrize('first_currency,second_currency,amount', (
            ('KZT', 'USD', 100),
            ('KZT', 'EUR', 100),
            ('EUR', 'USD', 100),
            ('EUR', 'KZT', 100),
            ('USD', 'KZT', 100),
            ('USD', 'EUR', 100),
    ))
    def test_currency_converter(self, first_currency, second_currency, amount):
        func_result = services.WalletServicesV1.currency_converter(first_currency, second_currency, amount)

        assert round(Decimal((convert(first_currency, amount=amount, to=[second_currency, ])[second_currency])),
                     2) == func_result
