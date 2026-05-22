from django.urls import path
from .views import LoginView, VerifyEmailView, RetrieveProfileView
from rest_framework_simplejwt.views import TokenRefreshView

verify_email = VerifyEmailView.as_view({"post": "create"})
profile = RetrieveProfileView.as_view({"get": "retrieve"})

urlpatterns = [
    path("verify_email/", verify_email, name="verify_email"),


    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", profile, name="retrieve_profile"),
]
