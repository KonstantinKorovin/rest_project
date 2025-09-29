from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель 'Пользователь'"""

    email = models.EmailField(verbose_name="E-mail пользователя", unique=True)
    phone_number = models.CharField(
        max_length=15, verbose_name="Номер телефона", blank=True, null=True, unique=True
    )
    city = models.CharField(verbose_name="Город пользователя", blank=True, null=True)
    avatar = models.ImageField(
        verbose_name="Фотография пользователя",
        upload_to="users/photo/",
        default="users/photo/default.png",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
