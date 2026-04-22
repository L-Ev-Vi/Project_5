from rest_framework import generics, viewsets

from .models import User, Payments
from .serializers import UserSerializer, PaymentsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

# Users

class UserViewSet(viewsets.ModelViewSet):
    """Класс описывающий логику обработки HTTP запросов"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Payments

class PaymentsCreateViewAPI(generics.CreateAPIView):
    """Класс отвечает за создание сущности (Платёж)"""
    serializer_class = PaymentsSerializer


class PaymentsListViewAPI(generics.ListAPIView):
    """Класс отвечает за отображение списка сущностей (Платёж)"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter,]
    ordering_fields = ("date",)
    filterset_fields = ("course", "lesson", "method",)


class PaymentsRetrieveViewAPI(generics.RetrieveAPIView):
    """Класс отвечает за отображение одной сущности (Платёж)"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


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
