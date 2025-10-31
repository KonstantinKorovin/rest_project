from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import CustomUser


@shared_task
def block_inactive_users():
    thirty_days_ago = timezone.now() - timedelta(days=30)

    inactive_users = CustomUser.objects.filter(is_active=True).filter(
        last_login__lt=thirty_days_ago
    )

    users_never_logged_in = CustomUser.objects.filter(
        is_active=True, last_login__is_null=True, date_joined__lt=thirty_days_ago
    )

    users_to_block = inactive_users | users_never_logged_in

    count = users_to_block.update(is_active=False)

    print(
        f"[{timezone.now()}] Celery Beat: Заблокировано {count} неактивных пользователей."
    )

    return f"Successfully blocked {count} users."
