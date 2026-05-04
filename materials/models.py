from django.db import models

from config import settings


class Lesson(models.Model):
    """Класс определяющий модель 'Урока'"""

    title = models.CharField(max_length=200, verbose_name="Название Урока")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    picture = models.ImageField(upload_to="picture/", blank=True, null=True, verbose_name="Превью")
    video = models.URLField(max_length=500, null=True, blank=True, verbose_name="Ссылка на видео")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Пользователь",
    )

    def __str__(self) -> str:
        """Метод определяет строковое представление объекта."""
        return f"{self.title}"

    class Meta:
        """Клас который добавляет метаданные к модели Lesson."""

        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title"]
        db_table = "lessons"


class Course(models.Model):
    """Класс определяющий модель 'Курса'"""

    title = models.CharField(max_length=100, verbose_name="Название курса")
    picture = models.ImageField(upload_to="picture/", blank=True, null=True, verbose_name="Превью")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    lesson = models.ManyToManyField(Lesson, blank=True, related_name="lessons", verbose_name="Уроки")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Пользователь",
    )

    def __str__(self) -> str:
        """Метод определяет строковое представление объекта."""
        return f"{self.title}"

    class Meta:
        """Клас который добавляет метаданные к модели Course."""

        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]
        db_table = "courses"
