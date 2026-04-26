from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from config import settings
from materials.models import Course, Lesson


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


class Payments(models.Model):
    """Класс определяющий модель платежи"""

    PAYMENT_METHOD = [
        ("cash", "Наличные"),
        ("translation", "Перевод"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    date = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Курс")
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Курс")
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Сумма оплаты")
    method = models.CharField(choices=PAYMENT_METHOD, default="translation", verbose_name="Оценка")

    def __str__(self):
        """Метод определяет строковое представление объекта."""
        return (
            f"{self.user.first_name} {self.user.last_name} - "
            f"{self.course.title if self.course else self.lesson.title} - {self.amount}"
        )

    class Meta:
        """Добавление метаданных к модели Payments."""

        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
        ordering = ["-date"]
        db_table = "payments"
