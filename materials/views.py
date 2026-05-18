from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson
from .paginators import MyPagination
from .permissions import UserInObjOrModeratorPermissions, UserIsAuthorPermissions, UserIsModeratorPermissions
from .serializers import (
    CourseListSerializer,
    CourseSerializer,
    CreateCourseSerializer,
    LessonListSerializer,
    LessonSerializer,
)
from .tasks import newsletter_about_updates


class CourseViewSet(viewsets.ModelViewSet):
    """Класс описывающий логику обработки HTTP запросов"""

    pagination_class = MyPagination

    def get_queryset(self):
        if self.action == "list":
            if self.request.user.groups.filter(name="Модераторы").exists():
                return Course.objects.all()
            return Course.objects.filter(author=int(self.request.user.pk))
        return Course.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer
        elif self.action in ("create", "update", "partial_update"):
            return CreateCourseSerializer
        return CourseSerializer

    def get_permissions(self):
        """Создает экземпляр и возвращает список разрешений, необходимых для этого представления."""
        if self.action == "retrieve":
            permission_classes = [IsAuthenticated, UserIsAuthorPermissions | UserIsModeratorPermissions]
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_update(self, serializer):
        instance = serializer.save()
        id = instance.id
        newsletter_about_updates.delay(id, "course")


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

    permission_classes = [IsAuthenticated]
    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all()
    pagination_class = MyPagination

    def get_queryset(self):
        if self.request.user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(author=int(self.request.user.pk))


class LessonRetrieveViewAPI(generics.RetrieveAPIView):
    """Класс отвечает за отображение одной сущности (Урока)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [UserIsAuthorPermissions | UserIsModeratorPermissions]


class LessonUpdateViewAPI(generics.UpdateAPIView):
    """Класс отвечает за редактирование одной сущности (Урока)"""

    permission_classes = [UserInObjOrModeratorPermissions]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def perform_update(self, serializer):
        instance = serializer.save()
        id = instance.id
        newsletter_about_updates.delay(id, "lesson")


class LessonDestroyViewAPI(generics.DestroyAPIView):
    """Класс отвечает за удаление сущности (Урока)"""

    permission_classes = [UserInObjOrModeratorPermissions]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
