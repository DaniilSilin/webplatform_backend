from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import UserProfile

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        return Response("", status=status.HTTP_201_CREATED)



class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer 
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return super().post(request, *args, **kwargs)