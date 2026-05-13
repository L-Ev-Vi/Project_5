from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Payments, Subscriptions, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = User
        fields = "__all__"


class PaymentsSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = Payments
        fields = "__all__"

    def validate(self, data):
        """Проверка заполнения полей курс и урок"""
        if data.get("course") is None and data.get("lesson") is None:
            raise ValidationError("Необходимо выбрать курс или урок!")
        return data


class SubscriptionsSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = Subscriptions
        fields = "__all__"


class RetrieveUserSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    payments = PaymentsSerializer(many=True)
    subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone_number", "city", "payments", "subscriptions")

    def get_subscriptions(self, instance):
        subscriptions = instance.user_subscriptions.all()
        return subscriptions


class GeneralInformationUserSerializer(serializers.ModelSerializer):
    """Сериализаторы определяющий представление API"""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "email",
            "city",
        )
