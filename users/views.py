from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Payments
from .serializers import (UserSerializer,
                          PaymentsSerializer,
                          RetrieveUserSerializer,
                          GeneralInformationUserSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .permissions import UserIsObjPermissions, UserInObjOrPermissions


# Users

class UserViewSet(viewsets.ModelViewSet):
    """Класс описывающий логику обработки HTTP запросов"""
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return GeneralInformationUserSerializer
        elif self.action == "retrieve":
            if self.request.user == self.get_object():
                return RetrieveUserSerializer
            return GeneralInformationUserSerializer
        return UserSerializer

    def get_permissions(self):
        """Создает экземпляр и возвращает список разрешений, необходимых для этого представления."""
        if self.action == "create":
            permission_classes = [AllowAny]
        elif self.action in ("update", "partial_update", "destroy"):
            permission_classes = [IsAuthenticated, UserIsObjPermissions]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_user = serializer.save(is_active=True)
        new_user.set_password(new_user.password)
        new_user.save()


# Payments

class PaymentsCreateViewAPI(generics.CreateAPIView):
    """Класс отвечает за создание сущности (Платёж)"""
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        new_payment = serializer.save()
        new_payment.user = self.request.user
        new_payment.save()


class PaymentsListViewAPI(generics.ListAPIView):
    """Класс отвечает за отображение списка сущностей (Платёж)"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter,]
    ordering_fields = ("date",)
    filterset_fields = ("course", "lesson", "method",)

    def get_queryset(self):
        queryset = Payments.objects.filter(user=int(self.request.user.pk))
        return queryset


class PaymentsRetrieveViewAPI(generics.RetrieveAPIView):
    """Класс отвечает за отображение одной сущности (Платёж)"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated, UserInObjOrPermissions]
