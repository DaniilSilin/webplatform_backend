from rest_framework import serializers
from rest_framework.serializers import SlugField, EmailField, CharField
from rest_framework.validators import UniqueValidator

from .validators import validate_username, check_password_complexity
from .models import UserProfile, UniversalVerification


class VerifyEmailSerializer(serializers.ModelSerializer):
    token = CharField()

    class Meta:
        model = UserProfile
        fields = ["email", "token"]

    def validate_email(self, email):
        return email.lower().strip()


class CheckEmailVerifiedSerializer(serializers.ModelSerializer):
    creation_id = CharField()

    class Meta:
        model = UniversalVerification
        fields = [
            "creation_id",
        ]


class CompleteEmailVerifySerializer(serializers.ModelSerializer):
    creation_id = CharField()
    secure_token = CharField()

    class Meta:
        model = UniversalVerification
        fields = ["creation_id", "secure_token"]


class CheckAccountNameAvailabilitySerializer(serializers.Serializer):
    creation_id = CharField()
    account_name = CharField()
    count = CharField()


class CheckPasswordAvailabilitySerializer(serializers.Serializer):
    account_name = CharField()
    password = CharField()
    count = CharField()


class RegisterSerializer(serializers.ModelSerializer):
    # password = CharField()
    # token = CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "email",
        ]

    def validate_email(self, email):
        return email.lower().strip()

    # def validate(self, data):
    #     check_password_complexity(data.get("password"), data.get("username"))
    #     return data


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ["id", "username", "email"]
