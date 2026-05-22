import hmac
import time
import uuid
import requests
import sys
import json

from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail

from .models import UniversalVerification, UserProfile
from .utils import generate_random_numbers
from utils.network_utils import get_client_ip

LAST_TIMESTAMP = -1
SEQUENCE = 0

def generate_snowflake_creation_id() -> int:
    global LAST_TIMESTAMP, SEQUENCE

    ms_timestamp = int(timezone.now().timestamp() * 1000)
    passed_ms = ms_timestamp - settings.MY_APP_EPOCH

    if passed_ms == LAST_TIMESTAMP:
        SEQUENCE = (SEQUENCE + 1) & 4095
    else:
        LAST_TIMESTAMP = passed_ms
        SEQUENCE = 0
    snowflake = (passed_ms << 22) | (settings.SERVER_ID << 12) | SEQUENCE
    return snowflake

def generate_email_verification_link(email: str) -> str:
    creation_id = generate_snowflake_creation_id()

    salt = uuid.uuid4().hex
    raw_data = f"{email}{salt}"
    secure_token = hmac.new(
        key=settings.SECRET_KEY.encode('utf-8'),
        msg=f"{salt}{email}".encode('utf-8'),
        digestmod='sha384'
    ).hexdigest()

    verification = UniversalVerification.objects.create(
        email=email,
        creation_id=creation_id,
        secure_token=secure_token,
        purpose='register'
    )

    email_verify_link = f"http://localhost:3000/account/newaccountverification?stoken={verification.secure_token}&creation_id={verification.creation_id}"
    return email_verify_link


def send_mail_on_email_verify(email: str, email_verify_link: str) -> None:
    send_mail(
        subject='Подтверждение эл. почты для нового аккаунта Steam',
        message=f"Подтверждение эл. почты для нового аккаунта Steam {email_verify_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


# def generate_verification_code(email: str, purpose: str) -> str:
#     email_codes_count = UniversalVerification.objects.filter(email=email, purpose=purpose).count()
#     if (email_codes_count >= 50):
#         UniversalVerification.objects.filter(email=email, purpose=purpose).last().delete()
#     code = generate_random_numbers()
#     UniversalVerification.objects.create(email=email, code=code, purpose=purpose)
#     return code


def check_captcha(token: str, request) -> bool:
    resp = requests.post(
       "https://smartcaptcha.cloud.yandex.ru/validate",
       data={
          "secret": settings.SMARTCAPTCHA_SERVER_KEY,
          "token": token,
          "ip": get_client_ip(request)
       },
       timeout=1
    )
    server_output = resp.content.decode()
    if resp.status_code != 200:
       print(f"Allow access due to an error: code={resp.status_code}; message={server_output}", file=sys.stderr)
       return True
    return json.loads(server_output)["status"] == "ok"
