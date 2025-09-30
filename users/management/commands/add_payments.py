from django.core.management import BaseCommand

import users.models
from materials.models import Course, Lesson
from users.models import CustomUser, Payments


class Command(BaseCommand):
    help = "Команда для заполнения базы данных моделью 'Payments' "

    def handle(self, *args, **options):
        user, _ = CustomUser.objects.get_or_create(email="test-user@email.ru")

        course1, _ = Course.objects.get_or_create(
            name="Русский язык",
            description="Изучение русского языка",
        )
        course2, _ = Course.objects.get_or_create(
            name="Математика",
            description="Изучение математики",
        )

        lesson1, _ = Lesson.objects.get_or_create(
            name="Алгебра", description="Квадратный корень", course=course2
        )
        lesson2, _ = Lesson.objects.get_or_create(
            name="Геометрия", description="Косинусы синусы", course=course2
        )
        lesson3, _ = Lesson.objects.get_or_create(
            name="Прилагательные", description="Изучение прилагательных", course=course1
        )
        lesson4, _ = Lesson.objects.get_or_create(
            name="Глаголы", description="Изучение глаголов", course=course1
        )

        payments_data = [
            {
                "user": user,
                "course_payment": course2,
                "lesson_payment": lesson1,
                "payment_amount": 10000,
                "payment_method": users.models.CASH,
            },
            {
                "user": user,
                "course_payment": course2,
                "lesson_payment": lesson2,
                "payment_amount": 11000,
                "payment_method": users.models.CARD,
            },
            {
                "user": user,
                "course_payment": course1,
                "lesson_payment": lesson3,
                "payment_amount": 12000,
                "payment_method": users.models.SBP,
            },
            {
                "user": user,
                "course_payment": course1,
                "lesson_payment": lesson4,
                "payment_amount": 13000,
            },
        ]

        for data in payments_data:
            data, created = Payments.objects.get_or_create(**data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Платежные данные: {data} внесены в базу данных."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Платежные данные: {data} уже существуют в базе данных."
                    )
                )
