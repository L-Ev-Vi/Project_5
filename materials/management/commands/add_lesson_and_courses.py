from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

from materials.models import Lesson, Course


class Command(BaseCommand):
    help = "Добавление урока и кирса в базу данных для тестирования"

    def handle(self, *args, **options):
        """Метод добавления данных в БД"""

        Lesson.objects.all().delete()  # предварительное удаление всех данных из таблицы
        Course.objects.all().delete()  # предварительное удаление всех данных из таблицы

        # сброс инкремента (счётчика 'id' до 1)
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE lessons_id_seq RESTART WITH 1")  # чистый SQL запрос
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE courses_id_seq RESTART WITH 1")  # чистый SQL запрос
        # данные операции были выполнены в рамках тестирования и не рекомендуются для массового использования

        call_command(
            "loaddata",
            "materials/management/commands/lesson_course_fixture.json",
            "--ignorenonexistent")
