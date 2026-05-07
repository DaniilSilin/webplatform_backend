from rest_framework import serializers
from rest_framework.serializers import SlugField, EmailField, CharField
from rest_framework.validators import UniqueValidator

from .validators import validate_username, check_password_complexity

from .models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = CharField()
    # token = CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ["email", "username", "password"]

    def validate_email(self, email):
        return email.lower().strip()

    def validate(self, data):
        check_password_complexity(data.get("password"), data.get("username"))
        return data


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ["id", "username", "email"]
