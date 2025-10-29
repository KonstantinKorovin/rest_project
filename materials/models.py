from django.db import models


class Course(models.Model):
    """Модель 'Курс'"""

    name = models.CharField(verbose_name="Название курса")
    preview = models.ImageField(
        verbose_name="Фотография", upload_to="materials/photo/", blank=True, null=True
    )
    description = models.TextField(verbose_name="Описание курса", blank=True, null=True)
    price = models.IntegerField(
        default=0, verbose_name="Стоимость курса"
    )
    stripe_course_id = models.CharField(
        max_length=50,
        verbose_name="id_stripe",
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        to="users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="Владелец курса",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель 'Урок'"""

    name = models.CharField(verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока", blank=True, null=True)
    preview = models.ImageField(
        verbose_name="Фотография", upload_to="materials/photo/", blank=True, null=True
    )
    link_to_the_video = models.CharField(
        verbose_name="Ссылка на видео", blank=True, null=True
    )
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        to="users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="Владелец урока",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
