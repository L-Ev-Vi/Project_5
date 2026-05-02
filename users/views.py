from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from materials.models import Course

from .models import Payments, User, Subscriptions
from .permissions import UserInObjPermissions, UserIsObjPermissions
from .serializers import GeneralInformationUserSerializer, PaymentsSerializer, RetrieveUserSerializer, UserSerializer

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
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    ordering_fields = ("date",)
    filterset_fields = (
        "course",
        "lesson",
        "method",
    )

    def get_queryset(self):
        queryset = Payments.objects.filter(user=int(self.request.user.pk))
        return queryset


class PaymentsRetrieveViewAPI(generics.RetrieveAPIView):
    """Класс отвечает за отображение одной сущности (Платёж)"""

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated, UserInObjPermissions]


# Subscriptions

class SubscriptionseViewAPI(APIView):
    """Создание и удаление подписки."""

    def post(self, request, *args, **kwargs):
        user = request.user
        course = get_object_or_404(Course, pk=request.data.get("course"))
        subs_course = [sub.course for sub in user.user_subscriptions.all()]
        if course in subs_course:
            sub = Subscriptions.objects.get(course=course.pk, user=user.pk)
            if sub.subscription:
                sub.subscription = False
                message = "Подписка отключена!"
            else:
                sub.subscription = True
                message = "Подписка включена!"
            sub.save()
        else:
            Subscriptions.objects.create(course=course, user=user)
            message = "Подписка отключена!"
        return Response({"message": message})
