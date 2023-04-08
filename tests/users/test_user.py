import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
import helpers


@pytest.mark.django_db
class UserViewTest(object):
    code = '1111'

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json')

    @pytest.mark.parametrize('case,code,status_code', (
            ('1', code, status.HTTP_201_CREATED),  # Correct case
            ('2', code, status.HTTP_400_BAD_REQUEST),  # No email in credentials
            ('3', code, status.HTTP_400_BAD_REQUEST),  # No phone number in credentials
            ('4', code, status.HTTP_400_BAD_REQUEST),  # No password in credentials
            ('5', code, status.HTTP_400_BAD_REQUEST),  # Invalid phone number
            ('6', code, status.HTTP_400_BAD_REQUEST),  # User with this phone number already exists
            ('7', code, status.HTTP_400_BAD_REQUEST),  # User with this email already exists
            ('1', '2222', status.HTTP_400_BAD_REQUEST),  # Incorrect verification code

    ))
    def test_create_user(self, api_client, mocker, case, code, status_code):
        mocker.patch('users.services.UserServicesV1._generate_code', return_value=self.code)

        data = helpers.load_json_data(f'users/create_user/{case}')

        response = api_client.post(
            '/api/v1/users/create/',
            data=data,
            format='json',
        )

        data = {**response.data, 'code': code}
        response = api_client.post(
            '/api/v1/users/verify/',
            data=data,
            format='json',
        )
        assert response.status_code == status_code

    @pytest.mark.parametrize('case,status_code', (
            ('1', status.HTTP_200_OK),  # Correct case
            ('2', status.HTTP_401_UNAUTHORIZED),  # Incorrect password
            ('3', status.HTTP_404_NOT_FOUND),  # User with this phone number doesn't exist
    ))
    def test_create_token(self, api_client, case, status_code):
        data = helpers.load_json_data(f'users/create_token/{case}')

        response = api_client.post(
            '/api/v1/users/token/create/',
            data=data,
            format='json',
        )

        assert response.status_code == status_code

    @pytest.mark.parametrize('case,code,user_id,status_code', (
            ('1', code, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", status.HTTP_200_OK),  # Correct case
            ('2', code, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", status.HTTP_400_BAD_REQUEST),  # No password
            ('3', code, "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", status.HTTP_400_BAD_REQUEST),  # No new password
            ('1', '2222', "af58bf95-cbd8-49e3-afea-1c35cf83b3a4", status.HTTP_400_BAD_REQUEST),  # Incorrect code
            ('1', code, None, status.HTTP_401_UNAUTHORIZED),  # No auth
    ))
    def test_update_user_password(self, api_client, case, code, user_id, status_code, mocker):
        mocker.patch('users.services.UserServicesV1._generate_code', return_value=self.code)

        data = helpers.load_json_data(f'users/update_password/{case}')

        if not user_id:
            authorization = None
        else:
            user = get_user_model().objects.get(pk=user_id)
            authorization = helpers.access_token(user)

        response = api_client.post(
            '/api/v1/users/password/update/',
            data=data,
            format='json',
            HTTP_AUTHORIZATION=authorization,
        )

        data = {**response.data, 'code': code}

        response = api_client.patch(
            '/api/v1/users/password/verify/',
            data=data,
            format='json',
            HTTP_AUTHORIZATION=authorization,
        )

        assert response.status_code == status_code

    @pytest.mark.parametrize('case,user_id,status_code', (
            ('1', 'af58bf95-cbd8-49e3-afea-1c35cf83b3a4', status.HTTP_200_OK),  # Correct case
            ('1', None, status.HTTP_401_UNAUTHORIZED),  # No auth
    ))
    def test_update_personal_info(self, api_client, case, user_id, status_code):
        data = helpers.load_json_data(f'users/update_personal_info/{case}')

        if not user_id:
            authorization = None
        else:
            user = get_user_model().objects.get(pk=user_id)
            authorization = helpers.access_token(user)

        response = api_client.patch(
            '/api/v1/users/update/',
            data=data,
            format='json',
            HTTP_AUTHORIZATION=authorization,
        )

        assert response.status_code == status_code

    @pytest.mark.parametrize('user_id,status_code', (
            ('af58bf95-cbd8-49e3-afea-1c35cf83b3a4', status.HTTP_200_OK),  # Correct case
            (None, status.HTTP_401_UNAUTHORIZED),  # No auth
    ))
    def test_get_user(self, api_client, user_id, status_code):
        if not user_id:
            authorization = None
        else:
            user = get_user_model().objects.get(pk=user_id)
            authorization = helpers.access_token(user)

        response = api_client.get(
            '/api/v1/users/',
            HTTP_AUTHORIZATION=authorization,
        )

        assert response.status_code == status_code
