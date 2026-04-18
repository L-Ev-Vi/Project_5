from rest_framework import generics, viewsets

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Класс описывающий логику обработки HTTP запросов"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


# class UserCreateViewAPI(generics.CreateAPIView):
#     """Класс отвечает за создание сущности (Урока)"""
#     serializer_class = UserSerializer
#
#
# class UserListViewAPI(generics.ListAPIView):
#     """Класс отвечает за отображение списка сущностей (Уроков)"""
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#
#
# class UserRetrieveViewAPI(generics.RetrieveAPIView):
#     """Класс отвечает за отображение одной сущности (Урока)"""
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#
#
# class UserUpdateViewAPI(generics.UpdateAPIView):
#     """Класс отвечает за редактирование одной сущности (Урока)"""
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#
#
# class UserDestroyViewAPI(generics.DestroyAPIView):
#     """Класс отвечает за удаление сущности (Урока)"""
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
