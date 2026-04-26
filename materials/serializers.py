from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    lessons = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons(self, instance):
        """Определяем количество уроков в курсе"""
        return instance.lesson.all().count()


class CreateCourseSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = Course
        fields = "__all__"


class LessonListSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = Lesson
        fields = ("id", "title",)


class CourseListSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "title", "lessons",)

    def get_lessons(self, instance):
        """Определяем количество уроков в курсе"""
        return instance.lesson.all().count()
