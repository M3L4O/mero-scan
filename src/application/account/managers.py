from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class AccountManager(BaseUserManager):
    def email_validator(self, email: str):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Por favor, entre com um endereço de email válido."))

    def create_user(self, **fields):
        if "email" in fields.keys():
            email = self.normalize_email(fields.get("email"))
            self.email_validator(email)
        else:
            raise ValueError(_("Endereço de email é requerido."))

        if "password" in fields.keys():
            password = fields.pop("password")
            user = self.model(**fields)
            user.set_password(password)
        else:
            raise ValueError(_("Senha é requerida."))
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is staff must be true for admin user"))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("is superuser must be true for admin user"))

        user = self.create_user(email=email, password=password, **extra_fields)
        user.save(using=self._db)
        return user
