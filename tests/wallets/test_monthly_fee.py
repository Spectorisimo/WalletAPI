import helpers
import pytest

from wallets import services, models, tasks


@pytest.mark.django_db
class WalletMonthlyFeeTest:

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'wallets.json', 'fees.json')

    @pytest.mark.freeze_time('2023-04-19 19:00:00')
    def test_withdraw_monthly_fee(self, api_client):
        tasks.charge_monthly_fees.delay()
        wallet = models.Wallet.objects.get(id=19)
        expected_amount = 4000 - services.WalletServicesV1.currency_converter('KZT',
                                                                              wallet.amount_currency,
                                                                              wallet.fee.amount)
        assert wallet.amount == expected_amount

    @pytest.mark.freeze_time('2023-04-19 19:00:00')
    def test_block_wallet(self, api_client):
        tasks.charge_monthly_fees.delay()
        wallet = models.Wallet.objects.get(id=16)
        assert wallet.is_active == False
