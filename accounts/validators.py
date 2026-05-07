import re
from pathlib import Path
from django.conf import settings
from rest_framework import serializers

path_to_most_common_passwords = Path(
    settings.BASE_DIR, "accounts/most_common_passwords.txt"
)

if path_to_most_common_passwords.exists():
    with open(path_to_most_common_passwords, "r", encoding="utf-8") as f:
        most_common_passwords = {line.strip() for line in f if line.strip()}


def validate_not_common_password(password):
    if password in most_common_passwords:
        raise serializers.ValidationError("Твой текст ошибки")
    return password


def validate_username(username):
    if len(username) < 3 or len(username) > 35:
        raise serializers.ValidationError(
            "Username must be between 3 and 35 characters long."
        )
    return username


def check_password_complexity(password, username):
    password_regex = r"^(?=.*[^\W\d_])(?=.*\d)(?=.*[^\w\s]).{8,35}$"

    if username.lower().strip() == password.lower().strip():
        raise serializers.ValidationError("Username and password are matched.")

    if not re.match(password_regex, password):
        raise serializers.ValidationError("Password does not meet requirements.")

    validate_not_common_password(password)
    return password
