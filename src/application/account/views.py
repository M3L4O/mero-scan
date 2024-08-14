from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (
    AccountLoginSerializer,
    AccountLogoutSerializer,
    AccountSerializer,
)
from .models import Account


class AccountRegisterView(GenericAPIView):
    serializer_class = AccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            account_data = serializer.data
            return Response(
                {"data": account_data, "message": "Conta criada com sucesso."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        account: Account = request.user
        serializer = self.serializer_class(account, data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        account: Account = request.user
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountLoginView(GenericAPIView):
    serializer_class = AccountLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status.HTTP_200_OK)


class AccountLogoutView(GenericAPIView):
    serializer_class = AccountLogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
