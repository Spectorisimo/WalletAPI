import random
import uuid

from . import repository
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from typing import Protocol, OrderedDict
from rest_framework_simplejwt import tokens


class UserServicesInterface(Protocol):

    @staticmethod
    def create_user(data: OrderedDict) -> dict:
        """
        Creates a new user verification session for the given phone number and returns a session ID.
        The user is not created until the verification process is complete.

        Args:
            data (OrderedDict): A dictionary containing user data, including the phone number.

        Returns:
            dict: A dictionary containing the session_id which is used to retrieve
            the user's data and verification code from the cache.

        Raises:
            None.
        """

        ...

    @staticmethod
    def _verify_phone_number(data: OrderedDict) -> str:
        """
         Generate a verification code and send it to the user's phone number.

         Args:
             data (OrderedDict): A dictionary containing user data.
                 The dictionary must contain the following key:
                 - phone_number (str): The phone number of the user to be verified.

         Returns:
             str: The session ID used to identify the user data and verification code in the cache.

         Note:
             This method generates a verification code and sends it to the user's phone number using
             the `_send_sms` method. The user data and verification code are stored in the cache using
             a session ID, method "_generate_session_id" generates the session ID,which is returned by this method.
         """
        ...

    @staticmethod
    def verify_user(data: OrderedDict) -> bool | None:
        """
        Verify user data and create a new user if verification succeeds.
        Sends email to user about successful registration.

        Args:
            data (OrderedDict): A dictionary containing user data and verification code.
                The dictionary must contain the following keys:
                - session_id (str): The session ID of the user to be verified.
                - code (str): The verification code entered by the user.

        Returns:
            bool: True if user verification succeeds and a new user is created, False otherwise.

        Raises:
            ValidationError: If the session ID is invalid or the verification code is incorrect.

        Note:
            The `session_id` is used to retrieve user data and verification code from the cache.
            The `code` key in the `data` dictionary should contain the code entered by the user.
        """
        ...

    @staticmethod
    def update_password(data: OrderedDict) -> dict:
        """
        Starts the updating user's password process and initiates the phone number verification process.
        The password is not updated until the verification process is complete.

        Args:
            data (OrderedDict): A dictionary containing the user's phone number and new password.

        Returns:
            dict: A dictionary containing the session_id which is used to retrieve
            the userdata(phone number,old and new passwords) and verification code from the cache.
        """
        ...

    @staticmethod
    def verify_update_password(data: OrderedDict) -> bool | None:
        """
        Verifies the user and updates the user's password.

        Args:
            data (OrderedDict): A dictionary containing user data and verification code.
                The dictionary must contain the following keys:
                - session_id (str): The session ID of the user to be verified.
                - code (str): The verification code entered by the user.

        Returns:
            bool: True if user verification succeeds and the user's password is updated, else None.

        Raises:
            ValidationError: If the session ID is invalid or the verification code is incorrect.

        Note:
            The `session_id` is used to retrieve userdata(phone number,old and new passwords)
            and verification code from the cache.
            The `code` key in the `data` dictionary should contain the code entered by the user.
        """
        ...

    @staticmethod
    def create_token(data: OrderedDict) -> bool | None:
        """
        Creates access and refresh tokens for the provided user data.

        Args:
            data (OrderedDict): A dictionary containing the user's phone number and password.

        Returns:
            A dictionary containing the access token and refresh token as strings.

        Raises:
            ValidationError: If the user data is invalid or the user doesn't exist.
        """
        ...

    @staticmethod
    def update_personal_info(data: OrderedDict) -> bool | None:
        """
        Updates personal information (first_name,last_name,profile_image) for a user with the specified phone number.

        Args:
            data (OrderedDict): A dictionary-like object containing the personal information to be updated.
            Phone number must be included.
            This may not include all fields to be updated.

        Returns:
        bool: True if the update was successful.

        Raises:
        None
        """
        ...


class UserServicesV1:
    user_repo: repository.UserRepositoryInterface = repository.UserRepositoryV1()

    def create_user(self, data: OrderedDict) -> dict:
        session_id = self._verify_phone_number(data)
        return {
            'session_id': session_id
        }

    def verify_user(self, data: OrderedDict) -> bool | None:
        user_data = cache.get(data['session_id'])
        code_from_user = data['code']
        verification_code = user_data.pop('code')

        if not user_data:
            raise ValidationError
        if code_from_user != verification_code:
            raise ValidationError

        user = self.user_repo.create_user(user_data)
        self._send_mail(user.email)
        return True

    def update_password(self, data: OrderedDict) -> dict:
        self.user_repo.get_user(data)

        session_id = self._verify_phone_number(data)
        return {
            'session_id': session_id
        }

    def verify_update_password(self, data: OrderedDict) -> bool | None:
        new_password_data = cache.get(data['session_id'])
        code_from_user = data['code']
        verification_code = new_password_data.pop('code')

        if not new_password_data:
            raise ValidationError
        if code_from_user != verification_code:
            raise ValidationError

        self.user_repo.update_password(new_password_data)
        return True

    def update_personal_info(self, data: OrderedDict) -> bool | None:
        self.user_repo.update_personal_info(data)
        return True

    def create_token(self, data: OrderedDict) -> dict:
        user = self.user_repo.get_user(data)
        access_token = tokens.AccessToken.for_user(user=user)
        refresh_token = tokens.RefreshToken.for_user(user=user)
        return {
            'access_token': str(access_token),
            'refresh_token': str(refresh_token),
        }

    def _verify_phone_number(self, data: OrderedDict):
        phone_number = data['phone_number']
        code = self._generate_code()
        self._send_sms(phone_number, code)
        session_id = self._generate_session_id()
        cache.set(session_id, {'code': code, **data}, timeout=300)
        return session_id

    @staticmethod
    def _send_mail(email: str) -> None:
        print(f'email has been sent to {email}')

    @staticmethod
    def _send_sms(phone_number: str, code: str) -> None:
        print(f'SMS CODE {code} has been sent to {phone_number}')

    @staticmethod
    def _generate_code() -> str:
        return ''.join(random.choices('0123456789', k=4))

    @staticmethod
    def _generate_session_id() -> str:
        return str(uuid.uuid4())
