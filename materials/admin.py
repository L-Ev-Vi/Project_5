from django.contrib import admin

from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Класс регистрации и настройки отображения модели 'Course' в админке"""

    list_display = (
        "pk",
        "title",
    )
    list_filter = ("title",)
    search_fields = (
        "title",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Класс регистрации и настройки отображения модели 'Lesson' в админке"""

    list_display = (
        "pk",
        "title",
    )
    list_filter = ("title",)
    search_fields = (
        "title",
    )
