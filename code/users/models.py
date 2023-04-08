import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save()
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        user = self._create_user(email, password, **extra_fields)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)

    profile_image = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    username = None

    def __str__(self):
        return str(self.phone_number)
