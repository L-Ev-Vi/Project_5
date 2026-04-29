from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создание Администратора."

    def handle(self, *args, **options):
        """Метод добавления данных в БД"""

        User = get_user_model()
        user = User.objects.create(email="admin@sky.com", first_name="Admin", last_name="Admine")
        user.set_password("1234")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS("'Admin' успешно создан!"))
