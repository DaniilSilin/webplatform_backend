from django.db import models
from django.conf import settings


class Channel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Владелец канала",
        related_name="channels",
    )
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Адрес канала")
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField("Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    avatar_small = models.ImageField(
        upload_to="channels/avatars/small/", verbose_name="Аватар (урезанный)"
    )
    avatar = models.ImageField(
        upload_to="channels/avatars/original/", verbose_name="Аватар"
    )
    banner = models.ImageField(
        upload_to="channels/banners/original/", verbose_name="Баннер"
    )
    banner_small = models.ImageField(
        upload_to="channels/banners/small/", verbose_name="Баннер (урезанный)"
    )

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

    def __str__(self):
        return self.title
