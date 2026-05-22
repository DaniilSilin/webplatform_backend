from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserProfile
from .serializers import UserProfileSerializer, RegisterSerializer, VerifyEmailSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .services import send_mail_on_email_verify, generate_email_verification_link, check_captcha


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
                {"error": "Вы не прошли проверку на робота!"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        verify_link = generate_email_verification_link(email)
        send_mail_on_email_verify(email, verify_link)

        return Response({"detail": "Account successfully created."}, status=status.HTTP_201_CREATED)


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