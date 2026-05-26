from django.core.cache import cache

from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import UniversalVerification
from .serializers import (
    RegisterSerializer,
    VerifyEmailSerializer,
    CheckEmailVerifiedSerializer,
    CompleteEmailVerifySerializer,
    UserProfileSerializer,
    CheckAccountNameAvailabilitySerializer,
    CheckPasswordAvailabilitySerializer
)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


from .services import (
    send_mail_on_email_verify,
    generate_email_verification_link,
    check_captcha,
)
from EResult import EResult


class VerifyEmailView(viewsets.ModelViewSet):
    serializer_class = VerifyEmailSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        token = serializer.data["token"]

        if not check_captcha(token, request):
            return Response(
                {"success": EResult.FAIL},
                status=status.HTTP_200_OK,
            )

        verify_link, verification = generate_email_verification_link(email)
        creation_id = verification.creation_id

        cache.set(f"auth_status_{creation_id}", "pending", timeout=3600)

        send_mail_on_email_verify(email, verify_link)

        return Response(
            {"success": EResult.OK, "creation_id": creation_id, "details": ""},
            status=status.HTTP_200_OK,
        )


class CheckEmailVerifiedView(viewsets.ModelViewSet):
    serializer_class = CheckEmailVerifiedSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        creation_id = serializer.data["creation_id"]

        cached_auth_status = cache.get(f"auth_status_{creation_id}")

        if cached_auth_status is None:
            return Response({"success": EResult.EXPIRED}, status=status.HTTP_200_OK)
        elif cached_auth_status == "verified":
            return Response({"success": EResult.OK}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"success": EResult.HANDSHAKE_ERROR}, status=status.HTTP_200_OK
            )


class CompleteEmailVerifyView(viewsets.ModelViewSet):
    serializer_class = CompleteEmailVerifySerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        creation_id = serializer.validated_data["creation_id"]
        secure_token = serializer.validated_data["secure_token"]

        try:
            verification = UniversalVerification.objects.get(
                creation_id=creation_id, secure_token=secure_token
            )
            if verification.is_used:
                return Response(
                    {"success": EResult.FAIL, "details": ""}, status=status.HTTP_200_OK
                )

            else:
                cache.set(f"auth_status_{creation_id}", "verified", timeout=3600)
                verification.is_used = True
                verification.save()

                return Response(
                    {"success": EResult.OK, "details": ""}, status=status.HTTP_200_OK
                )

        except UniversalVerification.DoesNotExist:
            return Response(
                {"success": EResult.FAIL, "details": "Неверная или устаревшая ссылка."},
                status=status.HTTP_200_OK,
            )


class CheckAccountNameAvailabilityView(viewsets.ModelViewSet):
    serializer_class = CheckAccountNameAvailabilitySerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data["username"]
        pass


class CheckPasswordAvailabilityView(viewsets.ModelViewSet):
    serializer_class = CheckPasswordAvailabilitySerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RegisterView(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        pass


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return super().post(request, *args, **kwargs)


class RetrieveProfileView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
