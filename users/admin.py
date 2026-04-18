from django.contrib import admin

from users.models import User


@admin.register(User)
class UserOfServiceAdmin(admin.ModelAdmin):
    """Класс регистрации и настройки отображения модели 'User' в админке"""

    list_display = (
        "email",
        "first_name",
        "last_name",
    )
    search_fields = ("last_name",)
