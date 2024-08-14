import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    username = models.CharField(max_length=100, verbose_name=_("Username"))
    email = models.EmailField(
        max_length=255, unique=True, verbose_name=_("Email Adress"), 
    )
    profile_image = models.FileField(default=None, null=True)
    description = models.CharField(max_length=255, default=None, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = AccountManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def __str__(self):
        return self.email
