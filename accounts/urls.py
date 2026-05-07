from django.urls import path
from .views import LoginView, RegisterView, RetrieveProfileView
from rest_framework_simplejwt.views import TokenRefreshView


register = RegisterView.as_view({"post": "create"})
profile = RetrieveProfileView.as_view({"get": "retrieve"})

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", profile, name="retrieve_profile"),
]
