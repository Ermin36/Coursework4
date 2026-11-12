
from django.core.management import BaseCommand

from django.contrib.auth.models import Group, Permission


MANAGER_PERMISSIONS = [
    'view_all_clients',
    'view_all_mailings',
    'disable_mailing',
    'view_all_mailingattempts',
]


class Command(BaseCommand):
    help = 'Создаёт группу Manager с правами менеджера'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Manager')

        permissions = Permission.objects.filter(codename__in=MANAGER_PERMISSIONS)

        # Проверяем, что все права найдены — чтобы опечатка не прошла молча
        found = {p.codename for p in permissions}
        missing = set(MANAGER_PERMISSIONS) - found
        if missing:
            self.stderr.write(
                f'Права не найдены: {", ".join(missing)}. '
                f'Проверь Meta.permissions моделей и выполни migrate.'
            )
            return

        group.permissions.set(permissions)
        group.save()

        if created:
            self.stdout.write(self.style.SUCCESS('Группа Manager создана, права выданы.'))
        else:
            self.stdout.write(self.style.SUCCESS('Группа Manager уже существовала, права обновлены.'))