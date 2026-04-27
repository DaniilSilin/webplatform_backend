from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


# Create your views here.
class RegisterView(viewsets.ModelViewSet):
    permission_class = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        