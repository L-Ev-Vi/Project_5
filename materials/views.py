from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import UserIsModeratorPermissions, UserInObjOrModeratorPermissions
from .models import Course, Lesson
from .serializers import (CourseSerializer,
                          LessonSerializer,
                          LessonListSerializer,
                          CourseListSerializer,
                          CreateCourseSerializer)


class CourseViewSet(viewsets.ModelViewSet):
    """Класс описывающий логику обработки HTTP запросов"""
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer
        elif self.action in ("create", "update", "partial_update"):
            return CreateCourseSerializer
        return CourseSerializer

    def get_permissions(self):
        """Создает экземпляр и возвращает список разрешений, необходимых для этого представления."""
        if self.action == "list":
            permission_classes = [AllowAny]
        elif self.action == "create":
            permission_classes = [IsAuthenticated, ~UserIsModeratorPermissions]
        elif self.action in ("update", "partial_update", "destroy"):
            permission_classes = [IsAuthenticated, UserInObjOrModeratorPermissions]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.author = self.request.user
        new_course.save()


class LessonCreateViewAPI(generics.CreateAPIView):
    """Класс отвечает за создание сущности (Урока)"""
    permission_classes = [IsAuthenticated, ~UserIsModeratorPermissions]
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.author = self.request.user
        new_lesson.save()


class LessonListViewAPI(generics.ListAPIView):
    """Класс отвечает за отображение списка сущностей (Уроков)"""
    permission_classes = [AllowAny]
    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveViewAPI(generics.RetrieveAPIView):
    """Класс отвечает за отображение одной сущности (Урока)"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateViewAPI(generics.UpdateAPIView):
    """Класс отвечает за редактирование одной сущности (Урока)"""
    permission_classes = [UserInObjOrModeratorPermissions]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyViewAPI(generics.DestroyAPIView):
    """Класс отвечает за удаление сущности (Урока)"""
    permission_classes = [UserInObjOrModeratorPermissions]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
