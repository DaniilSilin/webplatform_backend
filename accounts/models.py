from django.conf import settings
from django.db import models

from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    is_profile_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username


class UniversalVerification(models.Model):
    PURPOSE_CHOICES = [
        ('register', 'Регистрация нового аккаунта'),
        ('email_change', 'Смена текущей почты'),
        ('password_reset', 'Сброс/Восстановление пароля'),
        ('2fa_code', 'Двухфакторная аутентификация'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        verbose_name="Пользователь (если создан)"
    )
    email = models.EmailField(verbose_name="Email для отправки/проверки")
    secure_token = models.CharField(
        max_length=96, 
        unique=True, 
        null=True, 
        blank=True, 
        verbose_name="Секретный токен ссылки (SHA-384)"
    )
    creation_id = models.BigIntegerField(unique=True, null=True, blank=True, verbose_name="ID сессии Snowflake")
    code = models.CharField(max_length=6, blank=True, null=True, verbose_name="Короткий код подтверждения")
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, verbose_name="Тип проверки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_used = models.BooleanField(default=False, verbose_name="Использован ли")

    class Meta:
        verbose_name = 'Запрос верификации'
        verbose_name_plural = 'Запросы верификации'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email}: {self.purpose}"
