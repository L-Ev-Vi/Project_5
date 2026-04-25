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
