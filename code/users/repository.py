from django.db import transaction
from rest_framework.generics import get_object_or_404
from . import models
from typing import OrderedDict, Protocol
from rest_framework import exceptions


class UserRepositoryInterface(Protocol):

    @staticmethod
    def create_user(data: OrderedDict) -> models.CustomUser:
        """
        Creates a new user with the given data.

        Args:
            data (OrderedDict): A dictionary containing user data.

        Returns:
            models.CustomUser | None: The created user object if successful, None otherwise.
        """
        ...

    @staticmethod
    def get_user(data: OrderedDict) -> models.CustomUser:
        """
        Returns the `CustomUser` object corresponding to the provided phone number and password, if they match.

        Args:
            data (OrderedDict): An ordered dictionary containing the phone number and password to authenticate the user.

        Returns:
            models.CustomUser: A `CustomUser` object that matches the provided phone number and password.

        Raises:
            models.CustomUser.DoesNotExist: If no `CustomUser` object is found
             that matches the provided phone number and password.
        """
        ...

    @staticmethod
    def update_password(data: OrderedDict) -> None:
        """
        Updates the password of the user identified by the provided phone number.

        Args:
            data (OrderedDict): A dictionary-like object containing the data needed to update the password.
                It must have the following keys:
                - phone_number (str): The phone number associated with the user account.
                - new_password (str): The new password to be set for the user account.

        Raises:
            Http404: If the user with the provided phone number does not exist.

        Returns:
            None.
        """
        ...

    @staticmethod
    def update_personal_info(data: OrderedDict) -> None:
        """
        Updates personal information (first_name,last_name,profile_image) for a user with the specified phone number.

        Args:
            data (OrderedDict): A dictionary-like object containing the personal information to be updated.
            Phone number must be included.
            This may not include all fields to be updated.

        Returns:
            None
        """
        ...


class UserRepositoryV1:

    def create_user(self, data: OrderedDict) -> models.CustomUser | None:
        with transaction.atomic():
            user = models.CustomUser.objects.create_user(**data)

        return user

    def get_user(self, data: OrderedDict) -> models.CustomUser:
        user = get_object_or_404(models.CustomUser, phone_number=data['phone_number'])

        if not user.check_password(data['password']):
            raise exceptions.AuthenticationFailed('Invalid password')

        return user

    def update_password(self, data: OrderedDict) -> None:
        user = get_object_or_404(models.CustomUser, phone_number=data['phone_number'])
        user.set_password(data['new_password'])
        user.save()

    def update_personal_info(self, data: OrderedDict) -> None:
        phone_number = data.pop('phone_number')
        models.CustomUser.objects.update_or_create(phone_number=phone_number, defaults={**data})
