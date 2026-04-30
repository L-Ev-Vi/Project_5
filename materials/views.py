from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Subscriptions
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
        context['request'] = self.request
        return context

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     data = serializer.data
    #     data["subscriptions"] = Subscriptions.objects.get(course=instance.pk, user=self.request.user.pk).subscription
    #     return Response(data)


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


class LessonDestroyViewAPI(generics.DestroyAPIView):
    """Класс отвечает за удаление сущности (Урока)"""

    permission_classes = [UserInObjOrModeratorPermissions]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
