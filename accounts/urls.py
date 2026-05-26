from django.urls import path
from .views import (
    VerifyEmailView,
    CheckEmailVerifiedView,
    CompleteEmailVerifyView,
    RetrieveProfileView,
    CheckAccountNameAvailabilityView,
    CheckPasswordAvailabilityView,
    LoginView,
)
from rest_framework_simplejwt.views import TokenRefreshView

verify_email = VerifyEmailView.as_view({"post": "create"})
check_email_verified = CheckEmailVerifiedView.as_view({"post": "create"})
complete_email_verify = CompleteEmailVerifyView.as_view({"get": "list"})
check_account_name_availability = CheckAccountNameAvailabilityView.as_view({"get": "list"})
check_password_availability = CheckPasswordAvailabilityView.as_view({"get": "list"})

profile = RetrieveProfileView.as_view({"get": "retrieve"})

urlpatterns = [
    path("join/verify_email/", verify_email, name="verify_email"),
    path(
        "join/check_email_verified/", check_email_verified, name="check_email_verified"
    ),
    path(
        "join/complete_email_verify/",
        complete_email_verify,
        name="complete_email_verify",
    ),
    path(
        "join/check_account_name_availability/",
        check_account_name_availability,
        name="check_account_name_availability",
    ),
    path(
        "join/check_password_availability/",
        check_password_availability,
        name="check_password_availability",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", profile, name="retrieve_profile"),
]
