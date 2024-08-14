from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, NotAcceptable
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False, write_only=True)
    description = serializers.CharField(required=False)
    profile_image = serializers.CharField(required=False)

    class Meta:
        model = Account
        fields = [
            "username",
            "email",
            "password",
            "description",
            "profile_image",
        ]

    def validate(self, data):
        allowed_fields = (
            "username",
            "email",
            "password",
            "description",
            "profile_image",
        )
        fields = {}
        for k, v in data.items():
            if k in allowed_fields:
                if "email" == k and Account.objects.filter(email=v).exists():
                    raise NotAcceptable("Email já cadastrado.")
                fields[k] = v

        return fields

    def create(self, validated_data):
        account = Account.objects.create_user(**validated_data)

        return account

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            if k == "password":
                instance.set_password(v)
            else:
                setattr(instance, k, v)

        instance.save()
        return instance


class AccountLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=155)
    password = serializers.CharField(max_length=255, write_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Account
        fields = ["email", "password", "access", "refresh"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        request = self.context.get("request")

        account = authenticate(request=request, email=email, password=password)

        if not account:
            raise AuthenticationFailed("Credenciais inválidas.")

        tokens = account.tokens()

        return {
            "email": account.email,
            "access": str(tokens.get("access")),
            "refresh": str(tokens.get("refresh")),
        }


class AccountLogoutSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField()

    class Meta:
        model = Account
        fields = ["refresh"]

    def validate(self, attrs):
        self.token = attrs.get("refresh")
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return None
