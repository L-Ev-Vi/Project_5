from rest_framework import serializers

from users.models import Subscriptions

from .models import Course, Lesson
from .validators import CheckingVideoLink


class LessonSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [CheckingVideoLink("video")]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    lessons = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True)
    subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons(self, instance):
        """Определяем количество уроков в курсе"""
        return instance.lesson.all().count()

    def get_subscriptions(self, instance):
        user = self.context["request"].user
        if Subscriptions.objects.filter(user=user.pk, course=instance.pk).exists():
            return Subscriptions.objects.get(user=user.pk, course=instance.pk).subscription
        return Subscriptions.objects.create(user=user, course=instance).subscription


class CreateCourseSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = Course
        fields = "__all__"


class LessonListSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
        )


class CourseListSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "lessons",
        )

    def get_lessons(self, instance):
        """Определяем количество уроков в курсе"""
        return instance.lesson.all().count()
