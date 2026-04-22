from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Класс определяющий модель пользователя"""

    username = None

    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Номер телефона")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватарка")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Метод определяет строковое представление объекта."""
        return f"{self.first_name} {self.last_name}"

    class Meta:
        """Добавление метаданных к модели User."""

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["last_name"]
        db_table = "users"
