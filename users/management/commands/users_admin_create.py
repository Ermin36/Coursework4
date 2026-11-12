from django.core.management import BaseCommand

from users.models import CustomUser

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = CustomUser.objects.create_superuser(email='admin@example.com', password='admin.')
        user.is_active = True
        user.save()