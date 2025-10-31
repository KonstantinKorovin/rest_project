from celery import shared_task
from django.core.mail import send_mail

from users.models import Subscription


@shared_task
def send_update_notification_email(course_id, course_name):
    try:
        subscribers = Subscription.objects.filter(course_id=course_id).values_list(
            "user__email", flat=True
        )
        if not subscribers:
            print(f"Нет подписчиков для курса ID {course_id}. Письма не отправлены.")
            return
        subject = f"Обновление курса: {course_name}"
        message = (
            f"Привет!\n\n"
            f"Рады сообщить, что в курсе '{course_name}' появились новые материалы.\n"
            f"Заходите, чтобы посмотреть обновления!"
        )
        sender_email = "ryan337@mail.ru"
        send_mail(subject, message, sender_email, subscribers, fail_silently=False)
        print(
            f"Успешно отправлено {len(subscribers)} уведомлений для курса '{course_name}'."
        )

    except Exception as e:
        print(f"Ошибка при отправке уведомлений для курса ID {course_id}: {e}")
