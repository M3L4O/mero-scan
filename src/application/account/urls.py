from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    AccountDetailView,
    AccountLoginView,
    AccountLogoutView,
    AccountRegisterView,
)

urlpatterns = [
    path("register/", AccountRegisterView.as_view(), name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", AccountLoginView.as_view(), name="login-user"),
    path("logout/", AccountLogoutView.as_view(), name="logout-user"),
    path("account/", AccountDetailView.as_view(), name="account-detail"),
]
