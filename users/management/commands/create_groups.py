from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


MANAGER_PERMISSIONS = [
    "view_all_mailings",
    "disable_mailings",
    "view_all_recipients",
    "view_all_messages",
    "view_service_users",
    "block_users",
]

class Command(BaseCommand):
    """Создание группы 'Менеджеры' и назначение ей прав."""

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Менеджеры")

        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'Менеджеры' создана"))
        else:
            self.stdout.write("Группа 'Менеджеры' уже существует")

        for codename in MANAGER_PERMISSIONS:
            perms = Permission.objects.filter(codename=codename)
            if perms.count() == 1:
                group.permissions.add(perms.first())
                self.stdout.write(f"Добавлено право: {codename}")
            elif perms.count() > 1:
                self.stdout.write(self.style.ERROR(
                    f"⚠ Ошибка: найдено несколько прав с codename '{codename}'"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"⚠ Право '{codename}' не найдено — сделай миграции!"
                ))
        self.stdout.write(self.style.SUCCESS("Группа 'Менеджеры' успешно создана"))
