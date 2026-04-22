from rest_framework import generics, viewsets

from .models import User, Payments
from .serializers import UserSerializer, PaymentsSerializer, RetrieveUserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

# Users

class UserViewSet(viewsets.ModelViewSet):
    """Класс описывающий логику обработки HTTP запросов"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = RetrieveUserSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = RetrieveUserSerializer
        return super().retrieve(request, *args, **kwargs)


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
