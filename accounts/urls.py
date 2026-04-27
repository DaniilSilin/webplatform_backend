from django.contrib import admin
from django.urls import path, include

from .views import RegisterView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

register = RegisterView.as_view({"post": "create"})

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]