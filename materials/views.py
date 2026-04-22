from rest_framework import generics, viewsets

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Класс описывающий логику обработки HTTP запросов"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonCreateViewAPI(generics.CreateAPIView):
    """Класс отвечает за создание сущности (Урока)"""

    serializer_class = LessonSerializer


class LessonListViewAPI(generics.ListAPIView):
    """Класс отвечает за отображение списка сущностей (Уроков)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveViewAPI(generics.RetrieveAPIView):
    """Класс отвечает за отображение одной сущности (Урока)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateViewAPI(generics.UpdateAPIView):
    """Класс отвечает за редактирование одной сущности (Урока)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyViewAPI(generics.DestroyAPIView):
    """Класс отвечает за удаление сущности (Урока)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
