from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Команда установки прав доступа для группы 'Managers' "

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name="Managers")

        permissions_codenames = [
            "view_course",
            "view_lesson",
            "change_course",
            "change_lesson",
        ]

        permissions_to_add = []

        for codename in permissions_codenames:
            try:
                permission = Permission.objects.get(codename=codename)
                permissions_to_add.append(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Право '{codename}' не найдено."))

        group.permissions.add(*permissions_to_add)
        self.stdout.write(
            self.style.SUCCESS("Права успешно установлены для группы 'Managers' ")
        )
