from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

from materials.models import Course, Lesson
from users.models import Payments, User


class Command(BaseCommand):
    help = "Добавление урока и кирса в базу данных для тестирования"

    def handle(self, *args, **options):
        """Метод добавления данных в БД"""

        Lesson.objects.all().delete()  # предварительное удаление всех данных из таблицы
        Course.objects.all().delete()  # предварительное удаление всех данных из таблицы
        Payments.objects.all().delete()  # предварительное удаление всех данных из таблицы
        User.objects.all().delete()  # предварительное удаление всех данных из таблицы
        Group.objects.all().delete()  # предварительное удаление всех данных из таблицы

        # сброс инкремента (счётчика 'id' до 1)
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE payments_id_seq RESTART WITH 1")  # чистый SQL запрос
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1")  # чистый SQL запрос
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE auth_group_permissions_id_seq RESTART WITH 1")  # чистый SQL запрос
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE auth_group_id_seq RESTART WITH 1")  # чистый SQL запрос
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE lessons_id_seq RESTART WITH 1")  # чистый SQL запрос
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE courses_id_seq RESTART WITH 1")  # чистый SQL запрос
        # данные операции были выполнены в рамках тестирования и не рекомендуются для массового использования

        call_command(
            "loaddata",
            "users/management/commands/user_payments_groups_lesson_course_fixture.json",
            "--ignorenonexistent",
        )

        self.stdout.write(
            self.style.SUCCESS(
                'id=1 "Администратор" {"email": "admin@mail.ru", "password": "1234"}\n'
                'id=2 "Модератор" {"email": "tom@doe.ru", "password": "123asd"}\n'
                'id=3 "Пользователь" {"email": "jon@doe.ru", "password": "456"}\n'
            )
        )

        # id=1
        # Администратор
        # {
        #     "email": "admin@mail.ru",
        #     "password": "1234"
        # }

        # id=2
        # Модератор
        # {
        #     "email": "tom@doe.ru",
        #     "password": "123asd"
        # }

        # id=3
        # Пользователь
        # {
        #     "email": "jon@doe.ru",
        #     "password": "456"
        # }
