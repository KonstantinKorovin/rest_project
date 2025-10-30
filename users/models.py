from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


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


SBP, CARD, CASH = "SBP", "Card", "Cash"

PAYMENT_METHODS = [
    (SBP, "Система быстрых платежей"),
    (CARD, "Банковская карта"),
    (CASH, "Наличные"),
]


class Payments(models.Model):
    """Модель 'Платежи'"""

    user = models.ForeignKey(
        to=CustomUser, on_delete=models.CASCADE, related_name="users"
    )
    date_payment = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    course_payment = models.ForeignKey(
        to=Course, on_delete=models.CASCADE, related_name="courses"
    )
    lesson_payment = models.ForeignKey(
        to=Lesson, on_delete=models.CASCADE, related_name="lessons"
    )
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=4,
        verbose_name="Способ оплаты",
        choices=PAYMENT_METHODS,
        default=CASH,
    )
    owner = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Плательщик",
        blank=True,
        null=True,
    )
    link_to_the_payment = models.CharField(
        verbose_name="Ссылка на оплату", blank=True, null=True
    )
    stripe_session_id = models.CharField(
        max_length=255, verbose_name="ID сессии Stripe", blank=True, null=True
    )
    is_paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Subscription(models.Model):
    """Модель 'Подписка'"""

    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="follower",
        verbose_name="Подписчик",
    )
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="follower_course",
        verbose_name="Курс подписчика",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
